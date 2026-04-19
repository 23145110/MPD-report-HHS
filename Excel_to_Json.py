# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import xlwings as xl
import json

filename = r"C:\Users\23145110\Documents\electrical_data.xlsx"

app = xl.App(visible=False)

wb = app.books.open(filename)

used_keys = ["W2Al6_up", "W2Al6_down", "W2Al7_up", "W2Al7_down",
             "W2Al8_up", "W2Al8_down", "W2Al9_up", "W2Al9_down"]

used_keys2 = ["W2Al6t", "W2Al6b", "W2Al7t", "W2Al7b",
             "W2Al8t", "W2Al8b", "W2Al9t", "W2Al9b"]

data = dict()
for n in range(len(used_keys)):
    key1 = used_keys[n]
    key2 = used_keys2[n]
    
    A_vals = wb.sheets[key1].range("F3:F6").value
    B_vals = wb.sheets[key1].range("F11:F14").value
    C_vals = wb.sheets[key1].range("F19:F22").value
    
    AB_vals = wb.sheets[key1].range("L3:L6").value
    BC_vals = wb.sheets[key1].range("L11:L14").value
    
    ABC_vals = wb.sheets[key1].range("L19:L22").value
    
    this_dict = {"A":A_vals, "B":B_vals, "C":C_vals, "AB":AB_vals,
                 "BC":BC_vals, "ABC":ABC_vals}
    
    data.update({key2:this_dict})
    
with open(r"C:\Users\23145110\Documents\Electrical_data.json","w") as f:
    json.dump(data, f)

