# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 19:54:34 2018

t-tests within role

@author: Ian
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

output_dir = os.path.join(os.getcwd(),"figures")
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
df = pd.read_csv("Squad Roles Survey.csv")

col_names = list(df)
roles = ["medic","anti-tank","optics","AR/MG","scout","grenadier","crewman","marksman"]

c_df = df.drop([col_names[0],col_names[-1]],axis=1)
c_desc = c_df.describe()

fig,(ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8) = plt.subplots(1,8,figsize=(20,20))
ax_list = fig.axes
bar_width = 0.35

for i,role in enumerate(roles):
    ### Doing t-test
    ivar = [v for v in col_names if role in v]
    idf = c_df[ivar]
    
    i_val = idf[ivar].values
    t,p = ttest_ind(i_val[:,0],i_val[:,1])
    p_mc = p*(1)
    if p_mc >= .05:
        p_lab = '>.05'
    elif p_mc < .05 and p_mc > .001:
        p_lab = '<.05'
    else:
        p_lab = '<.001'
        
    means = np.mean(i_val,axis=0)
    std_err = idf.sem().values
    
    ### Making subplots
    cax = ax_list[i]
    cax.bar(x=1,capsize=4,
            width=bar_width,height=means[0],
            yerr=std_err[0],color='g',
            error_kw=dict(lw=2, capsize=4, capthick=1),
            alpha=1,label='Importance')
    cax.bar(x=1+bar_width,capsize=4,
            width=bar_width,height=means[1],
            yerr=std_err[1],color='b',
            error_kw=dict(lw=2, capsize=4, capthick=1),
            alpha=1,label='Effectiveness')
    
    cax.set_xticks([])
    cax.set_ylim([1,6])
    cax.set_yticklabels(labels=np.arange(1,6),fontsize=20)
    cax.set_ylabel('Score')
    cax.set_xlabel(role,fontsize=24)
    
#    t_text = r'$t$=%.2f, $p$%s' % (t,p_lab)
    t_text = r'$t$=%.2f' % t
    cax.text(1, 6, t_text, fontsize=20)
    
    cax.spines['top'].set_visible(False)
    cax.spines['right'].set_visible(False)
    
    ## Custom settings for subplots
    if p_mc < .05:
        cax.text(1+(bar_width/2),5.8,"*",fontsize=30)
        cax.axhline(y=5.8,xmin=.2,xmax=.9,color='k')
    
    if i != 0:
        cax.spines['left'].set_visible(False)
        cax.set_yticks([])
        cax.set_ylabel('')
    else:
        cax.set_ylabel('Score',fontsize=22)
        
    if i == len(roles)-1:
        cax.legend(loc='center left',
                   frameon=False,fontsize=30,
                   bbox_to_anchor=(-1, 0.85))
        
fpath = os.path.join(output_dir,"t_tests_roles.png")
fig.savefig(fpath,bbox_inches='tight',dpi=600,transparent=True)