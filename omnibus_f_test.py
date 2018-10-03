# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 00:42:52 2018

Omnibus F-test

@author: Ian
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from var_cleaner import var_cleaner as vc

output_dir = os.path.join(os.getcwd(),"figures")
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

df = pd.read_csv("Squad Roles Survey.csv")

col_names = list(df)
roles = ["medic","anti-tank","optics","AR/MG","scout","grenadier","crewman","marksman"]
eff_vars = [v for v in col_names if "effective" in v]
imp_vars = [v for v in col_names if "importance" in v]

c_df = df.drop([col_names[0],col_names[-1]],axis=1)
c_desc = c_df.describe()

f,p = f_oneway(
        c_df[list(c_df)[0]].values,
        c_df[list(c_df)[1]].values,
        c_df[list(c_df)[2]].values,
        c_df[list(c_df)[3]].values,
        c_df[list(c_df)[4]].values,
        c_df[list(c_df)[5]].values,
        c_df[list(c_df)[6]].values,
        c_df[list(c_df)[7]].values,
        c_df[list(c_df)[8]].values,
        c_df[list(c_df)[9]].values,
        c_df[list(c_df)[10]].values,
        c_df[list(c_df)[11]].values,
        c_df[list(c_df)[12]].values,
        c_df[list(c_df)[13]].values,
        c_df[list(c_df)[14]].values,
        c_df[list(c_df)[15]].values,)

p_mc = p*(16*15)
if p_mc >= .05:
    p_lab = '>.05'
elif p_mc < .05 and p_mc > .001:
    p_lab = '<%.3f' % p_mc
else:
    p_lab = '<.001'
    
imp_df = c_df.drop(eff_vars,axis=1)
imp_desc = imp_df.describe()
imp_desc.sort_values(by=['mean'],ascending = False,axis=1,inplace=True)

lab_or = []
for lab in list(imp_desc):
    for r in roles:
        if r in lab:
            lab_or.append(r)

eff_df = c_df.drop(imp_vars,axis=1)
eff_desc = eff_df.describe()

eff_means = []
for lab in list(imp_desc):
    for r in lab_or:
        if r in lab:
            col = [s for s in list(eff_desc) if r in s][0]
            eff_means.append(eff_desc[col]['mean'])

xpos = np.arange(8)
capsize = 2
bar_width = 0.35

fig,ax = plt.subplots()

ax.bar(x=xpos,height=imp_desc.loc['mean'].values,
       width=bar_width,
       yerr=imp_df.sem().values,
       capsize=capsize,color='g',
       label='Importance')

ax.bar(x=xpos+bar_width,height=eff_means,
       width=bar_width,
       yerr=eff_df.sem().values,
       capsize=capsize,color='b',
       label='Effectiveness')

ax.set_ylim([1,6])
ax.set_xticks(xpos)
ax.set_xticklabels(vc(list(imp_desc)),rotation=60,ha='center')
ax.xaxis.set_ticks_position('none') 
ax.set_ylabel('Score')
ax.legend(loc='upper center',frameon=False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

f_text = r'$F$ = %.02f, $p$ %s' % (f,p_lab)
ax.text(5.3, 6.2, f_text, fontsize=10)

fpath = os.path.join(output_dir,"omnibus_f.png")
fig.savefig(fpath,bbox_inches='tight',dpi=600)