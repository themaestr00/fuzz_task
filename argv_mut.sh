#!/usr/bin/bash

afl-fuzz -i $1/inputs -o $1/outputs -$2 fuzzer$3 -- bin/agrep-argv