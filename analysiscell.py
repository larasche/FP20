#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:42:36 2021

@author: larasche
"""

import numpy as np
import os.path
import os


# sort the data by time
filenames = os.listdir('Daten')


# reads the dark measurement in an array
idark200 = np.loadtxt("Daten/abgedunkelt_200ms.DAT", skiprows=17)
idark300 = np.loadtxt("Daten/abgedunkelt_300ms.DAT", skiprows=17)
idark350 = np.loadtxt("Daten/abgedunkelt_350ms.DAT", skiprows=17)
idark400 = np.loadtxt("Daten/abgedunkelt_400ms.DAT", skiprows=17)
idark500 = np.loadtxt("Daten/abgedunkelt_500ms.DAT", skiprows=17)

# reads all mesurements with cell and different times:
filenames = os.listdir('Daten')

i_withcell = {}
i_withoutcell = {}

for ii in filenames:
    for nn in range(0, 60):
        if ii == "mit_Zelle_200ms_" + str(nn) + ".DAT":
            name = "mit_Zelle_200ms_" + str(nn)
            i_withcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "mit_Zelle_300ms_" + str(nn) + ".DAT":
            name = "mit_Zelle_300ms_" + str(nn)
            i_withcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "mit_Zelle_350ms_" + str(nn) + ".DAT":
            name = "mit_Zelle_350ms_" + str(nn)
            i_withcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "mit_Zelle_400ms_" + str(nn) + ".DAT":
            name = "mit_Zelle_400ms_" + str(nn)
            i_withcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "mit_Zelle_500ms_" + str(nn) + ".DAT":
            name = "mit_Zelle_500ms_" + str(nn)
            i_withcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "ohne_Zelle_200ms_" + str(nn) + ".DAT":
            name = "ohne_Zelle_200ms_" + str(nn)
            i_withoutcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "ohne_Zelle_300ms_" + str(nn) + ".DAT":
            name = "ohne_Zelle_300ms_" + str(nn)
            i_withoutcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "ohne_Zelle_350ms_" + str(nn) + ".DAT":
            name = "ohne_Zelle_350ms_" + str(nn)
            i_withoutcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "ohne_Zelle_400ms_" + str(nn) + ".DAT":
            name = "ohne_Zelle_400ms_" + str(nn)
            i_withoutcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)
        if ii == "ohne_Zelle_500ms_" + str(nn) + ".DAT":
            name = "ohne_Zelle_500ms_" + str(nn)
            i_withoutcell[name] = np.loadtxt("Daten/"+ii, skiprows=17)

# substract the dark measurements
i_darkcorrected = {}
i0_darkcorrected = {}
for key in i_withcell:
    for nn in range(0, 60):
        if key == "mit_Zelle_200ms_" + str(nn):
            name = "mit_Zelle_200ms_" + str(nn)
            i_darkcorrected[name] = i_withcell[key][:, 1] - idark200[:, 1]
        if key == "mit_Zelle_300ms_" + str(nn):
            name = "mit_Zelle_300ms_" + str(nn)
            i_darkcorrected[name] = i_withcell[key][:, 1] - idark300[:, 1]
        if key == "mit_Zelle_350ms_" + str(nn):
            name = "mit_Zelle_350ms_" + str(nn)
            i_darkcorrected[name] = i_withcell[key][:, 1] - idark350[:, 1]
        if key == "mit_Zelle_400ms_" + str(nn):
            name = "mit_Zelle_400ms_" + str(nn)
            i_darkcorrected[name] = i_withcell[key][:, 1] - idark400[:, 1]
        if key == "mit_Zelle_500ms_" + str(nn):
            name = "mit_Zelle_500ms_" + str(nn)
            i_darkcorrected[name] = i_withcell[key][:, 1] - idark500[:, 1]
for key in i_withoutcell:
    for nn in range(0, 60):
        if key == "ohne_Zelle_200ms_" + str(nn):
            name = "ohne_Zelle_200ms_" + str(nn)
            i0_darkcorrected[name] = i_withoutcell[key][:, 1] - idark200[:, 1]
        if key == "ohne_Zelle_300ms_" + str(nn):
            name = "ohne_Zelle_300ms_" + str(nn)
            i0_darkcorrected[name] = i_withoutcell[key][:, 1] - idark300[:, 1]
        if key == "ohne_Zelle_350ms_" + str(nn):
            name = "ohne_Zelle_350ms_" + str(nn)
            i0_darkcorrected[name] = i_withoutcell[key][:, 1] - idark350[:, 1]
        if key == "ohne_Zelle_400ms_" + str(nn):
            name = "ohne_Zelle_400ms_" + str(nn)
            i0_darkcorrected[name] = i_withoutcell[key][:, 1] - idark400[:, 1]
        if key == "ohne_Zelle_500ms_" + str(nn):
            name = "ohne_Zelle_500ms_" + str(nn)
            i0_darkcorrected[name] = i_withoutcell[key][:, 1] - idark500[:, 1]

# apply wavelength calibration
a0 = float(429.494)
a1 = float(93.112)
a2 = float(-6.050)
wavelenscale = np.ones([1024])


def wave(ii):
    aa = a0 + a1*((ii-1)/(1023)) + a2*((ii-1)/(1023))**2
    return aa


wavelenscale = wave(idark200[:, 0])

# choose the fitting window: 432.5-465nm
wavemin = abs(wavelenscale - 432.5).argmin()
wavemax = abs(wavelenscale - 465).argmin()
wavelen = wavelenscale[wavemin: wavemax]

# apply the fitting window to the measurements
i_ready = {}
i0_ready = {}
for key in i_darkcorrected:
    for nn in range(0, 60):
        if key == "mit_Zelle_200ms_" + str(nn):
            name = "mit_Zelle_200ms_" + str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_300ms_" + str(nn):
            name = "mit_Zelle_300ms_" + str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_350ms_" + str(nn):
            name = "mit_Zelle_350ms_" + str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_400ms_" + str(nn):
            name = "mit_Zelle_400ms_" + str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_500ms_" + str(nn):
            name = "mit_Zelle_500ms_" + str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
for key in i0_darkcorrected:
    for nn in range(0, 60):
        if key == "ohne_Zelle_200ms_" + str(nn):
            name = "ohne_Zelle_200ms_" + str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_300ms_" + str(nn):
            name = "ohne_Zelle_300ms_" + str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_350ms_" + str(nn):
            name = "ohne_Zelle_350ms_" + str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_400ms_" + str(nn):
            name = "ohne_Zelle_400ms_" + str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_500ms_" + str(nn):
            name = "ohne_Zelle_500ms_" + str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]


# calculate ln(I0/I)
