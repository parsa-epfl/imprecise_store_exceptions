#!/usr/bin/python3
#
# See LICENSE for license details

import os
import re
import sys
import pandas as pd


def parse(fn):
    if not os.path.isfile(fn):
        sys.exit(f'ERROR: invalid file: {fn}')

    r = {}

    #                               name
    pat_run = re.compile(r'running (.+)')
    #                            user    kern
    pat_e2e = re.compile(r'e2e: (\d+) - (\d+)')
    #                            num_ld  num_st  num_all
    pat_exp = re.compile(r'exp: (\d+) - (\d+) - (\d+)')

    name = ''
    user = 0
    kern = 0
    nums = 0
    pers = 0

    with open(fn) as fd:
        for cs in fd:
            cs = cs.strip()

            if m := pat_run.match(cs):
                name = m.group(1)

            elif m := pat_e2e.match(cs):
                user = int(m.group(1))
                kern = int(m.group(2))

            elif m := pat_exp.match(cs):
                nums = int(m.group(2))
                diff = int(m.group(3)) - int(m.group(1))
                pers = nums / diff if diff else 0

                if name in r:
                    r[name].append((user, kern, nums, pers))
                else:
                    r[name] = [(user, kern, nums, pers)]

    return r


if __name__ == '__main__':
    def avg(a):
        return sum(a) / len(a)

    if len(sys.argv) < 2:
        sys.exit('Please provide the gap.log file')

    r = parse(sys.argv[1])

    t = pd.DataFrame(
            list(map(lambda x: list(map(avg, zip(*x))), r.values())),
            columns = ['User', 'Kernel', '# ISEs', '# FS per ISE'],
            index   = list(map(lambda x: x.upper(), r.keys())))

    print(t)
