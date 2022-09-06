
#include <stdlib.h>

#include <recGbl.h>
#include <alarm.h>
#include <menuFtype.h>
#include <aSubRecord.h>
#include <registryFunction.h>
#include <epicsExport.h>

/* group bits into words
 *
 * record(aSub, "name") {
 *     field(SNAM, "ISARA Group Bits")
 *     field(INPA, "") # Input bit array
 *     field(FTA , "SHORT")
 *     field(NOA , "256")
 *     field(OUTA, "") # bits 0-31.  (first char is bit 0)
 *     field(FTVA, "ULONG")
 *     field(OUTB, "") # bits 32-61
 *     field(FTVB, "ULONG")
 *     # ...
 * }
 */
static
long isara_group_bits(aSubRecord *prec)
{
    const epicsInt16 *inp;
    size_t c, o;
    size_t inplen;
    epicsUInt32 **out = (epicsUInt32**)&prec->vala;
    const epicsEnum16 *outf = &prec->ftva;
    const epicsUInt32 *outl = &prec->neva;
    size_t outcnt;
    const size_t maxoutcnt = (&prec->valu - &prec->vala);

    if(prec->fta!=menuFtypeSHORT) {
        recGblSetSevrMsg(prec, COMM_ALARM, INVALID_ALARM, "FTA");
        return 0;
    }

    inp = prec->a;
    inplen = prec->nea;

    for(outcnt=0; outcnt<maxoutcnt; outcnt++) {
        if(menuFtypeULONG!=outf[outcnt] || outl[outcnt]!=1)
            break;
    }

    for(c=0, o=0; c < inplen && o<outcnt; o++) {
        size_t b;
        epicsUInt32 word = 0;

        for(b=0; b<32 && c<inplen; c++, b++) {
            if(inp[c])
                word |= 1u<<b;
        }

        *out[o] = word;
    }

    if(!o) {
        recGblSetSevrMsg(prec, READ_ALARM, INVALID_ALARM, "Empty input");
    } else if(o<outcnt) {
        recGblSetSevrMsg(prec, READ_ALARM, INVALID_ALARM, "Insuf.");
    }

    return 0;
}

epicsRegisterFunction(isara_group_bits);
