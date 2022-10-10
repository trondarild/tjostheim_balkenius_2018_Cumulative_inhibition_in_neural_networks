#
# comparison between mmlt and iterative
#
import png as img
import numpy as np

# todo load png image

inp_size = (32, 32)
rf_size = 3
som_size_x = 3
som_size_y = 3
rf_inc_x = 1
rf_inc_y = 1

inp_size_x = inp_size[0]
inp_size_y = inp_size[1]

map_size_x = ((inp_size_x-rf_size)/ rf_inc_x) + 1
map_size_y = ((inp_size_y-rf_size)/ rf_inc_y) + 1

numkernels = som_size_x*som_size_y
kernelsize = rf_size*rf_size

def map_from_4d(source, target_dim):
    #
    return 0

def mmlt_a(a_inp, a_act, strt_weights, rf_size, alpha_val):
    # 
    return 0

def interative_4d(a_inp, a_act, strt_weights, map_sz, som_sz, rf_inc, alpha_val):
    #
    return 0