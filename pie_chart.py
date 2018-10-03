# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:21:19 2018

Pie chart

@author: Ian
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

output_dir = os.path.join(os.getcwd(),"figures")
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

df = pd.read_csv("Squad Roles Survey.csv")

col_names = list(df)
time_var = [v for v in col_names if "hours" in v][0]
t_vals = list(df[time_var].values)

def recode_time(string_list):
    dummy_code = []
    for ts in string_list:
        if "less than 50" in ts:
            dummy_code.append(1)
        elif "50 to 100" in ts:
            dummy_code.append(2)
        elif "100 to 200" in ts:
            dummy_code.append(3)
        else:
            dummy_code.append(4)
    return dummy_code

dc = np.array(recode_time(t_vals))
dcu,dcc = np.unique(dc,return_counts=True)
dcp = dcc/len(dc)

labs = ['<50','50 to 100','100 to 200','200+']

fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)

explode = (0.4,0,0,0) 
colors = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange']
ax.pie(dcp,autopct='%1.1f%%',
       colors=colors,
       textprops=dict(color="k",fontsize=12))
                                  
ax.legend(labs,title='Hours played',loc="lower right")

fpath = os.path.join(output_dir,"piechart.png")
fig.savefig(fpath,bbox_inches='tight',dpi=600,transparent=True)