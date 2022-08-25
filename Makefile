# Makefile at top of application tree
TOP = .
include $(TOP)/configure/CONFIG

# Directories to build, any order
DIRS += configure

DIRS += src
src_DEPEND_DIRS = configure

DIRS += src/Db
src/Db_DEPEND_DIRS = src

DIRS += isaraDemoApp
isaraDemoApp_DEPEND_DIRS += src

DIRS += $(wildcard iocBoot)
iocBoot_DEPEND_DIRS += src src/Db isaraDemoApp

# Add any additional dependency rules here:

include $(TOP)/configure/RULES_TOP
