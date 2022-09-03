TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

# hijack .db install rules
INSTALL_DB = $(INSTALL_LOCATION)/opi

DB += isara-main.bob

DB += isara-alarm.bob
DB += isara-di.bob
DB += isara-do.bob
DB += isara-sampledata.bob

DB += _isara-bit.bob
DB += _isara-readback.bob

ifeq (YES,$(BUILD_ISARA_DEMO))
# copy in external OPIs linked from our OPIs
DB_INSTALLS += $(ASYN)/opi/bob/autoconvert/asynRecord.bob
DB_INSTALLS += $(ASYN)/opi/bob/autoconvert/asynOctet.bob
DB_INSTALLS += $(ASYN)/opi/bob/autoconvert/asynIPPortSetup.bob
endif

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

