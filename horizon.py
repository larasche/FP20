#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 17:02:12 2021

@author: larasche
"""

import numpy as np
import os.path
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy.linalg as nl


# reads the differential cross section for NO_2

NO2cross = np.loadtxt("Daten/NO2_DiffXSection.dat", skiprows=6)


# reads the dark measurement in an array

idark500 = np.loadtxt("Daten/abgedunkelt_500ms.DAT", skiprows=17)

# reads the angular measurements
filenames = os.listdir('Daten')

i_measurements = {}
for ii in filenames:
    for nn in range(0, 15):
        if ii == "Spektrum_" + str(nn) + "grad.DAT":
            i_measurements[str(nn)] = np.loadtxt("Daten/"+ii, skiprows=17)

I0_measurement = np.loadtxt("Daten/Spektrum_90grad.DAT", skiprows=17)

# substract the dark measurements
i_darkcorrected = {}
for key in i_measurements:
    for nn in range(0, 15):
        if key == str(nn):
            i_darkcorrected[key] = i_measurements[key][:, 1] - idark500[:, 1]


# apply wavelength calibration
a0 = float(429.494)
a1 = float(93.112)
a2 = float(-6.050)
wavelenscale = np.ones([1024])


def wave(ii):
    aa = a0 + a1*((ii-1)/(1023)) + a2*((ii-1)/(1023))**2
    return aa


wavelenscale = wave(idark500[:, 0])


# choose the fitting window: 432.5-465nm
wavemin = abs(wavelenscale - 432.5).argmin()
wavemax = abs(wavelenscale - 465).argmin()
wavelen = wavelenscale[wavemin: wavemax]


# aplly the fitting window to the measurements
# alternative (without the string like "ohne_Zelle_200ms_")
i_ready = {}

for key in i_darkcorrected:
    for nn in range(0, 15):
        if key == str(nn):
            i_ready[key] = i_darkcorrected[key][wavemin: wavemax]
