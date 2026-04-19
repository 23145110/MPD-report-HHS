# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:45:07 2026

@author: 23145110
"""
import json
import numpy as np
import matplotlib.pyplot as plt


def calc_mean_and_std(used_keys):
    out_dict = dict()
    for key in used_keys:  # calculates the mean and std of each channel and puts it in a dict
        try:
            Mean_A = sum(data_dict[key]["A"])/len(data_dict[key]["A"])
            std_A = np.std(data_dict[key]["A"])
        except:
            Mean_A = 0
            std_A = 0

        try:
            Mean_B = sum(data_dict[key]["B"])/len(data_dict[key]["B"])
            std_B = np.std(data_dict[key]["B"])
        except:
            Mean_B = 0
            std_B = 0

        try:
            Mean_C = sum(data_dict[key]["C"])/len(data_dict[key]["C"])
            std_C = np.std(data_dict[key]["C"])
        except:
            Mean_C = 0
            std_C = 0

        try:
            Mean_AB = sum(data_dict[key]["AB"])/len(data_dict[key]["AB"])
            std_AB = np.std(data_dict[key]["AB"])
        except:
            Mean_AB = 0
            std_AB = 0

        try:
            Mean_BC = sum(data_dict[key]["BC"])/len(data_dict[key]["BC"])
            std_BC = np.std(data_dict[key]["BC"])
        except:
            Mean_BC = 0
            std_BC = 0

        try:
            Mean_ABC = sum(data_dict[key]["ABC"])/len(data_dict[key]["ABC"])
            std_ABC = np.std(data_dict[key]["ABC"])
        except:
            Mean_ABC = 0
            std_ABC = 0

        this_dict = {"R_A": [Mean_A, std_A], "R_B": [Mean_B, std_B], "R_C": [Mean_C, std_C],
                     "R_AB": [Mean_AB, std_AB], "R_BC": [Mean_BC, std_BC], "R_ABC": [Mean_ABC, std_ABC]}

        out_dict.update({key: this_dict})
    return out_dict


def hist_plot():

    resistance_list = []
    for key in used_keys:
        R_A = res_dict[key]["R_A"][0] if res_dict[key]["R_A"][0] != 0 else np.nan
        R_B = res_dict[key]["R_B"][0] if res_dict[key]["R_B"][0] != 0 else np.nan
        R_C = res_dict[key]["R_C"][0] if res_dict[key]["R_C"][0] != 0 else np.nan
        R_AB = res_dict[key]["R_AB"][0] / \
            2 if res_dict[key]["R_AB"][0] != 0 else np.nan
        R_BC = res_dict[key]["R_BC"][0] / \
            2 if res_dict[key]["R_BC"][0] != 0 else np.nan
        R_ABC = res_dict[key]["R_ABC"][0] / \
            3 if res_dict[key]["R_ABC"][0] != 0 else np.nan

        resistance_list.append(R_A)
        resistance_list.append(R_B)
        resistance_list.append(R_C)
        resistance_list.append(R_AB)
        resistance_list.append(R_BC)
        resistance_list.append(R_ABC)

    plt.hist(resistance_list, bins=np.linspace(4.5, 7.5, 13), edgecolor="k")
    plt.grid(axis="y")
    plt.xlabel(r"Restistance of channel, $R$ [ $\Omega $ ]")
    plt.ylabel(r"Number in bin, $N$ [ - ]")


def hist_plot_double():

    resistance_list1 = []
    resistance_list2 = []
    for key in used_keys:
        R_A = res_dict[key]["R_A"][0] if res_dict[key]["R_A"][0] != 0 else np.nan
        R_B = res_dict[key]["R_B"][0] if res_dict[key]["R_B"][0] != 0 else np.nan
        R_C = res_dict[key]["R_C"][0] if res_dict[key]["R_C"][0] != 0 else np.nan
        R_AB = res_dict[key]["R_AB"][0] / \
            2 if res_dict[key]["R_AB"][0] != 0 else np.nan
        R_BC = res_dict[key]["R_BC"][0] / \
            2 if res_dict[key]["R_BC"][0] != 0 else np.nan
        R_ABC = res_dict[key]["R_ABC"][0] / \
            3 if res_dict[key]["R_ABC"][0] != 0 else np.nan

        resistance_list1.append(R_A)
        resistance_list1.append(R_B)
        resistance_list1.append(R_C)

        resistance_list2.append(R_A)
        resistance_list2.append(R_B)
        resistance_list2.append(R_C)
        resistance_list2.append(R_AB)
        resistance_list2.append(R_BC)
        resistance_list2.append(R_ABC)

    plt.subplots(1, 2, layout="constrained", figsize=(
                 9, 4.5), sharex=True, sharey=True)

    plt.subplot(1, 2, 1)
    plt.hist(resistance_list1, bins=np.linspace(4.5, 7.5, 13), edgecolor="k")
    plt.grid(axis="y")
    plt.xlabel(r"Restistance of channel, $R$ [ $\Omega $ ]")
    plt.ylabel(r"Number in bin, $N$ [ - ]")

    plt.subplot(1, 2, 2)
    plt.hist(resistance_list2, bins=np.linspace(4.5, 7.5, 13), edgecolor="k")
    plt.grid(axis="y")
    plt.xlabel(r"Restistance of channel, $R$ [ $\Omega $ ]")
    plt.ylabel(r"Number in bin, $N$ [ - ]")

    plt.show()


def plot_A_B_C():
    X_axis = ["A", "B", "C"]
    for key in used_keys:
        R_A = res_dict[key]["R_A"][0] if res_dict[key]["R_A"][0] != 0 else np.nan
        R_B = res_dict[key]["R_B"][0] if res_dict[key]["R_B"][0] != 0 else np.nan
        R_C = res_dict[key]["R_C"][0] if res_dict[key]["R_C"][0] != 0 else np.nan

        y_axis = [R_A, R_B, R_C]
        plt.scatter(range(len(y_axis)), y_axis, s=10, label=key)

    plt.xticks(range(len(X_axis)), X_axis, size='small')
    plt.legend(loc="upper left", prop={'size': 8})
    plt.grid(axis="y")
    plt.xlabel("Channel of structure")
    plt.ylabel(r"Resistance of channel, $R$ [ $\Omega$ ]")
    plt.show()


with open(r"c:\users\koxal\desktop\school\year 3\mpd\quick_folder\Electrical_data.json") as f:
    data_dict = json.load(f)

used_keys = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
             "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]

res_dict = calc_mean_and_std(used_keys)


def difference_plot():
    X_axis = ["AB-(A+B)", "BC-(B+C)", "ABC-(A+B+C)"]

    for_hist = []
    plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))
    plt.subplot(1, 2, 1)
    for key in used_keys:

        if key == "W2Al6b" or key == "W2Al8b":
            continue
        else:
            A = res_dict[key]["R_A"][0] if res_dict[key]["R_A"][0] != 0 else np.nan
            B = res_dict[key]["R_B"][0] if res_dict[key]["R_B"][0] != 0 else np.nan
            C = res_dict[key]["R_C"][0] if res_dict[key]["R_C"][0] != 0 else np.nan
            AB = res_dict[key]["R_AB"][0] if res_dict[key]["R_AB"][0] != 0 else np.nan
            BC = res_dict[key]["R_BC"][0] if res_dict[key]["R_BC"][0] != 0 else np.nan
            ABC = res_dict[key]["R_ABC"][0] if res_dict[key]["R_ABC"][0] != 0 else np.nan

            # Mean = (A+B+C)/3

            yaxis = [(AB - (A+B)), (BC - (B+C)), (ABC - (A+B+C))]

            for_hist.append((AB - (A+B)))
            for_hist.append((BC - (B+C)))
            for_hist.append((ABC - (A+B+C))/2)

            plt.scatter(X_axis, yaxis, label=key)

    plt.grid()
    plt.legend(prop={'size': 10})
    plt.xticks(range(len(X_axis)), X_axis)
    plt.ylabel("Difference in resistance, $\Delta R$ [$\Omega $]")
    plt.xlabel("Channels permutation [ - ]")

    plt.subplot(1, 2, 2)
    plt.hist(for_hist, edgecolor="k")
    plt.xlabel("Difference in resistance, $\Delta R$ [$\Omega $]")
    plt.ylabel(r"Number in bin, $N$ [ - ]")
    plt.grid()
    plt.show()


hist_plot_double()
