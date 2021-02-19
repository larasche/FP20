#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:42:36 2021

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


# reads the time
filenames = os.listdir('Daten')


def time(filename):
    """Calculates the passed time since midnight (00:00:00)
    Args:
        filename: path to the file as string

    Returns:
        sectime: seconds since midnight
    """
    f = open("Daten/"+filename, "r")
    time = f.readlines()[1]  # time is stored in row 2
    ntime = time.split(" ")
    mtime = ntime[3].split(":")
    sectime = 3600*int(mtime[0]) + 60*int(mtime[1]) + int(mtime[2])
    f.close()
    return sectime


# start time in seconds since midnigth
stat_t = time("mit_Zelle_500ms_1.DAT")

# time since the first measurement
seconds_since_start = {}
for ii in filenames:
    for nn in range(1, 60):
        if ii == "mit_Zelle_200ms_"+str(nn)+".DAT":
            seconds_since_start[nn] = time(ii) - stat_t
        if ii == "mit_Zelle_300ms_"+str(nn)+".DAT":
            seconds_since_start[nn] = time(ii) - stat_t
        if ii == "mit_Zelle_350ms_"+str(nn)+".DAT":
            seconds_since_start[nn] = time(ii) - stat_t
        if ii == "mit_Zelle_400ms_"+str(nn)+".DAT":
            seconds_since_start[nn] = time(ii) - stat_t
        if ii == "mit_Zelle_500ms_"+str(nn)+".DAT":
            seconds_since_start[nn] = time(ii) - stat_t

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


# aplly the fitting window to the measurements
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


# interpolate the differential cross section to the measurement wavelengths
waveair = NO2cross[:, 0]
diffNO2 = NO2cross[:, 1]
intercross = interp1d(waveair, diffNO2)  # interpolates the FUNKTION intercross

# fit the cross section to mesurement wavelength (wavelen)

finalcross = intercross(wavelen)  # finalcross = cross section for the right wavelength

nfinalcross = np.reshape(finalcross, (367, 1))


# ##########################(this is possible right)#####################

# also a new try because i'm stupid (row, column)

idiffnew = {}
for key in i_logdiff:
    for nn in range(0, 60):
        if key == str(nn):
            idiffnew[key] = np.reshape(i_logdiff[key], (367, -1))

test = nl.lstsq(nfinalcross, idiffnew["5"])

fit_SC = {}
for key in idiffnew:
    for nn in range(0, 60):
        if key == str(nn):
            fit_SC[key] = nl.lstsq(nfinalcross, idiffnew[key])


# plot plot plot :)


specialtime = seconds_since_start[1]
plt.plot(wavelen, i_logdiff["1"], "-", color="red",
         label="measurement")
plt.plot(wavelen, fit_SC["1"][0]*nfinalcross, "-", color="blue",
         label="scaled NO2 reference")
plt.xlabel("Wavelength (nm)")
plt.ylabel("differential optical depth")
plt.legend()
plt.title("Seconds since start: 0s")
plt.show
plt.savefig("cell_time_0s.pdf")

specialtime = seconds_since_start[5]
plt.plot(wavelen, i_logdiff["5"], "-", color="red",
         label="measurement")
plt.plot(wavelen, fit_SC["5"][0]*nfinalcross, "-", color="blue",
         label="scaled NO2 reference")
plt.xlabel("Wavelength (nm)")
plt.ylabel("differential optical depth")
plt.legend()
plt.title("Seconds since start: 471s")
plt.show
plt.savefig("cell_time_471s.pdf")

specialtime = seconds_since_start[59]
plt.plot(wavelen, i_logdiff["59"], "-", color="red",
         label="measurement")
plt.plot(wavelen, fit_SC["59"][0]*nfinalcross, "-", color="blue",
         label="scaled NO2 reference")
plt.xlabel("Wavelength (nm)")
plt.ylabel("differential optical depth")
plt.legend()
plt.title("Seconds since start: 5786s")
plt.show
plt.savefig("cell_time_5786s.pdf")


# calculate the concentration of NO2 in the cell


SClist = []
timelist = []
for key in seconds_since_start:
    for key2 in fit_SC:
        if str(key) == key2:
            timelist.append(seconds_since_start[key])
            SClist.append(float(fit_SC[key2][0]))

cell_length = float(10)
concentration = []
for ii in range(0, len(SClist)):
    concentration.append(SClist[ii]/cell_length)


plt.plot(timelist, concentration, ".")
plt.xlabel("seconds since first measurement")
plt.ylabel("concentration [molec/cm³]")
plt.title("Concentration of NO2 in the cell")
plt.savefig("cell_concentration.pdf")
plt.show()
