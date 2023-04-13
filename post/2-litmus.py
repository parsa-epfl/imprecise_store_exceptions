#!/usr/bin/python3

import sys
import subprocess


def run(hw, mod):
    return subprocess.check_output(['mcompare7', '-nohash', hw, mod])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Please provide both the litmus.log and a model (herd) log')

    r = run(sys.argv[1], sys.argv[2]).decode('utf-8')
    f = False

    for cs in r.split('\n'):
        if cs.startswith('!!! Warning negative differences in'):
            print(cs)
            f = True
            break

    if not f:
        print('OK')
