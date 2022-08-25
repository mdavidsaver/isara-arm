#!../../bin/linux-x86_64/isaraDemo

# record name prefix
epicsEnvSet("P", "TST:")
# Device IP address
epicsEnvSet("IP", "localhost")
# Optional: Override port numbers
#epicsEnvSet("PORT_CMD", "10000")
#epicsEnvSet("PORT_STS", "1000")

epicsEnvSet("STREAM_PROTOCOL_PATH", "../../db")

## Register all support components
dbLoadDatabase "../../dbd/isaraDemo.dbd"
isaraDemo_registerRecordDeviceDriver(pdbbase) 

# Command socket
drvAsynIPPortConfigure("ISARA_CMD", "$(IP):$(PORT_CMD=10000)")
asynOctetSetInputEos("ISARA_CMD", -1, "\r")
asynOctetSetOutputEos("ISARA_CMD", -1, "\r")

#asynSetTraceMask("ISARA_CMD", -1, 0x29)
#asynSetTraceIOMask("ISARA_CMD", -1, 0x6)
#asynSetTraceFile("ISARA_CMD", -1, "command.log")

# Status socket
drvAsynIPPortConfigure("ISARA_STS", "$(IP):$(PORT_STS=1000)")
asynOctetSetInputEos("ISARA_STS", -1, "\r")
asynOctetSetOutputEos("ISARA_STS", -1, "\r")

#asynSetTraceMask("ISARA_STS", -1, 0x29)
#asynSetTraceIOMask("ISARA_STS", -1, 0x6)
#asynSetTraceFile("ISARA_STS", -1, "status.log")

# Records

dbLoadRecords("../../db/isara-command.db","P=$(P),DEV=ISARA_CMD")
dbLoadRecords("../../db/isara-status.db", "P=$(P),DEV=ISARA_STS")

# lots of noise...
#var("streamDebug", 5)

iocInit()

#dbl > records.dbl
