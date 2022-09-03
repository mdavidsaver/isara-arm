# Makefile at top of application tree
TOP = .
include $(TOP)/configure/CONFIG

UNINSTALL_DIRS += $(INSTALL_LOCATION)/opi

# Directories to build, any order
DIRS += configure

DIRS += src
src_DEPEND_DIRS = configure

DIRS += src/Db
src/Db_DEPEND_DIRS = src

DIRS += src/opi
src/opi_DEPEND_DIRS = configure

DIRS += $(wildcard iocBoot)
iocBoot_DEPEND_DIRS += src src/Db

ifeq (YES,$(BUILD_ISARA_DEMO))
DIRS += isaraDemoApp
isaraDemoApp_DEPEND_DIRS += src
iocBoot_DEPEND_DIRS += isaraDemoApp
endif

# Add any additional dependency rules here:

include $(TOP)/configure/RULES_TOP
