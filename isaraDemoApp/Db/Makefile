TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
# Create and install (or just install) into <top>/db
# databases, templates, substitutions like this
#DB += xxx.db

# copy in from external modules to be self-contained

DB_INSTALLS += $(ASYN)/db/asynRecord.db

ifneq ($(AUTOSAVE),)
DB_INSTALLS += $(firstword $(wildcard $(AUTOSAVE)/asApp/Db/save_restoreStatus.db $(AUTOSAVE)/db/save_restoreStatus.db))
endif

#----------------------------------------------------
# If <anyname>.db template is not named <anyname>*.template add
# <anyname>_template = <templatename>

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

