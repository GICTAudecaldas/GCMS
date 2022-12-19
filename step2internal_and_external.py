# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 2022

@author: Juliana RL
"""


import os
from pyms.Experiment import load_expr
from pyms.DPA.PairwiseAlignment import PairwiseAlignment, align_with_tree
from pyms.DPA.Alignment import exprl2alignment
import glob

# define the input experiments list
path_expr_1="" #carpeta donde se tienen los .expr del bache 1
expr_file_1 = glob.glob(os.path.join(path_expr_1, "*.expr"))
bache_name_p='' #nombre del bache
expr_1_codes=[]
for expr in expr_file_1:
    file_name=os.path.basename(expr)
    expr_1_codes.append(file_name.split('.')[0])
    
path_expr_2=""#carpeta donde se tienen los .expr del bache 2
expr_file_2 = glob.glob(os.path.join(path_expr_2, "*.expr"))
bache_name_m='' #nombre del bache    
expr_2_codes=[]
for expr in expr_file_2:
    file_name=os.path.basename(expr)
    expr_2_codes.append(file_name.split('.')[0])

path_expr_3=""#carpeta donde se tienen los .expr del bache 3
expr_file_3 = glob.glob(os.path.join(path_expr_3, "*.expr"))
bache_name_a='' #nombre del bache    
expr_3_codes=[]
for expr in expr_file_3:
    file_name=os.path.basename(expr)
    expr_3_codes.append(file_name.split('.')[0])
    

# within replicates alignment parameters
Dw = 2.5  # rt modulation [s] UTILIZAR EL VALOR QUE MEJOR SE CONSIDERE
Gw = 0.30 # gap penalty

# do the alignment pereira
print('Aligning expt {}'.format(bache_name_p))
expr_list = []
for expr_code in expr_1_codes:
    print(expr_code)
    file_name = os.path.join(path_expr_1, expr_code + ".expr")
    expr = load_expr(file_name)
    expr_list.append(expr)
    
F1 = exprl2alignment(expr_list)
print('F1 done')
T1 = PairwiseAlignment(F1, Dw, Gw)
print('T1 done')
A1 = align_with_tree(T1, min_peaks=2)
print('A1 donde')
top_ion_list_p = A1.common_ion()
A1.write_common_ion_csv('/area1.csv', top_ion_list_p) #carpeta donde se guardará la alineación del bache 1

# do the alignment manizales
print('Aligning expt {}'.format(bache_name_m))
expr_list = []
for expr_code in expr_2_codes:
    file_name = os.path.join(path_expr_2, expr_code + ".expr")
    expr = load_expr(file_name)
    expr_list.append(expr)
    
F2 = exprl2alignment(expr_list)
print('F2 done')
T2 = PairwiseAlignment(F2, Dw, Gw)
print('T2 done')
A2 = align_with_tree(T2, min_peaks=2)
print('A2 done')
top_ion_list_m = A2.common_ion()
A2.write_common_ion_csv('/area2.csv', top_ion_list_m) #carpeta donde se guardará la alineación del bache 2

# do the alignment ARMENIA
print('Aligning expt {}'.format(bache_name_a))
expr_list = []
for expr_code in expr_3_codes:
    file_name = os.path.join(path_expr_3, expr_code + ".expr")
    expr = load_expr(file_name)
    expr_list.append(expr)
    
F3 = exprl2alignment(expr_list)
print('F3 done')
T3 = PairwiseAlignment(F3, Dw, Gw)
print('T3 done')
A3 = align_with_tree(T3, min_peaks=2)
print('A3 done')
top_ion_list_a = A3.common_ion()
A3.write_common_ion_csv('/area3.csv', top_ion_list_a)#carpeta donde se guardará la alineación del bache 3

print('complete alignment')
# Define the within-state alignment parameters.
Db = 10.0 # rt modulation
Gb = 0.30 # gap penalty

T9 = PairwiseAlignment([A1,A2,A3], Db, Gb) #alineación entre baches
A9 = align_with_tree(T9)
common_ion_list = A9.common_ion()
A9.write_common_ion_csv('/complete_area_common_ion.csv',common_ion_list) #carpeta donde se guardará la alineación completa