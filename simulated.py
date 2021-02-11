#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:26:39 2021

@author: larasche
"""

import numpy as np
import os.path
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy.linalg as nl


# read the refernez cross sections:

refcross = {}

refcross["O3"] = np.loadtxt("Daten/O3_DIFFXSECTION.DAT", skiprows=6)
refcross["BrO"] = np.loadtxt("Daten/BRO_DIFFXSECTION.DAT", skiprows=6)
refcross["HCHO"] = np.loadtxt("Daten/HCHO_DIFFXSECTION.DAT", skiprows=6)

#read the simulated data at different angels (80° as i0 and 20° as i)

i_20 = np.loadtxt("Daten/TG_A_DATA_20.DAT", skiprows=6)
i_80 = np.loadtxt("Daten/TG_A_DATA_80.DAT", skiprows=6)


# this data must not be dark corrected
# therefor we can directly apply the fitting window

wavelenscale = i_20[:, 0]

wavemin = abs(wavelenscale - 336).argmin()
wavemax = abs(wavelenscale - 357).argmin()
wavelen = wavelenscale[wavemin: wavemax]

i0_ready = i_80[wavemin: wavemax]
i_ready = i_20[wavemin: wavemax]


# calculate log(I0_ready/I_ready)

i_log = np.log(i0_ready[:, 1]/i_ready[:, 1])

# fit a polynomial of order 3 to i_log


def polynom3(a0, a1, a2, a3, x):
    """"calculates the polynom of order 3"""
    aa = a0*x**3 + a1*x**2 + a2*x + a3
    return aa


fitparas = np.polyfit(wavelen, i_log, 3)
poly = polynom3(fitparas[0], fitparas[1], fitparas[2], fitparas[3], wavelen)

# substract the polynom

i_logdiff = i_log - poly

# interpolate the differential cross section to the measurement wavelengths

waveair = {}
cross = {}
intercross = {}
for key in refcross:
    waveair[key] = refcross[key][:, 0]
    cross[key] = refcross[key][:, 1]
    intercross[key] = interp1d(waveair[key], cross[key])

# fit the cross section to mesurement wavelength (wavelen)

finalcross = {}
nfinalcross = {}
for key in intercross:
    finalcross[key] = intercross[key](wavelen)  # finalcross = cross section for the right wavelength
    nfinalcross[key] = np.reshape(finalcross[key], (210, 1))


idiffnew = np.reshape(i_logdiff, (210, -1))

fit_SC = {}
for key in nfinalcross:
    fit_SC[key] = nl.lstsq(nfinalcross[key], idiffnew)

plt.plot(wavelen, i_logdiff, "-", color="red")
plt.plot(wavelen, fit_SC["O3"][0]*nfinalcross["O3"], ".", color="blue")
plt.show

plt.plot(wavelen, i_logdiff, "-", color="red")
plt.plot(wavelen, fit_SC["BrO"][0]*nfinalcross["BrO"], ".", color="blue")
plt.show

plt.plot(wavelen, i_logdiff, "-", color="red")
plt.plot(wavelen, fit_SC["HCHO"][0]*nfinalcross["HCHO"], ".", color="blue")
plt.show