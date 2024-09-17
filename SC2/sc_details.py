import pandas as pd
import numpy as np
import os
from itertools import chain
import warnings
warnings.filterwarnings('ignore')

folder_path = os.getcwd()

def cell_temp_voc(df1):
    print('Getting temperature')
    inn_str_no = 14
    out_str_no = 16
    temp = ([[((df1['prt_22'])).values - df1['prt_11'].values + df1['cell_temp']]*inn_str_no, [df1['cell_temp'].values]*out_str_no])
    temp = list(chain(*temp))
    temp = np.array(temp).T
    ref = 28
    print('Success')
    return temp, ref

def str_config():
    print('String configuration')
    string_config_file = os.path.join(folder_path, "sc2_str.csv")
    str_config = pd.read_csv(string_config_file)
    par_nos = np.array(str_config['Np'])
    i_mp = np.array(str_config['Imp'])/1000
    i_sc = np.array(str_config['Isc'])/1000
    v_mp = np.array(str_config['Vmp'])/1000
    v_oc = np.array(str_config['Voc'])/1000
    print('Success')
    return par_nos, i_mp, i_sc,v_mp,v_oc