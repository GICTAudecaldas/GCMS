# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 14:34:25 2022

@author: Juliana RL
"""

import os
from pyms.Experiment import load_expr
from pyms.DPA.PairwiseAlignment import PairwiseAlignment, align_with_tree
from pyms.DPA.Alignment import exprl2alignment
import glob

# define the input experiments list
path="" #carpeta donde tienes los archivos .expr
expr_file = glob.glob(os.path.join(path, "*.expr"))


bache_name='' # colocar el nombre que se quiera
exprA_codes=[]
for expr in expr_file:
    file_name=os.path.basename(expr)
    exprA_codes.append(file_name.split('.')[0])
    

# within replicates alignment parameters
Dw = 3.0  # rt modulation [s] cambiar al valor que se desee
Gw = 0.30 # gap penalty

# do the alignment
print('Aligning expt {}'.format(bache_name)) #visualizar en que experimento va
expr_list = []

for expr_code in exprA_codes:
    print(expr_code)
    file_name = os.path.join(path, expr_code + ".expr")
    expr = load_expr(file_name)
    expr_list.append(expr)
    
F1 = exprl2alignment(expr_list)
print('F1 done')
T1 = PairwiseAlignment(F1, Dw, Gw)
print('T1 done')
A1 = align_with_tree(T1, min_peaks=2)
print('A1 done')


top_ion_list = A1.common_ion()
A1.write_common_ion_csv('/Output/area2.csv', top_ion_list) # colocar la carpeta donde se quiere guardar el .csv alineado

