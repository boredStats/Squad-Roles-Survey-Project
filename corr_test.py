# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 02:29:07 2018

Correlation

@author: Ian
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None):
    """Return an axes of confidence bands using a simple approach.

    Notes
    -----
    .. math:: \left| \: \hat{\mu}_{y|x0} - \mu_{y|x0} \: \right| \; \leq \; T_{n-2}^{.975} \; \hat{\sigma} \; \sqrt{\frac{1}{n}+\frac{(x_0-\bar{x})^2}{\sum_{i=1}^n{(x_i-\bar{x})^2}}}
    .. math:: \hat{\sigma} = \sqrt{\sum_{i=1}^n{\frac{(y_i-\hat{y})^2}{n-2}}}

    References
    ----------
    .. [1]: M. Duarte.  "Curve fitting," JUpyter Notebook.
       http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/CurveFitting.ipynb

    """
    if ax is None:
        ax = plt.gca()

    ci = t*s_err*np.sqrt(1/n + (x2-np.mean(x))**2/np.sum((x-np.mean(x))**2))
    ax.fill_between(x2, y2+ci, y2-ci, color="#b9cfe7", edgecolor="",label='ci')

output_dir = os.path.join(os.getcwd(),"figures")
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
df = pd.read_csv("Squad Roles Survey.csv")

col_names = list(df)
x_vars = [v for v in col_names if "effective" in v]
y_vars = [v for v in col_names if "importance" in v]

c_df = df.drop([col_names[0],col_names[-1]],axis=1)

x_vals = []
for v in x_vars:
    x_vals = x_vals+list(c_df[v].values)
    
y_vals = []
for v in y_vars:
    y_vals = y_vals+list(c_df[v].values)

r_val,p_val = stats.pearsonr(x_vals,y_vals)

if p_val >= .05:
    p_lab = '>.05'
elif p_val < .05 and p_val > .001:
    p_lab = '<%03f' % p_val
else:
    p_lab = '<.001'

x = np.array(x_vals)
y = np.array(y_vals)

p, cov = np.polyfit(x, y, 1, cov=True)
y_model = np.polyval(p, x)

n = x.size
m = p.size
DF = n - m
t = stats.t.ppf(0.95, n - m)

resid = y - y_model                           
chi2 = np.sum((resid/y_model)**2)
chi2_red = chi2/(DF)
s_err = np.sqrt(np.sum(resid**2)/(DF))

x2 = np.linspace(np.min(x), np.max(x), 100)
y2 = np.linspace(np.min(y_model), np.max(y_model), 100)

fig, ax = plt.subplots(figsize=(8,6))
ax.plot(x,y,"o", color="b", markersize=8,alpha=.1,markeredgecolor="none")
ax.set_xlim([0,6.5])
ax.set_ylim([0,6.5])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
r_text = r'$r$ = %.02f, $p$ %s' % (r_val,p_lab)
ax.text(5, 6.4, r_text, fontsize=10)

ax.set_xlabel("Effectiveness score",fontsize=14)
ax.set_ylabel("Importance score",fontsize=14)

ax.plot(x,y_model,"-", color="k", linewidth=1, alpha=1, label="Fit")  

plot_ci_manual(t, s_err, n, x, x2, y2, ax=ax)

handles, labels = ax.get_legend_handles_labels()
plt.legend([handles[0],handles[1]],
        ["Line of best fit","95% confidence interval"],
        loc="lower left",frameon=False)

fpath = os.path.join(output_dir,"corr.png")
fig.savefig(fpath,bbox_inches='tight',dpi=600,transparent=True)