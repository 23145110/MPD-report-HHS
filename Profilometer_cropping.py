# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:22:09 2026

@author: 23145110
"""
import json
import matplotlib.pyplot as plt
import time
import numpy as np
from math import ceil


def find_step(z, treshold, diff_array_width, prominance):
    step_indexes = np.array([])
    step_heights = np.array([])

    x = ceil(diff_array_width/2)
    for n in range(x, len(z)-x):
        arr = z[n-x:n+x]
        diff = max(arr) - min(arr)

        prom = ceil(prominance/2)
        if diff >= treshold:

            condition = (step_indexes > n - prom) & (step_indexes < n + prom)

            # indx = step_indexes[condition]
            heights = step_heights[condition]

            if heights.size > 0:
                if diff > max(heights):
                    step_indexes = np.delete(step_indexes, condition)
                    step_heights = np.delete(step_heights, condition)

                    step_indexes = np.append(step_indexes, n)
                    step_heights = np.append(step_heights, diff)

                else:
                    pass
            else:
                step_indexes = np.append(step_indexes, n)
                step_heights = np.append(step_heights, diff)

    steps = []
    heights = []
    for k in range(len(step_indexes)):
        n = int(step_indexes[k])
        region = z[n-x:n+x]

        steps.append((np.argmin(region)+n-x, np.argmax(region)+n-x))
        heights.append((min(region), max(region)))

    return steps, heights


t0 = time.time()
with open(r"Height_data2.json") as f:
    data_dict = json.load(f)

tload_file = time.time()

used_keys = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
             "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]

used_names = ["alignment_markL", "alignment_markM", "alignment_markR", "Pad1",
              "Pad4", "Pad5", "Pad8"]


final_vals = {"W2Al6t": "65,150,1000", "W2Al6b": "65,150,1000",
              "W2Al7t": "65,150,1000", "W2Al7b": "65,150,1000",
              "W2Al8t": "50,175,9000", "W2Al8b": "65,85,5000",
              "W2Al9t": "65,120,10000", "W2Al9b": "65,180,9000"}

# W2Al8b Mark Left,
# W2Al9t Mark right (can't find proper step) and
# W2Al9b pad 8 are still problems. Can fix by hand.

problem_names = {"W2Al8b_alignment_markL": (28300, 42400), "W2Al9t_alignment_markR": (
    23000, 36450), "W2Al9b_Pad4": (9900, 38700), "W2Al9b_Pad8": (0, 42000)}

# after cropping a bit manually, only W2Al9t MR and W2Al8bML does not work


def one_picture(data_dict, key, name, slc):
    data_x, data_z = data_dict[key][name]

    data_x = np.array(data_x)
    data_z = np.array(data_z)

    x = data_x[int(slc[0]):int(slc[1])]
    z = data_z[int(slc[0]):int(slc[1])]

    plt.plot(x/1E6, z)
    plt.grid()
    plt.xlabel(r"length $x$ [ mm ]")
    plt.ylabel(r"height $z$ [ nm ]")

    # plt.title(f"{key} {name}")
    plt.show()


def whole_picture_array():
    n = 0
    while n < 8:
        key = used_keys[n]
    # for key in used_keys:
        bb = final_vals[key]
        try:
            vals = [int(x) for x in bb.split(",")]

            for name in used_names:
                data_x, data_z = data_dict[key][name]

                if f"{key}_{name}" in problem_names:
                    val = problem_names[f"{key}_{name}"]
                    data_x = data_x[val[0]:val[1]]
                    data_z = data_z[val[0]:val[1]]
                    print(val)

                data_x = np.array(data_x)
                data_z = np.array(data_z)

                peaks, heights = find_step(data_z, vals[0], vals[1], vals[2])
                print(f"peaks: {peaks}")
                print(f"heights: {heights}")
                print("")
                try:
                    if f"{key}_{name}" in ["W2Al9t_alignment_markR",
                                           "W2Al8b_alignment_markL",
                                           "W2Al9b_Pad4"]:
                        x = data_x.copy()
                        z = data_z.copy()
                    else:
                        x = data_x[int(peaks[0][0]):int(peaks[-1][0])]
                        z = data_z[int(peaks[0][0]):int(peaks[-1][0])]

                    plt.plot(x/1E6, z)
                    plt.grid()
                    plt.xlabel(r"length $x$ [ mm ]")
                    plt.ylabel(r"height $z$ [ nm ]")

                    # plt.title(f"{key} {name}")
                    plt.show()
                except:
                    print(f"Failed {key} {name}")
        except:
            pass

        aa = input("proceed?")
        if aa == "y":
            n += 1
        else:
            pass


def save_cropped_data():
    cropped_data = dict()
    t0 = time.time()
    for key in used_keys:
        print(f"working on {key}")
        single_struct_dict = dict()

        bb = final_vals[key]

        try:
            vals = [int(x) for x in bb.split(",")]

            for name in used_names:
                data_x, data_z = data_dict[key][name]

                if f"{key}_{name}" in problem_names:
                    val = problem_names[f"{key}_{name}"]
                    data_x = data_x[val[0]:val[1]]
                    data_z = data_z[val[0]:val[1]]
                    # print(val)

                peaks, heights = find_step(
                    np.array(data_z), vals[0], vals[1], vals[2])
                # print(f"peaks: {peaks}")
                # print(f"heights: {heights}")
                # print("")
                try:
                    if f"{key}_{name}" in ["W2Al9t_alignment_markR",
                                           "W2Al8b_alignment_markL",
                                           "W2Al9b_Pad4"]:
                        x = data_x
                        z = data_z
                    else:
                        x = data_x[int(peaks[0][0]):int(peaks[-1][0])]
                        z = data_z[int(peaks[0][0]):int(peaks[-1][0])]

                    single_struct_dict.update({name: {"x": x, "z": z}})
                except:
                    print(f"Failed {key} {name}")
        except:
            pass
        cropped_data.update({key: single_struct_dict})

    t1 = time.time()
    print(f"Done cropping data, time elapsed: {t1-t0}")
    print("Saving data")

    with open(r"Cropped_height_data.json", "w") as f:
        json.dump(cropped_data, f)
    print("Done saving")
    print(f"Time elapsed saving: {time.time()-t1}")

    print("Exiting function")
    print(f"Time elapsed in function: {time.time()-t0}")
    return None
