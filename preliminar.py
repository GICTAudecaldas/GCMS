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
    
















        

