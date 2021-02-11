#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:32:14 2021

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
idark200 = np.loadtxt("Daten/abgedunkelt_200ms.DAT", skiprows=17)
idark300 = np.loadtxt("Daten/abgedunkelt_300ms.DAT", skiprows=17)
idark350 = np.loadtxt("Daten/abgedunkelt_350ms.DAT", skiprows=17)
idark400 = np.loadtxt("Daten/abgedunkelt_400ms.DAT", skiprows=17)
idark500 = np.loadtxt("Daten/abgedunkelt_500ms.DAT", skiprows=17)

# reads all mesurements with cell and different times:
filenames = os.listdir('Daten')


i_withoutcell = {}

for ii in filenames:
    for nn in range(2, 60):
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

i0 = np.loadtxt("Daten/ohne_Zelle_500ms_1.DAT", skiprows=17)


# substract the dark measurements
i_darkcorrected = {}

for key in i_withoutcell:
    for nn in range(0, 60):
        if key == "ohne_Zelle_200ms_" + str(nn):
            name = str(nn)
            i_darkcorrected[name] = i_withoutcell[key][:, 1] - idark200[:, 1]
        if key == "ohne_Zelle_300ms_" + str(nn):
            name = str(nn)
            i_darkcorrected[name] = i_withoutcell[key][:, 1] - idark300[:, 1]
        if key == "ohne_Zelle_350ms_" + str(nn):
            name = str(nn)
            i_darkcorrected[name] = i_withoutcell[key][:, 1] - idark350[:, 1]
        if key == "ohne_Zelle_400ms_" + str(nn):
            name = str(nn)
            i_darkcorrected[name] = i_withoutcell[key][:, 1] - idark400[:, 1]
        if key == "ohne_Zelle_500ms_" + str(nn):
            name = str(nn)
            i_darkcorrected[name] = i_withoutcell[key][:, 1] - idark500[:, 1]

i0_darkcorrected = i0[:, 1] - idark500[:, 1]

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

# aplly the fitting window to the measurements

i_ready = {}
for key in i_darkcorrected:
    for nn in range(0, 60):
        if key == str(nn):
            name = str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]


i0_ready = i0_darkcorrected[wavemin: wavemax]

# calculate log(I0_ready/I_ready)

i_log = {}

for key in i_ready:
    for ii in range(2, 60):
        if key == str(ii):
            i_log[key] = np.log(i0_ready/i_ready[key])


# fit a polynomial of order 3 to i_log

def polynom3(a0, a1, a2, a3, x):
    """"calculates the polynom of order 3"""
    aa = a0*x**3 + a1*x**2 + a2*x + a3
    return aa


poly = {}
for key in i_log:
    fitparas = np.polyfit(wavelen, i_log[key], 3)
    poly[key] = polynom3(fitparas[0], fitparas[1], fitparas[2], fitparas[3], wavelen)


# substract the fitted polynomial from i_log to get the differential i_logdiff

i_logdiff = {}
for key in i_log:
    for key2 in poly:
        if key == key2:
            i_logdiff[key] = i_log[key] - poly[key2]


# interpolate the differential cross section to the measurement wavelengths
waveair = NO2cross[:, 0]
diffNO2 = NO2cross[:, 1]
intercross = interp1d(waveair, diffNO2)  # interpolates the FUNKTION intercross

# fit the cross section to mesurement wavelength (wavelen)

finalcross = intercross(wavelen)  # finalcross = cross section for the right
                                                # wavelength

nfinalcross = np.reshape(finalcross, (367, 1))


idiffnew = {}
for key in i_logdiff:
    for nn in range(0, 60):
        if key == str(nn):
            idiffnew[key] = np.reshape(i_logdiff[key], (367, -1))


fit_SC = {}
for key in idiffnew:
    for nn in range(0, 60):
        if key == str(nn):
            fit_SC[key] = nl.lstsq(nfinalcross, idiffnew[key])

plt.plot(wavelen, i_logdiff["5"], "-", color="red")
plt.plot(wavelen, fit_SC["5"][0]*nfinalcross, ".", color="blue")
plt.show
