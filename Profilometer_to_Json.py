# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:54:42 2026

@author: 23145110
"""
import json
import numpy as np
import xml.etree.ElementTree as ET
import time


def parse_XML(Struct_name):
    fnames = ["alignment_markL", "alignment_markM", "alignment_markR", "Pad1",
              "Pad4", "Pad5", "Pad8"]
    part1 = r'c:\users\koxal\desktop\school\year 3\mpd\quick_folder\profilometer'

    single_struct = dict()

    for name in fnames:
        filepath = rf"{part1}\{Struct_name}\{Struct_name}_{name}.xml"
        tree = ET.parse(filepath)
        root = tree.getroot()

        x_list = []
        y_list = []
        data_block = root[1]
        for child in data_block:
            x_list.append(float(child[0].text))
            y_list.append(float(child[1].text))

        if Struct_name == "W2Al6t" and name == "Pad4":
            # needs leveling, was not done properly in profilometer
            y = np.array(y_list)
            p1 = (7325, y[7325])
            p2 = (27050, y[27050])

            print(f"p1: {p1}, p2: {p2}")
            a = (p2[1]-p1[1])/(p2[0]-p1[0])
            b = p2[1] - a*p2[0]
            y = y - (a*np.linspace(0, len(y)-1, 1)+b)

            print(y[7325])

            print(f"a: {a}, b: {b}")

            y_list = list(y)
        single_struct.update({name: [x_list, y_list]})

    return single_struct


t0 = time.time()
used_keys = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
             "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]


profilometer_data = dict()

for key in used_keys:
    single_struct = parse_XML(key)

    profilometer_data.update({key: single_struct})

with open(r"c:\users\koxal\desktop\school\year 3\mpd\quick_folder\height_data2.json", "w") as f:
    json.dump(profilometer_data, f)

print(f"time elapsed: {time.time()-t0} seconds")
