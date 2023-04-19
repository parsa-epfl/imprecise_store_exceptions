#!/usr/bin/python3
#
# See LICENSE for license details

import os
import sys
import numpy  as np
import pandas as pd


def parse_raw(fn):
    def rd(fd):
        def cov(s):
            try:
                return float(s)
            except Exception:
                return float('nan')
        for cs in fd:
            yield list(map(cov, cs.split()))

    r = []

    with open(fn) as fd:
        # skip 3 lines
        for i in range(3):
            fd.readline()

        for cs in rd(fd):
            r.extend(cs)

    return r


def parse(fn):
    if not os.path.isfile(fn):
        sys.exit(f'ERROR: invalid file: {fn}')

    c = ['enum',
         'snum',
         'pcycle',
         'pinst',
         'lcycle',
         'lisnt',
         'acycle',
         'ainst',
         'ucycle',
         'uinst']

    r = parse_raw(fn)[:-1]
    n = len(r) // 10
    d = pd.DataFrame(np.array(r).reshape(n, 10),
                     columns = pd.Index(c),
                     index   = pd.Index(list(map(int, range(n)))))

    # average os performing time per store
    d['ppers' ] = d['pcycle'] / d['snum'  ]

    # misc part of the handler
    d['mcycle'] = d['acycle'] - d['ucycle'] - d['lcycle'] + d['pcycle']
    # per store
    d['mpers' ] = d['mcycle'] / d['snum'  ]

    # batch number
    d['sbatch'] = d['snum'  ] / d['enum'  ]

    # per load/store user-level overhead
    d['xcycle'] = d['ucycle'] - d[d['enum'] == 0.0]['ucycle'].mean()
    # per store
    d['xpers' ] = d['xcycle'] / d['snum'  ]

    return d


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'Please provide the mbench.log file')

    s = parse(sys.argv[1])

    # large variation
    x = s[(s['snum'] != 0.0) & (s['xpers'] >= 0.0) & (s['xpers'] < 200.0)]

    # this makes more sense
    m = x[ x['sbatch'] == 1.0]
    n = x[(x['sbatch'] >= 5.0) & (x['sbatch'] < 6.0)]

    print(m)

    t = pd.DataFrame([[
            m['xpers'].mean(),
            m['ppers'].mean(),
            m['mpers'].mean()
        ], [
            n['xpers'].mean(),
            n['ppers'].mean(),
            n['mpers'].mean()
        ]],
        columns = [
            'Microarchitectural',
            'Performing Stores',
            'Context Switch & Misc.'
        ],
        index   = [
            'Imprecise',
            'Imprecise w. Batching'
        ]
    )

    print(t)
