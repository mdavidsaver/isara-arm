TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = isara
# isara.dbd will be created and installed
DBD += isara.dbd

# isara.dbd will be made up from these files:
isara_DBD += base.dbd

# Include dbd files from all support applications:
#isara_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#isara_LIBS += xxx

# isara_registerRecordDeviceDriver.cpp derives from isara.dbd
isara_SRCS += isara_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
isara_SRCS_DEFAULT += isaraMain.cpp
isara_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#isara_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
isara_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

