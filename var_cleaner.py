# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 00:41:02 2018

Function to clean variable names

@author: Ian
"""

def var_cleaner(var_list):
    cleaned_list = []
    for var in var_list:
        no_rel = var.replace("Relative ","")
        no_eff = no_rel.replace("effectiveness ","")
        no_imp = no_eff.replace("importance ","")
        no_of = no_imp.replace("of ","")
        no_lb = no_of.replace("[","")
        no_rb = no_lb.replace("]","")
        no_col = no_rb.replace(":","")
        no_rif = no_col.replace("rifleman","")
        cleaned_list.append(no_rif)
    
    return cleaned_list