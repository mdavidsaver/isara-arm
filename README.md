# EPICS Driver for ISARA Sample Mounting Robot

EPICS Driver for X-ray crystallography ISARA sample changer.

https://www.irelec-alcen.com/en/synchrotrons/x-ray-crystallography-isara-sample-changer

Based on document:

- ISARA-NS-05 rev. 13 - ISARA Sample Changer, List of socket commands
- ISARA-NS-12 rev. 2  - I/O List, for interpreting `di`/`do` responses

Requires:

- [EPICS](https://epics-controls.org/) [Base](https://epics.anl.gov/)
- [Asyn](https://epics-modules.github.io/master/asyn/)
- [busy](https://github.com/epics-modules/busy)
- [StreamDevice](https://paulscherrerinstitute.github.io/StreamDevice/) built with the optional PCRE support

Optional:

- [autosave](https://github.com/epics-modules/autosave) (persist user arguments to trajectory commands)

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

OPI screen files are installed under `opi/`.

## Including in an IOC.

See `isaraDemoApp/src/Makefile`.

## Build options

To omit building/installing the `isaraDemo` executable.

```sh
echo "BUILD_ISARA_DEMO=NO" >> configure/CONFIG_SITE.local
```

## Other work

Another EPICS driver https://github.com/michel4j/aunt-isara
