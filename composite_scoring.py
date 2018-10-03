# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 00:42:52 2018

composite scoring

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
roles = ["medic","anti-tank","optics","AR/MG","scout","grenadier","crewman","marksman"]

c_df = df.drop([col_names[0],col_names[-1]],axis=1)
c_desc = c_df.describe()

crole_df = pd.DataFrame()
for role in roles:
    ivar = [v for v in col_names if role in v]
    i_val = c_df[ivar].values
    c_val = (i_val[:,0] + i_val[:,1])/2
    crole_df[role] = c_val

crole_desc = crole_df.describe()
crole_desc.sort_values(by=['mean'],ascending=False,axis=1,inplace=True)

xpos = np.arange(8)
capsize = 1

fig,ax = plt.subplots()
ax.errorbar(x=xpos,
            y=crole_desc.loc['mean'].values,
            yerr=crole_df.sem().values,
            fmt='ko',capsize=capsize,
            markersize='1',linestyle='-',
            linewidth=.2)
ax.set_ylim([1,6])
ax.set_xticks(xpos)
ax.set_xticklabels(list(crole_desc),rotation=90,ha='center',fontsize=16)
ax.set_ylabel('Composite Score')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ytp = crole_desc.loc['mean'].values
for a,b in zip(xpos, ytp):
    str_in = '%.02f' % crole_desc.loc['mean'].values[a]
    ax.text(a-.2, b+.2, str(str_in),fontsize=13)

for xl in xpos:
    ax.axvline(x=xl,linestyle=':',color='k',linewidth=.5)

fpath = os.path.join(output_dir,"composite_scores.png")
fig.savefig(fpath,bbox_inches='tight',dpi=600,transparent=True)