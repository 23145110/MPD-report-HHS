# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 12:47:52 2026

@author: koxal
"""
import json
import time
import matplotlib.pyplot as plt
import numpy as np
import xlwings as xl


def res_err_per_channel():

    def R_err(I, V):
        I_err = ((0.05)/100) * I + 3*(1e-6)
        V_err = ((0.02)/100) * I + 4*(100e-6)

        dRdV = 1/I
        dRdI = - V/(I**2)

        R_err = np.sqrt((V_err*dRdV)**2+(I_err*dRdI)**2)

        return R_err

    filename = r"C:\Users\koxal\Desktop\school\year 3\MPD\quick_folder\electrical_data.xlsx"
    app = xl.App(visible=False)

    wb = app.books.open(filename)

    used_keys = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
                 "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]

    sheet_names = ["W2Al6_up", "W2Al6_down", "W2Al7_up", "W2Al7_down",
                   "W2Al8_up", "W2Al8_down", "W2Al9_up", "W2Al9_down"]

    res_err_dict = dict()
    for n in range(len(used_keys)):
        key1 = used_keys[n]
        key2 = sheet_names[n]

        I = np.array(wb.sheets[key2].range("D3:D6").value)
        V = np.array(wb.sheets[key2].range("E3:E6").value)
        A_errs = R_err(I/1000, V) if I[0] != None else np.nan

        I = np.array(wb.sheets[key2].range("D11:D14").value)
        V = np.array(wb.sheets[key2].range("E11:E14").value)
        B_errs = R_err(I/1000, V) if I[0] != None else np.nan

        I = np.array(wb.sheets[key2].range("D19:D22").value)
        V = np.array(wb.sheets[key2].range("E19:E22").value)
        C_errs = R_err(I/1000, V) if I[0] != None else np.nan

        I = np.array(wb.sheets[key2].range("J3:J6").value)
        V = np.array(wb.sheets[key2].range("K3:K6").value)
        AB_errs = R_err(I/1000, V) if I[0] != None else np.nan

        I = np.array(wb.sheets[key2].range("J11:J14").value)
        V = np.array(wb.sheets[key2].range("K11:K14").value)
        BC_errs = R_err(I/1000, V) if I[0] != None else np.nan

        I = np.array(wb.sheets[key2].range("J19:J22").value)
        V = np.array(wb.sheets[key2].range("K19:K22").value)
        ABC_errs = R_err(I/1000, V) if I[0] != None else np.nan

        this_dict = {"A": A_errs, "B": B_errs, "C": C_errs, "AB": AB_errs,
                     "BC": BC_errs, "ABC": ABC_errs}

        res_err_dict.update({key1: this_dict})

    return res_err_dict


def err_total(R, w, h, l, dR, dw, dh):
    dpdR = (dR * w * h) / (l)
    dpdw = (dw * R * h) / (l)
    dpdh = (dh * R * w) / (l)

    Delta_p = np.sqrt(dpdR**2 + dpdh**2 + dpdw**2)

    return Delta_p


with open(r"Cropped_height_data.json") as f:
    height_dict = json.load(f)

with open(r"Electrical_data.json") as f:
    resistance_dict = json.load(f)

width = 200  # micrometer

err_width_dict = {"W2Al6t": 1.997419096379057e-06,
                  "W2Al6b": 1.5322254223116608e-05,
                  "W2Al7t": 2.0772450906984876e-06,
                  "W2Al7b": 2.713623532418044e-06,
                  "W2Al8t": 2.9259834410148985e-06,
                  "W2Al8b": 4.811979939049166e-06,
                  "W2Al9t": 1.0004650692128713e-05,
                  "W2Al9b": 2.080853975615475e-06}

length = 2000  # micrometer

average_height_dict = {}

list_for_x = []

for wafer_key in height_dict:
    average_heights_on_wafer = {}
    wafer = height_dict[wafer_key]

    list_for_plot = []

    for struct_key in wafer:
        struct = wafer[struct_key]
        if wafer_key == "W2Al7t" and (struct_key == "Pad8" or struct_key == "Pad5"):
            pass
        else:
            pass

        x = np.array(struct["x"])
        z = np.array(struct["z"])

        mean_height = np.average(z)

        err = np.std(z)
        list_for_plot.append(mean_height)
        # plt.scatter(mean_height, struct_key)

        average_heights_on_wafer.update({struct_key: (mean_height)})

    # plt.title(wafer_key)
    # plt.grid()
    # plt.show()
    standard_deviation_of_mean = np.std(
        list_for_plot)/np.sqrt(len(list_for_plot))
    # print(standard_deviation_of_mean)
    list_for_x.append(np.mean(list_for_plot))

    average_height_dict.update(
        {wafer_key: (np.mean(list_for_plot), standard_deviation_of_mean)})

# for key in average_height_dict:
    # plt.scatter(average_height_dict[key], key)

# plt.grid()
# plt.show()

specific_resistance_dict = dict()


err_resistances = res_err_per_channel()
for_hyst = []

for wafer_key in average_height_dict:
    sr_wafer = dict()

    for channel in resistance_dict[wafer_key]:

        if None not in resistance_dict[wafer_key][channel]:
            # print(resistance_dict[wafer_key][channel])
            length_1_channel = 2000E-6  # micrometer
            err_length = 0  # assumed to be insignificant

            if channel in ["A", "B", "C"]:
                l = length_1_channel
            elif channel in ["AB", "BC"]:
                l = 2 * length_1_channel
            elif channel in ["ABC"]:
                l = 3 * length_1_channel
            else:
                print("fuck")

            R = np.mean(resistance_dict[wafer_key][channel])
            err_R = np.mean(err_resistances[wafer_key][channel])

            width = 200E-6  # micrometer
            err_width = err_width_dict[wafer_key]

            height = average_height_dict[wafer_key][0]/1E9
            err_height = average_height_dict[wafer_key][1]/1E9
            sr = R*width*height / l
            err_sr = err_total(R, width, height, l,
                               err_R, err_width, err_height)
            # print(err_sr)
            sr_wafer.update({channel: (sr, err_sr)})
            for_hyst.append(sr)

        else:
            pass
    specific_resistance_dict.update({wafer_key: sr_wafer})


plt.hist(for_hyst, edgecolor="k", bins=9)
plt.grid(axis="y")
plt.xlabel(r"Specific resistance channel, $\rho$ [ $\Omega $ ]")
plt.ylabel(r"Number in bin, $N$ [ - ]")
plt.show()


def hist_plots():

    used_keys = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
                 "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]

    resistance_list = []

    for key in used_keys:
        R_A = np.mean(
            resistance_dict[key]["A"]) if resistance_dict[key]["A"][0] != None else np.nan
        R_B = np.mean(
            resistance_dict[key]["B"]) if resistance_dict[key]["B"][0] != None else np.nan
        R_C = np.mean(
            resistance_dict[key]["C"]) if resistance_dict[key]["C"][0] != None else np.nan
        R_AB = np.mean(
            resistance_dict[key]["AB"])/2 if resistance_dict[key]["AB"][0] != None else np.nan
        R_BC = np.mean(
            resistance_dict[key]["BC"])/2 if resistance_dict[key]["BC"][0] != None else np.nan
        R_ABC = np.mean(
            resistance_dict[key]["ABC"])/3 if resistance_dict[key]["ABC"][0] != None else np.nan

        resistance_list.append(R_A)
        resistance_list.append(R_B)
        resistance_list.append(R_C)
        resistance_list.append(R_AB)
        resistance_list.append(R_BC)
        resistance_list.append(R_ABC)

    plt.subplots(1, 2, layout="constrained", figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(resistance_list, bins=np.linspace(4.5, 7.5, 13), edgecolor="k")
    plt.grid(axis="y")
    plt.xlabel(r"Restistance of channel, $R$ [ $\Omega $ ]")
    plt.ylabel(r"Number in bin, $N$ [ - ]")

    plt.subplot(1, 2, 2)
    plt.hist(for_hyst, bins=9, edgecolor="k")
    plt.grid(axis="y")
    plt.xlabel(r"resistivity of channel, $\rho$ [ $\Omega m$ ]")
    plt.ylabel(r"Number in bin, $N$ [ - ]")

    plt.show()

    # print(np.std(for_hyst))
    # print(~np.isnan(resistance_list))
    res_lst = np.array(resistance_list)[~np.isnan(resistance_list)]
    print(f"min: {min(res_lst)}, max: {max(res_lst)}")
    # print(np.std(res_lst))


# hist_plots()


# used_keys = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
#              "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]

# plot_res = []
# plot_height = []

# for key in used_keys:
#     R_A = np.mean(
#         resistance_dict[key]["A"]) if resistance_dict[key]["A"][0] != None else np.nan
#     R_B = np.mean(
#         resistance_dict[key]["B"]) if resistance_dict[key]["B"][0] != None else np.nan
#     R_C = np.mean(
#         resistance_dict[key]["C"]) if resistance_dict[key]["C"][0] != None else np.nan
#     R_AB = np.mean(
#         resistance_dict[key]["AB"])/2 if resistance_dict[key]["AB"][0] != None else np.nan
#     R_BC = np.mean(
#         resistance_dict[key]["BC"])/2 if resistance_dict[key]["BC"][0] != None else np.nan
#     R_ABC = np.mean(
#         resistance_dict[key]["ABC"])/3 if resistance_dict[key]["ABC"][0] != None else np.nan

#     plot_height.append(average_height_dict[key][0])
#     plot_res.append((R_A+R_B+R_C+(R_AB/2)+(R_BC/2)+(R_ABC/3))/6)


# plt.scatter(plot_height, plot_res)
# plt.grid()
# plt.show()
