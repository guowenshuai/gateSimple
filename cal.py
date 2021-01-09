#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def rate(n1, n2):
    print("增长率 %f" % ((n2-n1)*100/n1))

if __name__ == "__main__":
    rate(float(sys.argv[1]), float(sys.argv[2]))