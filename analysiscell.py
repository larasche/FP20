#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:42:36 2021

@author: larasche
"""

import numpy as np
import os.path
import os

# reads only one file
directory = "Daten"
# fname = "mit_Zelle_200ms_58.DAT"
fname_full = os.path.join(directory, fname)
print(fname_full)
data = np.loadtxt(fname_full, skiprows=17)
print(data)

# trys to read all files

filenames = os.listdir('Daten')
print(filenames)
for fname in filenames:
    print(fname)
    directory = "Daten"
    fname_full = os.path.join(directory, fname)
    data = np.loadtxt(fname_full, skiprows=17)
    fname = [data]

# new try
withcell = []
for ii in filenames:
    if ii == np.join("mit_Zelle_200ms_"+ii+".DAT"):
        print(ii)


# reads the dark measurement
idark200 = np.loadtxt("Daten/abgedunkelt_200ms.DAT", skiprows=17)
idark300 = np.loadtxt("Daten/abgedunkelt_300ms.DAT", skiprows=17)
idark350 = np.loadtxt("Daten/abgedunkelt_350ms.DAT", skiprows=17)
idark400 = np.loadtxt("Daten/abgedunkelt_400ms.DAT", skiprows=17)
idark500 = np.loadtxt("Daten/abgedunkelt_500ms.DAT", skiprows=17)

# reads all mesurements with cell and different times:
filenames = os.listdir('Daten')


for ii in filenames:
    for nn in range(0,60):
        if ii == "mit_Zelle_200ms_" + str(nn) + ".DAT":

        if ii == "mit_Zelle_300ms_" + str(nn) + ".DAT":
            print(ii)
        if ii == "mit_Zelle_350ms_" + str(nn) + ".DAT":
            print(ii)
        if ii == "mit_Zelle_400ms_" + str(nn) + ".DAT":
            print(ii)
        if ii == "mit_Zelle_500ms_" + str(nn) + ".DAT":
            print(ii)

name = "mit_Zelle_200ms_"
ii = str(17)
fullname = name+ii
print(fullname)

