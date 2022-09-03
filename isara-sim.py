#!/usr/bin/env python3
"""
Bare bones simulation of ISARA sample auto-mounter arm
"""

import asyncio
from dataclasses import dataclass, field
from functools import wraps
import logging
import re
import signal

import numpy

_log = logging.getLogger()

# <cmd>
# <cmd> '(' <args> ')'
_cmd = re.compile(rb'([a-z_]+)(?:\(([^)]*)\))?')

def task_guard(corofn):
    """Make some noise if a Task ends with an error
    """
    async def wrapper(*args, **kws):
        coro = corofn(*args, **kws)
        try:
            return (await coro)
        except (asyncio.CancelledError, asyncio.IncompleteReadError) as e:
            _log.debug('%r %s', coro, e)
        except:
            _log.exception(coro)
    return wrapper

@dataclass(frozen=True)
class Path:
    # final arm position name
    ends: str
    # time to complete move
    duration: float = 3.0

# trajectories
_paths = {
    b'home':Path('HOME'),
    b'recover':Path('HOME'),
    b'put':Path('GONIO'),
    b'get':Path('DEWAR_CENTER'),
    b'getput':Path('GONIO'),
    b'pick':Path('SOAK'),
    b'datamatrix':Path('DEWAR_CENTER'),
    b'back':Path('DEWAR_CENTER'),
    b'soak':Path('SOAK'),
    b'dry':Path('DRY_END'),
    b'gotodif':Path('GONIO'),
    b'putplate':Path('GONIO'),
    b'getplate':Path('TOOL_STORE'),
    b'platetodif':Path('GONIO'),
    b'teachgonio':None,
    b'teachpuck':None,
    b'teachdewar':None,
    b'teachplateholder':None,
    b'changetool':Path('TOOL_STORE'),
    b'toolcal':Path('PARK'),
}

@dataclass
class State:
    """Simulate state
    """

    # values returned in reply to b'state' command
    # 0
    power: bool = False
    remote: bool = False
    fault_stop: bool = False
    tool: str = 'DoubleGripper'
    position: str = 'HOME'
    path: str = ''
    gripA: bool = False
    gripB: bool = False
    puckA: int = -1
    sampleA: int = -1
    # 10
    puckB: int = -1
    sampleB: int = -1
    puckDiff: int = -1
    sampleDiff: int = -1
    plateTool: int = -1
    plateDiff: int = -1
    lastDM: str = ''
    seqRun: bool = False
    seqPause: bool = False
    speedRatio: float = 100.0
    # 20
    ln2Reg: bool = False
    soakingPhases: int = 7
    ln2Level: float = 86.15965
    ln2Max: float = 89.0
    ln2Min: float = 87.0
    camTrack: bool = False
    gripDrying: bool = False
    ln2PhaSep: bool = False
    lastMsg: str = 0
    binAlarm: int = 0

    # position
    # (x, y, z, Rx, Ry, Rz)
    pos: numpy.ndarray = field(default_factory=lambda:numpy.zeros((6,)))

    # raw digital intputs/outputs
    di: numpy.ndarray = field(default_factory=lambda:numpy.zeros((112,), dtype='?'))
    do: numpy.ndarray = field(default_factory=lambda:numpy.zeros((112,), dtype='?'))

    # last system message
    message: str = 'System OK for operation'

    # implied/hidden/fake state

    # current traj(...) args
    s_traj: list = None
    # time since start of move, because we don't model position/velocity
    s_time: float = 0.0
    # path of current move
    s_path: Path = None
    # client which initiated move
    s_client: asyncio.StreamWriter = None

    def state(self) -> [str]:
        S = [
            self.power,
            self.remote,
            self.fault_stop,
            self.tool,
            self.position,
            self.path,
            self.gripA,
            self.gripB,
            self.puckA,
            self.sampleA,
            self.puckB,
            self.sampleB,
            self.puckDiff,
            self.sampleDiff,
            self.plateTool,
            self.plateDiff,
            self.lastDM,
            self.seqRun,
            self.seqPause,
            self.speedRatio,
            self.ln2Reg,
            self.soakingPhases,
            self.ln2Level,
            self.ln2Max,
            self.ln2Min,
            self.camTrack,
            self.gripDrying,
            self.ln2PhaSep,
            self.lastMsg,
            self.binAlarm,
        ]
        S.extend([str(p) for p in self.pos]) # 6 items
        S.extend('21.5,-15.6,97.1,0.0,98.5,-23.5'.split(',')) # joint position
        S.append(self.lastMsg)
        S.extend(["0"]*(58-42)) # unused
        S.append('changetool|3|3|0|3.248|-0.01|392.597|0.0|0.0|-2.375')

        R = [None]*len(S)
        for i,s in enumerate(S):
            if isinstance(s, bool):
                R[i] = '1' if s else '0'
            elif isinstance(s, (int, float, str)):
                R[i] = str(s)
            else:
                raise NotImplementedError(type(s))
        return R

