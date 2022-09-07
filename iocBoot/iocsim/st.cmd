#!../../bin/linux-x86_64/isaraDemo

# record name prefix
epicsEnvSet("P", "TST:")
# Device IP address
epicsEnvSet("IP", "localhost")
# Optional: Override port numbers
#epicsEnvSet("PORT_CMD", "10000")
epicsEnvSet("PORT_STS", "10001")

epicsEnvSet("STREAM_PROTOCOL_PATH", "../../db")

## Register all support components
dbLoadDatabase "../../dbd/isaraDemo.dbd"
isaraDemo_registerRecordDeviceDriver(pdbbase) 

# error on re-use of record name
var dbRecordsOnceOnly 1

# Command socket
drvAsynIPPortConfigure("ISARA_CMD", "$(IP):$(PORT_CMD=10000)")
asynOctetSetInputEos("ISARA_CMD", -1, "\r")
asynOctetSetOutputEos("ISARA_CMD", -1, "\r")

asynSetTraceMask("ISARA_CMD", -1, 0x29)
asynSetTraceIOMask("ISARA_CMD", -1, 0x2)
#asynSetTraceFile("ISARA_CMD", -1, "command.log")

# Status socket
drvAsynIPPortConfigure("ISARA_STS", "$(IP):$(PORT_STS=1000)")
asynOctetSetInputEos("ISARA_STS", -1, "\r")
asynOctetSetOutputEos("ISARA_STS", -1, "\r")

#asynSetTraceMask("ISARA_STS", -1, 0x29)
#asynSetTraceIOMask("ISARA_STS", -1, 0x2)
#asynSetTraceFile("ISARA_STS", -1, "status.log")

# Records

dbLoadRecords("../../db/isara-command.db","P=$(P),DEV=ISARA_CMD")
dbLoadRecords("../../db/isara-status.db", "P=$(P),DEV=ISARA_STS")

# lots of noise...
#var("streamDebug", 5)

# autosave part 1
dbLoadRecords ("../../db/save_restoreStatus.db","P=$(P)AS:")
save_restoreSet_status_prefix("$(P)AS:")
save_restoreSet_Debug(0)
save_restoreSet_IncompleteSetsOk(1)
set_savefile_path("$(PWD)", "/as")
set_requestfile_path("$(PWD)", "/as")
system("install -m 777 -d $(PWD)/as")
set_pass0_restoreFile("ioc_settings.sav")

iocInit()

dbl > records.dbl

# autosave part 2
makeAutosaveFileFromDbInfo("$(PWD)/as/ioc_settings.req", "autosaveFields_pass0")
create_monitor_set("ioc_settings.req", 10, "")

epicsThreadSleep 1

dbcar '' 1
