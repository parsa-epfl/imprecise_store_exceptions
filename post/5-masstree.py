#!/usr/bin/python3

import os
import re
import sys
import json


def parse(fn):
    if not os.path.isfile(fn):
        sys.exit(f'ERROR: invalid file: {fn}')

    with open(fn) as fd:
        for cs in fd:
            if cs.startswith('{"table":"mb",'):
                try:
                    return float(json.loads(cs)['ops_per_sec'])
                except:
                    sys.exit(f'ERROR: fail to parse data from: {cs}')

    return float('nan')


if __name__ == '__main__':
    def avg(a):
        return sum(a) / len(a)

    if len(sys.argv) < 3:
        sys.exit('Please provide the masstree.log and masstree-ref.log files')

    r_ise = parse(sys.argv[1])
    r_ref = parse(sys.argv[2])

    print(f'Aggregated throughput for {sys.argv[1]} is : {r_ise} ops/sec')
    print(f'Aggregated throughput for {sys.argv[2]} is : {r_ref} ops/sec')
    print(f'Slowdown: {r_ise / r_ref :.2f}x')