def state_gate(cond, msg):
    def dec(fn):
        @wraps(fn)
        def wrapper(self, args):
            if not cond(self.S):
                return msg
            return fn(self, args)
        return wrapper
    return dec

class ISARA:
    def __init__(self):
        self.reset()
        self.simWake = asyncio.Event()
        self.run = True

    def reset(self):
        self.S = State()
        self.S.lastMsg = 'System OK for operation'

        self.S.di[:] = numpy.asarray('1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0'.split(' '), dtype='u1')

        self.S.do[:] = numpy.asarray('0 0 0 0 0 1 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'.split(' '), dtype='u1')

        self.S.binAlarm |= 0x40000000

        self.S.pos[:] = [304.7,139.9,-94.4,0.0,-180.0,-47.5]

    @task_guard
    async def sim(self):
        loop = asyncio.get_running_loop()
        prev = loop.time()
        while self.run:
            try:
                await asyncio.wait_for(self.simWake.wait(), timeout=0.1)
            except asyncio.TimeoutError:
                pass # simulation tick
            self.simWake.clear()

            now = loop.time()
            dT = now - prev
            prev = now

            if not self.S.power:
                continue # nothing to do when Off

            if self.S.seqRun and not self.S.seqPause:
                self.S.s_time += dT
                _log.debug('Move in progress... %f, %f / %f', dT, self.S.s_time, self.S.s_path.duration)
                if self.S.s_time >= self.S.s_path.duration:
                    _log.info('Move complete %r, %r', self.S.s_traj, self.S.s_path)

                    if self.S.s_client is not None:
                        self.S.s_client.write(self.S.s_traj + b'\r')
                        await self.S.s_client.drain()

                    self.S.path = ''
                    self.S.position = self.S.s_path.ends
                    self.S.seqRun = False

                    self.S.s_traj = self.S.s_path = None
                    self.S.s_time = 0.0

    def cmd_poweron(self, args):
        self.S.power = True

    def cmd_poweroff(self, args):
        self.S.power = False

    def cmd_speedup(self, args):
        self.S.speedRatio = max(100.0, self.S.speedRatio+1.0)

    def cmd_speeddown(self, args):
        self.S.speedRatio = min(0.01, self.S.speedRatio-1.0)

    def cmd_panic(self, args):
        self.S.power = False
        self.S.path = ''
        self.S.seqRun = self.S.seqPause = False
        self.S.s_traj = self.S.s_path = None
        self.S.s_time = 0.0

    def cmd_abort(self, args):
        self.S.path = ''
        self.S.seqRun = self.S.seqPause = False
        self.S.s_traj = self.S.s_path = None
        self.S.s_time = 0.0

    def cmd_pause(self, args):
        self.S.seqPause = True

    def cmd_restart(self, args):
        self.S.seqPause = False

    def cmd_regulon(self, args):
        self.S.ln2Reg = True

    def cmd_reguloff(self, args):
        self.S.ln2Reg = False

    def cmd_ps_regulon(self, args):
        self.S.ln2PhaSep = True

    def cmd_ps_reguloff(self, args):
        self.S.ln2PhaSep = False

    @state_gate(lambda S:S.power, b"Robot power disabled")
    def cmd_traj(self, args):
        path = _paths.get(args[0])
        if path is not None:
            self.S.s_path = path
            self.S.s_traj = args[0]
            self.S.s_time = 0.0

            self.S.path = args[0].decode()
            self.S.seqRun = True
            _log.info('Moving on %r %r', self.S.path, path)
            return False # defer reply

        else:
            _log.error('Ignore unknown traj(%r)', args)
            return b'Unknown/unmodeled trajectory'

    @task_guard
    async def new_cmd_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle client on Command socket
        """
        try:
            while self.run:
                line = reply = (await reader.readuntil(b'\r'))[:-1]
                M = _cmd.match(line)
                if M is None:
                    _log.error('Pretend success for unknown/unmodeled %r', line)
                    reply = None

                else:
                    meth = getattr(self, 'cmd_' + M.group(1).decode())

                    reply = meth((M.group(2) or b'').split(b','))

                    if asyncio.iscoroutine(reply):
                        reply = await reply

                if reply is None:
                    reply = line # most commands just echo on success

                elif reply is False:
                    self.S.s_client = writer
                    continue # defer reply

                writer.write(reply + b'\r')
                await writer.drain()

        finally:
            if self.S.s_client is writer:
                _log.warning('Client orphans move')
                self.S.s_client = None
            if not writer.is_closing():
                writer.close()

    @task_guard
    async def new_sts_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle client on Status socket
        """
        while self.run:
            line = (await reader.readuntil(b'\r'))[:-1]
            if line==b'position':
                ret = ','.join(['%.3f'%p for p in self.S.pos])
                writer.write(f'position({ret})\r'.encode())

            elif line==b'state':
                ret = ','.join(self.S.state())
                writer.write(f'state({ret})\r'.encode())

            elif line==b'di':
                ret = ','.join(['1' if p else '0' for p in self.S.di])
                writer.write(f'di({ret})\r'.encode())

            elif line==b'do':
                ret = ','.join(['1' if p else '0' for p in self.S.do])
                writer.write(f'do({ret})\r'.encode())

            elif line==b'message':
                writer.write(self.S.lastMsg.encode() + b'\r')

            elif line==b'sampledata':
                writer.write(b'sampledata(0.0,0.0,9.0,8.0,0.0,24.98,0.0,14.19,52.11,13.13,79.46,1202,21,0,0,0,0,0,0,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,)\r')

            else:
                writer.write(b'Unexpected status command\r')

            await writer.drain()

