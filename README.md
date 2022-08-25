# EPICS Driver for ISARA Sample Mounting Robot

EPICS Driver for X-ray crystallography ISARA sample changer.

Requires:

- [EPICS](https://epics-controls.org/) [Base](https://epics.anl.gov/)
- [Asyn](https://epics-modules.github.io/master/asyn/)
- [StreamDevice](https://paulscherrerinstitute.github.io/StreamDevice/).

https://www.irelec-alcen.com/en/synchrotrons/x-ray-crystallography-isara-sample-changer

Based on document ISARA-NS-05 - ISARA Sample Changer, List of socket commands

## Current State

**Untested** and under active development!

## Contents

This module builds `isaraDemo` IOC executable,
and includes `iocBoot/iocdemo/st.cmd` for use with it.

A minimally functional simulator is provided for driver testing:

```sh
./isara-sim.py -S 10001
```

Concurrently:

```sh
cd iocBoot/iocsim
./st.cmd
```

## Other work

Another EPICS driver https://github.com/michel4j/aunt-isara
