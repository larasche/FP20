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
idark200 = np.loadtxt("Daten/abgedunkelt_200ms.DAT", skiprows=17)
idark300 = np.loadtxt("Daten/abgedunkelt_300ms.DAT", skiprows=17)
idark150 = idark300/2

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

i0_darkcorrected = I0_measurement[:, 1] - idark200[:, 1]

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

i0_ready = i0_darkcorrected[wavemin: wavemax]


# calculate log(I0_ready/I_ready)

i_log = {}

for key in i_ready:
    i_log[key] = np.log(i0_ready/i_ready[key])



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

finalcross = intercross(wavelen)  # finalcross = cross section for the right wavelength

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

SC = []
angel = []
for key in fit_SC:
    SC.append(float(fit_SC[key][0]))
    angel.append(int(key))


plt.plot(angel, SC, ".")
plt.show()
