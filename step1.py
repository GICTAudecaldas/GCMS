# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 18:04:01 2022

@author: Juliana RL
"""

import os
import glob
import time
from pyms.GCMS.IO.ANDI import ANDI_reader
from pyms.Noise.SavitzkyGolay import savitzky_golay
from pyms.TopHat import tophat
from pyms.IntensityMatrix import build_intensity_matrix_i
from pyms.BillerBiemann import BillerBiemann, rel_threshold, num_ions_threshold
from pyms.Noise.Analysis import window_analyzer
from pyms.Peak.Function import peak_sum_area,peak_top_ion_areas
from pyms.Experiment import Experiment

start = time.time()


path="" #carpeta donde estan los .CDFs
CDF_files = glob.glob(os.path.join(path, "*.CDF"))



for GCMS in CDF_files:
    file_name=os.path.basename(GCMS)
    name=file_name.split('.')[0]
    data = ANDI_reader(GCMS)
    print(data.info())
    
    im = build_intensity_matrix_i(data)
    n_scan, n_mz = im.size

    for ii in range(n_mz):
        ic = im.get_ic_at_index(ii)
        ic_smooth = savitzky_golay(ic)
        ic_bc = tophat(ic_smooth)
        im.set_ic_at_index(ii, ic_bc) 
        
        
    peak_list = BillerBiemann(im, points=9, scans=2)
    print('peak selection')
    tic = data.tic
    noise_level = window_analyzer(tic)
    filtered_peak_list=rel_threshold(peak_list, percent=2)
    filtered_peak_list_by_noise = num_ions_threshold(filtered_peak_list, n=3, cutoff=noise_level)
    print('peak filtering')
    print('inicial peaks: {}'.format(len(peak_list)))
    print('first filter: {}'.format(len(filtered_peak_list)))
    print('noise filter: {}'.format(len(filtered_peak_list_by_noise)))


    for peak in peak_list:
        peak.crop_mass(35, 499) #cambiar estos valores según la exploración preliminar de los datos

        peak.null_mass(73)#aquí se pueden agregar otras masas que no se consideren relevantes
        peak.null_mass(147)

        area = peak_sum_area(im, peak)
        peak.area = area
        area_dict = peak_top_ion_areas(im, peak)
        peak.ion_areas = area_dict

    tic_clean=im.tic

    expr = Experiment(name, peak_list)
    f='' #carpeta donde se van a guardar los .expr
    output_file=f+name+'.expr'

    expr.dump(output_file)

    output_tic='/Output/tic/'+name+'_tic.csv' #carpeta donde se van a guardar los .tic
    output_tic_clean='/Output/tic/'+name+'_tic_clean.csv'#carpeta donde se van a guardar los .tic
    tic.write(output_tic, minutes=True)
    tic_clean.write(output_tic_clean, minutes=True)
















        

