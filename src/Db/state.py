#!/usr/bin/env python3

import sys

with open(sys.argv[1], 'r') as F:
    ents = F.readlines()

fmt = []
recs = []

fmt2rec = {
    "b": "bi",
    "s": "stringin",
    "]": "stringin",
    "d": "longin",
    "u": "longin",
    "f": "ai",
}

first=True
for line in ents:
    line = line.strip()
    if not line or line[0]=='#':
        continue

    line = line.split()

    if first:
        first = False
        fmt.append(f'%{line[0]}')
    else:
        fmt.append(f'%(\\$1{line[1]}){line[0]}')

    recs.append(f'record({fmt2rec[line[0][-1]]}, "$(P){line[1]}") {{}}')

print(f"state({','.join(fmt)})")

print("")

[print(r) for r in recs]
