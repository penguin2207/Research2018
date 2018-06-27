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
for file in os.listdir("/home/kpark1/Work/SLab/data/") :
    with open('data/'+file, "r") as file1: 
        data= file1.read()
        print(str(file1) + ':\n')
    
# decode the scope trace
        trace = ScopeTrace.ScopeTrace(data,1)
# find baseline and jitter 
        baseline,jitter = trace.find_baseline_and_jitter(0,250)
        jitter_stored.append(jitter)
        print(jitter)
#set x and y
        inverted_yvalues = [-(val-baseline) for val in trace.yvalues]
        
#x values at peaks and if multiple x values of the same max y values, select the first max
        x = np.array(trace.xvalues)
        y = np.array(inverted_yvalues) 
        idx = np.where(y_array == y_array.max())[0][0]
        x_peak = x[idx]

#Curvefit for Landau with parameters mpv,  eta, A 
        mpv = x_peak
        rmin= 1
        def diff_sq_fn(parameter):
            return round(sum((y-pylandau.landau(x, *parameter))**2), 4)
        try: 
            land_par_rmin, pcov_rmin = curve_fit(pylandau.landau, x, y, p0= (mpv, rmin, rmin))
            par_init = np.ndarray.tolist(np.around(land_par_rmin, decimals = 3))
            working_land_par = par_init
            initial_diff_sq = [diff_sq_fn(landau_par_rmin)]
        
        except RuntimeError as message:
            print(str(message) + ' for ' + str( file))
            continue
        except TypeError as message:
            print(str(message) + ' for ' + str(file))
            continue

      #only one best possible parameter with the least diff_sq
        for eta, A in product(np.linspace(rmin, 25,5 ), np.linspace(rmin, 25, 5)):
            try:
                land_par, pcov = curve_fit(pylandau.landau, x, y, p0= (mpv, eta,A))
                land_par = np.ndarray.tolist(np.around(land_par, decimals =3))
                
                if initial_diff_sq[0] < .01:
                    break
                elif land_par != working_par[0] and diff_sq_fn(land_par) < initial_diff_sq[0]:
                    working_land_par[0] =land_par
                    initial_diff_sq[0] = diff_sq_fn(land_par)
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
        working_land_par = working_land_par[0]
        mpv_stored.append(working_land_par[0])
        eta_stored.append(working_land_par[1])
        A_stored.append(working_land_par[2])
        #print('In ' + str(file) +', ' +'the variance is '+ str(diff/len(y))+' for the final working landau parameters '+str(workinglandaupar))
        plt.plot(x, y, label = 'data')
        plt.plot(x, pylandau.landau(x, *working_land_par),color = 'r',alpha = .8, label = 'Landau with jitter of '+str(np.around(jitter, decimals = 7)))
        plt.title(file)
        #plt.ylim(-.005, .04)
        plt.xlabel('Time [nanoseconds]')
        plt.ylabel('Voltage [V]')
        plt.legend()
        plt.show()
     
        
#create a histogram -> CHANGE THE FILE NAME EACH TIME YOU RUN IT
#with open('jitter_data_3.csv', 'wb') as f:
    #wr = csv.writer(f)
    #wr.writerow(jitter_stored)

#with open('mpv_data_3.csv', 'wb') as f:
    #wr = csv.writer(f)
    #wr.writerow(mpv_stored)
#with open('eta_data_3.csv', 'wb') as f:
    #wr = csv.writer(f)
    #wr.writerow(eta_stored)

#with open('A_data_3.csv', 'wb') as f:
    #wr = csv.writer(f)
    #wr.writerow(A_stored)

