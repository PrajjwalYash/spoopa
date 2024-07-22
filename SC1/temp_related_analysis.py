import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = [20, 10]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['axes.grid'] = True
import os


folder_path = os.getcwd()

def voc_plots(df1, data_start, data_end, mission_name):
    print('Temperature related plot')
    string_config_file = os.path.join(folder_path,'SC1', "sc1_str.csv")
    str_config = pd.read_csv(string_config_file)
    sp11_strs = df1.columns[df1.columns.str.startswith('str_sts')][str_config['Panel']=='SP11']
    sp12_strs = df1.columns[df1.columns.str.startswith('str_sts')][str_config['Panel']=='SP12']
    sp21_strs = df1.columns[df1.columns.str.startswith('str_sts')][str_config['Panel']=='SP21']
    sp22_strs = df1.columns[df1.columns.str.startswith('str_sts')][str_config['Panel']=='SP22']
    df1['sp11_sum_str'] = df1[sp11_strs].sum(axis=1)
    df1['sp12_sum_str'] = df1[sp12_strs].sum(axis=1)
    df1['sp21_sum_str'] = df1[sp21_strs].sum(axis=1)
    df1['sp22_sum_str'] = df1[sp22_strs].sum(axis=1)
    df_voc = df1[df1['sun_lit']==True][['cell_temp','prt_11', 'sp21_sum_str']]
    df_voc['shunt_str_no'] = len(sp21_strs) - df_voc['sp21_sum_str']
    df_voc['gradient'] = df_voc['cell_temp'] - df_voc['prt_11']
#     corr= np.round(spearmanr(df_voc['gradient'], df_voc['shunt_str_no'])[0],2)
    fig, ax1 = plt.subplots(figsize=(20, 10))
    ax1.plot(df1['cell_temp'][:500], label = 'voc cell temp', marker = '*')
    ax1.plot(df1['cell_temp'][:500] - df1['prt_11'][:500], label = 'gradient', marker = '*')
    ax1.plot(df1['prt_11'][:500], label = 'prt',color = 'black', marker = '*')
    #     ax2.plot(len(sp21_strs) - df1[df1['sun_lit']==True]['sp21_sum_str'][100:300], label = 'no_of_shunted_str',color = 'purple', marker = '*')
    plt.title(mission_name+'_'+data_start+'_to_'+data_end+'\n PRT, cell temp & gradient')
    ax1.set_ylabel('temp')
#     ax2.set_ylabel('shunted string no.')
    ax1.legend(loc = 'upper right', ncols=3)
    ax1.set_ylim(-10,100)
    ax1.grid()
    plt.xlabel('Timestamp')
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'voc_shunt.png'
    plot_7 = results_dir+plot_name
    plt.savefig(results_dir+plot_name)
    #plt.show()
    df1['gradient'] = df_voc['gradient']
    df1['shunt_str_no'] = df_voc['shunt_str_no']
    print('Success')
    return df1, plot_7