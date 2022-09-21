# EPICS Driver for ISARA Sample Mounting Robot

EPICS Driver for X-ray crystallography ISARA sample changer.

https://www.irelec-alcen.com/en/synchrotrons/x-ray-crystallography-isara-sample-changer

Based on document:

- ISARA-NS-05 rev. 13 - ISARA Sample Changer, List of socket commands
- ISARA-NS-12 rev. 2  - I/O List, for interpreting `di`/`do` responses

Requires:

- [EPICS](https://epics-controls.org/) [Base](https://epics.anl.gov/)
- [asyn](https://epics-modules.github.io/master/asyn/)
- [busy](https://github.com/epics-modules/busy)
- [StreamDevice](https://paulscherrerinstitute.github.io/StreamDevice/)

Optional:

- [autosave](https://github.com/epics-modules/autosave) (persist user arguments to trajectory commands)

## Current State

**Untested** and under active development!

## Including in an IOC.

```make
PROD_IOC += myIoc

myIoc_DBD += asyn.dbd drvAsynIPPort.dbd
myIoc_DBD += busySupport.dbd
myIoc_DBD += stream.dbd
myIoc_DBD += isaraSupport.dbd

myIoc_LIBS += stream
myIoc_LIBS += busy
myIoc_LIBS += asyn
myIoc_LIBS += isaraSupport

...
```

See for a working example: `isaraDemoApp/src/Makefile`.

## isaraDemo IOC

By default this module builds the `isaraDemo` IOC executable,
which can be used to run `iocBoot/iocsim/st.cmd` in conjunction
with the included (minimal) device simulator.

```sh
./isara-sim.py -S 10001
```

Concurrently:

```sh
cd iocBoot/iocsim
./st.cmd
```

OPI screen files are installed under `opi/`.

### Skip building demo IOC

To omit building/installing the `isaraDemo` executable.

```sh
echo "BUILD_ISARA_DEMO=NO" >> configure/CONFIG_SITE.local
```

## Forward Compatibility

It is anticipated the future versions of the robot firmware will
add new command and status requests.  The output of the existing
status replies might also be extended.
To facilitate this, extra output arguments to the status replies
will be ignored.

It is assumed that any string values in status replies will never
included escaped comma '\,' or right parenthesis '\)' sequences.

## Other work

Another EPICS driver https://github.com/michel4j/aunt-isara
