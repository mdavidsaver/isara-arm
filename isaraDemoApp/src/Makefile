TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = isaraDemo
# isaraDemo.dbd will be created and installed
DBD += isaraDemo.dbd

# isaraDemo.dbd will be made up from these files:
isaraDemo_DBD += base.dbd
isaraDemo_DBD += system.dbd

isaraDemo_DBD += asyn.dbd drvAsynIPPort.dbd
isaraDemo_DBD += stream.dbd

isaraDemo_DBD += isaraSupport.dbd

isaraDemo_LIBS += stream asyn
isaraDemo_LIBS += isaraSupport

ifneq (,$(AUTOSAVE))
isaraDemo_DBD += asSupport.dbd
isaraDemo_LIBS += autosave
endif

ifdef EPICS_QSRV_MAJOR_VERSION
isaraDemo_DBD += qsrv.dbd
isaraDemo_DBD += PVAServerRegister.dbd
isaraDemo_LIBS += qsrv
isaraDemo_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
endif

# isaraDemo_registerRecordDeviceDriver.cpp derives from isaraDemo.dbd
isaraDemo_SRCS += isaraDemo_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
isaraDemo_SRCS += isaraDemoMain.cpp

# Finally link to the EPICS Base libraries
isaraDemo_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
