#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
import ScopeTrace
import math
from scipy.optimize import curve_fit
#---------------------------------------------------------------------------------------------------
# M A I N
#---------------------------------------------------------------------------------------------------
# initial settings
mlp.rcParams['axes.linewidth'] = 2

for filename in sys.argv[1:]:
    print ' File to open: ' + filename
    with open(filename,"r") as file:
        data = file.read()

# decode the scope trace
trace = ScopeTrace.ScopeTrace(data,1)

# find baseline and jitter
baseline,jitter = trace.find_baseline_and_jitter(0,250)
print ' Baseline: %10.6f,  Jitter: %10.6f'%(baseline,jitter)

# calculate the baseline
yvalues_list = []
for i in range(len(trace.xvalues)):
    if float(trace.xvalues[i]) <= 250:
        yvalues_list.append(float(trace.yvalues[i]))
    else:
        break
sum_1 = sum(yvalues_list)
baseline = sum_1 /  len(yvalues_list)
print('Baseline:' + str(baseline))
   
# calculate the jitter or variance
mean = sum(trace.yvalues)/len(trace.yvalues)
difference_list = []
i=0 
while i <= 250:
    difference_value_sq = (trace.yvalues[i]-baseline)**2
    difference_list.append(difference_value_sq)
    i += 1
jitter = sum(difference_list) / 250
print('Jitter:'+ str(jitter))
#Curve fitting
def func(amp, b, c, width):
	return amp*math.exp(-.5*(b

#temporary for 15192.CSV
jitter_2 = .002416
gaussian_yvalues = []
landau_yvalues = []
width = math.sqrt(jitter_2)
amp = 1/(2*math.pi *width**2)
for i in trace.xvalues:
    gaussian_yvalue = amp * math.exp(-.5*((i-mean)/width)**2)
    gaussian_yvalues.append(gaussian_yvalue)
for i in trace.xvalues:
  #  if i<0:
    landau_yvalue =math.exp(-.5*(i+ math.exp(-i))) / math.sqrt(2*math.pi)
   # else:
    #     landau_yvalue =(math.exp(-i- math.exp(i))) / math.sqrt(2*math.pi)
 #   print(landau_yvalue, i) 
    landau_yvalues.append(landau_yvalue)

#threshold = 3*jitter
#delta_min = 2*jitter
#n_pulses = trace.find_number_of_pulses(baseline,threshold,delta_min)

# get x and y values of the traces
xvalues = trace.xvalues
yvalues = []
for each_yvalue in trace.yvalues:
    each_adjusted_yvalue = each_yvalue - baseline
    yvalues.append(each_adjusted_yvalue)

inverted_yvalues = []
for value in yvalues:
    inverted_yvalue = -value
    inverted_yvalues.append(inverted_yvalue)


new_xvalues = list(range(len(trace.yvalues)))
# define the figure
fig = mlp.pyplot.gcf()
fig.set_size_inches(18.5, 14.5)
plt.figure(1)
#plt.plot(xvalues,yvalues, color = 'b')
plt.plot(xvalues,inverted_yvalues, color = 'b')
#plt.scatter(new_xvalues, gaussian_yvalues, color = 'g') 
plt.plot(new_xvalues, landau_yvalues, color = 'r')


# make plot nicer
plt.title("Oscilloscope", fontsize=28)
plt.xlabel('x-interval[n%s] '%trace.horizontal_units, fontsize=24)
plt.ylabel('y-reading [%s]'%trace.vertical_units, fontsize=24)
#plt.xlim([-10,10])
# tick marker sizes
ax = plt.gca()
#ax.xaxis.set_tick_params(labelsize=16)
#ax.yaxis.set_tick_params(labelsize=20)

# save plot for later viewing
plt.subplots_adjust(top=0.99, right=0.99, bottom=0.10, left=0.10)
plt.savefig("oscilloscope_plot.png",bbox_inches='tight',dpi=400)
plt.show()




