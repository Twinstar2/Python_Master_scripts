#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import epros_file
from outliers import smirnov_grubbs as grubbs

# argparse for information
parser = argparse.ArgumentParser()
#parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
parser.add_argument("-e", "--energy", help="input energy profile directory")
#parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and prints out the quantil ranges"
    parser.print_help()
    sys.exit(0)


# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))

# ------------------------------------------------- main script ------------------------------------------------------ #

energy_list = []
counter = 0
total_file_count = sum([len(files) for r, d, files in os.walk(top=args.energy)])
print "started for:", total_file_count, "files"

for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        line_count = 0
        counter += 1
        if counter % 10000 == 0:
            print energy_file
        if energy_file.endswith(".ep2"):
            with open(dirpath + energy_file, 'r') as energy_file_handle:  # with open(energy_dir + file, 'r') as energy_file:
                for line in energy_file_handle:
                    line_array = line.split("\t")
                    if not "REMK" in line_array:
                        if line_count == 0:
                            name = line_array[1]
                        elif line_count == 1:
                            type = line_array[1]
                        elif line_count == 2:
                            header = line_array
                        else:
                            # just extract the A Chain
                            # if line_array[1] == "B":
                            #    break
                            energy_list.append(line_array[5].rstrip())
                    line_count += 1

energy_list = [float(x) for x in energy_list]
energy_list.sort()
# remove outliers with grubbs algorithm
energy_list = grubbs.test(energy_list, alpha=0.05)
print len(energy_list)
quant = len(energy_list)/4
print quant, "per entries per quantil"
print energy_list[0]
print energy_list[quant]
print energy_list[2*quant]
print energy_list[3*quant]
print energy_list[-1]


###################### OUT
'''
119460386
Quantil:  29865096
-118.303418308
-21.3328509911
-9.26231037705
-3.33429827376
11.5566432042

whithout outliers
Quantil:  29864995
-81,4800043161
-21,3326960217
-9,26223609962
-3,33428488184
11,5566432042
'''