def getargs():
    from argparse import ArgumentParser
    P = ArgumentParser()
    P.add_argument('-d', '--debug', action='store_true')
    P.add_argument('-C', '--command-port', metavar='PORT', type=int, default=10000)
    P.add_argument('-S', '--status-port', metavar='PORT', type=int, default=1000)
    P.add_argument('-B', '--bind', metavar='IP', default=None)
    return P

async def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    _log.info('Starting')

    loop = asyncio.get_running_loop()
    if args.debug:
        loop.set_debug(True)

    # capture SIGINT for orderly shutdown
    done = asyncio.Event()
    loop.add_signal_handler(signal.SIGINT, done.set)
    loop.add_signal_handler(signal.SIGTERM, done.set)

    # prepare simulation
    dev = ISARA()
    simT = asyncio.create_task(dev.sim(), name='Sim')

    # start listening
    cmd_srv = await asyncio.start_server(dev.new_cmd_client, host=args.bind, port=args.command_port)
    for sock in cmd_srv.sockets:
        _log.info("Listening for Commands on %s", sock.getsockname())

    sts_srv = await asyncio.start_server(dev.new_sts_client, host=args.bind, port=args.status_port)
    for sock in sts_srv.sockets:
        _log.info("Listening for Status on %s", sock.getsockname())

    _log.info('Running')
    await done.wait()
    _log.info('Stopping')

    # interrupt sim task
    dev.run = False
    dev.simWake.set()

    # stop listening and close active connections
    cmd_srv.close()
    sts_srv.close()

    # join tasks
    for F in (cmd_srv.wait_closed(), sts_srv.wait_closed(), simT):
        try:
            await F
        except asyncio.CancelledError:
            pass

    _log.info('Done')

if __name__=='__main__':
    asyncio.run(main(getargs().parse_args()))
