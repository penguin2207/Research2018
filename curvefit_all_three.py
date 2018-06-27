#!/usr/bin/env python
import sys, os, ScopeTrace, pylandau, ScopeTrace
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
from scipy.optimize import curve_fit
from itertools import product
import csv
#-------------------------------------------------------------------------------
#loop through all files
mlp.rcParams['axes.linewidth'] = 2
jitter_stored = []
mpv_stored = []
eta_stored = []
A_stored = []
for file in sorted(os.listdir("/home/kpark1/Work/SLab/data_3/")) :
    
    with open('data_3/'+file, "r") as file1: 
        data= file1.read()
        print(str(file1) + ':\n')
    
# decode the scope trace
        trace = ScopeTrace.ScopeTrace(data,1)
# find baseline and jitter 
        baseline,jitter = trace.find_baseline_and_jitter(0,250)
        jitter_stored.append(jitter)
#set x and y
        inverted_yvalues = []
        for value in trace.yvalues:
            inverted_yvalue = -(value-baseline)
            inverted_yvalues.append(inverted_yvalue)
        x = np.array(trace.xvalues)
        y = np.array(inverted_yvalues)    
#x values at peaks
        y_array = np.array(y)
        idx = np.where(y_array == y_array.max())
#if multiple x values of the same max y values, select the first max
        idx = idx[0][0]
        x_values_peak = x[idx]

#GAUSSIAN
        mean = x_values_peak 
        a = max(y)
        g_par = []
        def gaus(x, a, x0, sigma):
            return a* np.exp(-(x-x0)**2/(2*sigma**2))
        def diff_sq_fn(parameter):
            return round(sum((y-gaus(x, *parameter))**2), 4)
        for sigma in range(0, 50):
            popt, pcov = curve_fit(gaus, x, y, p0 = [a,mean, sigma])
            if diff_sq_fn(popt) < .5:
                g_par.append(popt)
                break
            else:
                continue
        plt.plot(x, y, 'c', label = 'Oscilloscope Data')
        try:
            g_par = g_par[0]
            plt.plot(x, gaus(x, *g_par), 'r', label = 'Gaussian')
            plt.legend()
        except IndexError as message:
            print(message)
        
#LANDAU
        mpv = x_values_peak
        rmin= 1
        def diff_sq_fn(parameter):
            return round(sum((y-pylandau.landau(x, *parameter))**2), 4)
        try: 
            landau_par_rmin, pcov_rmin = curve_fit(pylandau.landau, x, y, p0= (mpv, rmin, rmin))
            array_1 = np.ndarray.tolist(np.around(landau_par_rmin, decimals = 3))
            param_list = [array_1]
            workinglandaupar = [array_1]
            initial_diff_sq = [diff_sq_fn(landau_par_rmin)]
        except RuntimeError as message:
            print(str(message) + ' for ' + str( file))
            continue
        except TypeError as message:
            print(str(message) + ' for ' + str(file))
            continue

      #only one best possible parameter with least diff_sq
        for eta, A in product(np.linspace(rmin, 25,5 ), np.linspace(rmin, 25, 5)):
            try:
                landau_par, pcov = curve_fit(pylandau.landau, x, y, p0= (mpv, eta,A))
                landau_par = np.ndarray.tolist(np.around(landau_par, decimals =3))
                diff= diff_sq_fn(landau_par)
                par = param_list[0]
                if initial_diff_sq[0] < .01:
                    break
                elif landau_par != par and diff < initial_diff_sq[0]:
                    param_list.append(landau_par)
                    
                    del workinglandaupar[0]
                    del initial_diff_sq[0]
                    initial_diff_sq.append(diff)
                    workinglandaupar.append(landau_par)
                    break
                else:
                    continue
            except RuntimeError as message:
                print(str(message)+ str(file))
                continue
            except TypeError as message:
                print(str(message) +'2nd'+ str(file))
            except ValueError as message:
                print(str(message) + str(file))
        workinglandaupar = workinglandaupar[0]     
        plt.plot(x, pylandau.landau(x, *workinglandaupar),linestyle = 'dashed',color = 'm', label = 'Landau')
        plt.legend()

#LANGAU
        mpv = x_values_peak
        rmin= 1
        def diff_sq_fn(parameter):
            return round(sum((y-pylandau.langau(x, *parameter))**2), 4)
        try: 
            langau_par_rmin, pcov_rmin = curve_fit(pylandau.langau, x, y, p0= (mpv, rmin, rmin, rmin))
            array_1 = np.ndarray.tolist(np.around(langau_par_rmin, decimals = 3))
            param_list = [array_1]
            workinglangaupar = [array_1]
            initial_diff_sq = [diff_sq_fn(langau_par_rmin)]
        except RuntimeError as message:
            print(str(message) + ' for ' + str( file))
            continue
        except TypeError as message:
            print(str(message) + ' for ' + str(file))
            continue

      #only one best possible parameter with least diff_sq
        for eta, sigma, A in product(np.linspace(rmin, 25,5 ), np.linspace(rmin,25, 5),np.linspace(rmin, 25, 5)):
            try:
                langau_par, pcov = curve_fit(pylandau.langau, x, y, p0= (mpv, eta, sigma,A))
                langau_par = np.ndarray.tolist(np.around(langau_par, decimals =3))
                diff= diff_sq_fn(langau_par)
                par = param_list[0]
                if initial_diff_sq[0] < .01:
                    break
                elif langau_par != par and diff < initial_diff_sq[0]:
                    param_list.append(langau_par)
                    
                    del workinglangaupar[0]
                    del initial_diff_sq[0]
                    initial_diff_sq.append(diff)
                    workinglangaupar.append(langau_par)
                    break
                else:
                    continue
            except RuntimeError as message:
                print(str(message)+ str(file))
                continue
            except TypeError as message:
                print(str(message) +'2nd'+ str(file))
            except ValueError as message:
                print(str(message) + str(file))
        workinglangaupar = workinglangaupar[0]     
        plt.plot(x, pylandau.langau(x, *workinglangaupar),color = 'b',linestyle = 'dotted', label = 'Langau')
        plt.xlabel('Time [nanoseconds]')
        plt.ylabel('Voltage [Volt]')
        plt.title('Fitting Gaussian, Landau, and Langau Distributions for '+str(file))
        plt.xlim(0,1000)
        plt.legend()
        plt.show()

