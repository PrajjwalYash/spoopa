import pandas as pd
import numpy as np
import seaborn as sns
import warnings
import os
warnings.filterwarnings('ignore')
import matplotlib.pyplot  as plt
plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = [20, 10]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['axes.grid'] = True

from data_preprocess import get_data, get_all_points
from sc_details import str_config, cell_temp_voc
from sc_lat_lon import get_lat_lon
from solar_cell_operation import get_load_point, exp_sags, pred_improv
from error_analysis import get_error,plot_sags,plot_sags_error,valid_points_error
from lat_lon_analysis import lat_dist_isc_error,lat_dist_sags_error,lat_lon_dist_isc,lat_lon_dist_sags,exp_isc, isc_sags_ratio
from temp_related_analysis import voc_plots
from statistics_and_report import generate_report,get_sts,store_data

folder_path = os.getcwd()
print(folder_path)
mission_name = 'SC1'


filename = os.path.join(folder_path,'Datasets/', "sc1_sep23_lon_clean.csv")    #user input

df1, data_start, data_end = get_data(filename, frame_no=29)

df1 = get_all_points(df1)

df1 = get_lat_lon(df1)


temp,ref = cell_temp_voc(df1)

L_I = 0.989
L_V = 0.982

par_nos, i_mp, i_sc,v_mp,v_oc = str_config()

par_nos_with_temp, i_l, i_sc_with_temp, v_oc_with_temp = get_load_point(df1, par_nos, i_mp, i_sc,v_mp,v_oc, ns=22, L_I = L_I, L_V = L_V,temp=temp, ref=ref)

df1 = exp_sags(df1,par_nos_with_temp, i_l, i_sc_with_temp)

df1 = pred_improv(df1)

df1,err = get_error(df1)

plot_1 = plot_sags(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

plot_2,all_point_export = plot_sags_error(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

plot_3 = lat_dist_sags_error(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

valid_point_export = valid_points_error(df1)[1]

df1,plot_4 = exp_isc(df1, L_I = L_I,mission_name=mission_name, data_end=data_end, data_start=data_start,temp=temp, ref=ref)

df1, plot_5, np_isc_ovg, sp_isc_ovg = lat_dist_isc_error(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

df1, plot_6 = isc_sags_ratio(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

df1, plot_8 = lat_lon_dist_sags(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)


df1, plot_9 = lat_lon_dist_isc(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

df1, plot_7 = voc_plots(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)


data_file_name = store_data(df1, mission_name=mission_name, data_end=data_end, data_start=data_start)

df_exp = get_sts(df1,all_point_export=all_point_export, valid_point_export=valid_point_export,np_isc_ovg=np_isc_ovg, sp_isc_ovg=sp_isc_ovg)

df_exp.to_csv(os.path.join(folder_path, 'Exports/', mission_name+'_'+data_start+'_to_'+data_end+'_stats.csv'))


report_filename = generate_report(df_exp=df_exp, mission_name=mission_name, data_end=data_end, data_start=data_start, 
                                  plot_1=plot_1, plot_2=plot_2, plot_3=plot_3, plot_4=plot_4, plot_5=plot_5, plot_6=plot_6, plot_7=plot_7, plot_8=plot_8, plot_9=plot_9)
