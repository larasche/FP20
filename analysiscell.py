#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:42:36 2021

@author: larasche
"""

import numpy as np
import os.path
import os


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
#i_ready = {}
#i0_ready = {}
#for key in i_darkcorrected:
 #   for nn in range(0, 60):
  #      if key == "mit_Zelle_200ms_" + str(nn):
   #         name = "mit_Zelle_200ms_" + str(nn)
   #         i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
    #    if key == "mit_Zelle_300ms_" + str(nn):
    #        name = "mit_Zelle_300ms_" + str(nn)
    #        i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
    #    if key == "mit_Zelle_350ms_" + str(nn):
    #        name = "mit_Zelle_350ms_" + str(nn)
     #       i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
     ##   if key == "mit_Zelle_400ms_" + str(nn):
     #       name = "mit_Zelle_400ms_" + str(nn)
    #        i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
    #    if key == "mit_Zelle_500ms_" + str(nn):
#            name = "mit_Zelle_500ms_" + str(nn)
#            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
#for key in i0_darkcorrected:
 #   for nn in range(0, 60):
   #     if key == "ohne_Zelle_200ms_" + str(nn):
  #          name = "ohne_Zelle_200ms_" + str(nn)
     #       i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
    #    if key == "ohne_Zelle_300ms_" + str(nn):
 #           name = "ohne_Zelle_300ms_" + str(nn)
  #          i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
 #       if key == "ohne_Zelle_350ms_" + str(nn):
 #           name = "ohne_Zelle_350ms_" + str(nn)
 #           i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
 #       if key == "ohne_Zelle_400ms_" + str(nn):
 #           name = "ohne_Zelle_400ms_" + str(nn)
#            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
#        if key == "ohne_Zelle_500ms_" + str(nn):
 #           name = "ohne_Zelle_500ms_" + str(nn)
 #           i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]


# calculate log(I0_ready/I_ready)

# i_log = {}

# alternative (without the string like "ohne_Zelle_200ms_")
i_ready = {}
i0_ready = {}
for key in i_darkcorrected:
    for nn in range(0, 60):
        if key == "mit_Zelle_200ms_" + str(nn):
            name = str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_300ms_" + str(nn):
            name = str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_350ms_" + str(nn):
            name = str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_400ms_" + str(nn):
            name = str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
        if key == "mit_Zelle_500ms_" + str(nn):
            name = str(nn)
            i_ready[name] = i_darkcorrected[key][wavemin: wavemax]
for key in i0_darkcorrected:
    for nn in range(0, 60):
        if key == "ohne_Zelle_200ms_" + str(nn):
            name = str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_300ms_" + str(nn):
            name = str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_350ms_" + str(nn):
            name = str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_400ms_" + str(nn):
            name = str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]
        if key == "ohne_Zelle_500ms_" + str(nn):
            name = str(nn)
            i0_ready[name] = i0_darkcorrected[key][wavemin: wavemax]


# calculate log(I0_ready/I_ready)

i_log = {}

for key in i_ready:
    for key2 in i0_ready:
        if key == key2:
            i_log[key] = np.log(i0_ready[key]/i_ready[key2])


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


# sort the data by time
filenames = os.listdir('Daten')


def time(filename):
    f = open(filename, "r")
    time = f.readlines()[1]  # time is stored in row 2
    ntime = time.split(" ")
    mtime = ntime[3].split(":")
    # seconds since midnight (00:00:00:00)
    sectime = 3600*int(mtime[0]) + 60*int(mtime[1]) + int(mtime[2])
    f.close()
    return sectime


test = time("Daten/mit_Zelle_200ms_56.DAT")


# interpolate the differential cross section to the measurements cross section
