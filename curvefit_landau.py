#!/usr/bin/env python
import sys, os, ScopeTrace, pylandau, ScopeTrace_edit
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
for file in os.listdir("/home/kpark1/Work/SLab/data_4/") :
    with open('data_4/'+file, "r") as file1: 
        data= file1.read()
        print(str(file1) + ':\n')
    
# decode the scope trace
        trace = ScopeTrace_edit.ScopeTrace(data,1)
# find baseline and jitter 
        baseline,jitter = trace.find_baseline_and_jitter(0,250)
        jitter_stored.append(jitter)
        print(jitter)
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

#Curvefit for Landau with parameters mpv,  eta, A 
        mpv = x_values_peak
        rmin= 1
       
        try: 
            landau_par_rmin, pcov_rmin = curve_fit(pylandau.landau, x, y, p0= (mpv, rmin, rmin))
            array_1 = np.ndarray.tolist(np.around(landau_par_rmin, decimals = 3))
            param_list = [array_1]
            workinglandaupar = [array_1]
            def diff_sq_fn(parameter):
                return round(sum((y-pylandau.landau(x, *parameter))**2), 4)
        #print('The first diff is ' +str(diff_sq_fn(landau_par_rmin))+' for initial parameters ' +str(landau_par_rmin))
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
                landau_par, pcov = curve_fit(pylandau.landau, x, y, p0= (mpv, eta,A))
                landau_par = np.ndarray.tolist(np.around(landau_par, decimals =3))
                #print(landau_par)
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
        mpv_stored.append(workinglandaupar[0])
        eta_stored.append(workinglandaupar[1])
        A_stored.append(workinglandaupar[2])
        #print('In ' + str(file) +', ' +'the variance is '+ str(diff/len(y))+' for the final working landau parameters '+str(workinglandaupar))
        plt.plot(x, y, label = 'data')
        plt.plot(x, pylandau.landau(x, *workinglandaupar),color = 'r',alpha = .8, label = 'Landau with jitter of '+str(np.around(jitter, decimals = 7)))
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

