# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:52:42 2026

@author: koxal
"""
import numpy as np
import cv2

names = ["At", "Bt", "Ct", "Ab", "Bb", "Cb"]
folder = r"C:\Users\koxal\Desktop\school\year 3\MPD\data\pictures\SEM"

wafer_keys = []
channel_keys = []

pic_dict = dict()
for n in range(6, 10):
    wafer = f"w2al{n}"
    wafer_dict = dict()
    for name in names:
        img = cv2.imread(rf"{folder}\{wafer}_{name}.jpg", cv2.IMREAD_GRAYSCALE)[
            840:863, 550:750]
        wafer_dict.update({f"{name}": img})
        slc = img[12, :]
        width_in_pixels = np.sum(slc == 255, axis=0)
        print(f"{wafer}_{name} bar width = {width_in_pixels}")
    pic_dict.update({f"{wafer}": wafer_dict})
