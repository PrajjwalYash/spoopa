import pandas as pd
import numpy as np
import os
from itertools import chain
import warnings
warnings.filterwarnings('ignore')

folder_path = os.getcwd()

def get_load_point(df1, par_nos, i_mp, i_sc,v_mp,v_oc, ns, L_I, L_V, temp, ref):
    print('Obtaining Load point')
    par_nos_with_temp = np.array([par_nos]*len(df1)).reshape((len(df1),len(par_nos)))
    i_mp_with_temp = L_I*np.array([i_mp]*len(df1)).reshape((len(df1),len(i_mp)))
    i_mp_with_temp = i_mp_with_temp + ((temp-ref)*0.000240)
    i_sc_with_temp = L_I*np.array([i_sc]*len(df1)).reshape((len(df1),len(i_sc)))
    i_sc_with_temp = i_sc_with_temp+ ((temp-ref)*0.000358)
    v_mp_with_temp = L_V*np.array([v_mp]*len(df1)).reshape((len(df1),len(v_mp)))
    v_mp_with_temp = v_mp_with_temp +  (temp-ref)*(-0.0067)
    v_oc_with_temp = L_V*np.array([v_oc]*len(df1)).reshape((len(df1),len(v_oc)))
    v_oc_with_temp = v_oc_with_temp + ((temp-ref)*(-0.00635))
    c3 = 0.000000001
    m = np.log(np.log((i_sc_with_temp*(1+c3)-i_mp_with_temp)/(c3*i_sc_with_temp))/(np.log((1+c3)/c3)))/np.log(v_mp_with_temp/v_oc_with_temp)
#     ns = 22
    bat_vlt = np.array([df1['bat_vlt_sel'].values]*par_nos.shape[0]).T
    v_l = (bat_vlt + 3)/ns
    i_l = i_sc_with_temp*(1-c3*np.exp((np.log(((1+c3)/c3))/v_oc_with_temp**m) * v_l**m - 1))
    print('Success')
    return par_nos_with_temp, i_l, i_sc_with_temp,v_oc_with_temp 

def exp_sags(df,par_nos_with_temp, i_l, i_sc_with_temp):
    print('Estimating SAGS')
    df_exp_sags = df.copy(deep = True) #deep copy to make sure original df does not have too many columns
    c = np.array(df_exp_sags.columns)
    str_cols = c[df_exp_sags.columns.str.startswith('str_sts')==True]
    df_exp_sags['sum_str'] = np.sum(df_exp_sags[str_cols], axis =1)
    for i in range (len(str_cols)):
        df_exp_sags['comp_'+str_cols[i]] = 1 - df_exp_sags[str_cols[i]] #complementary status
        df_exp_sags['pred_cur'] = (df_exp_sags[df_exp_sags.columns[df_exp_sags.columns.str.startswith('str')]]*i_l*par_nos_with_temp).sum(axis = 1)
    c = np.array(df_exp_sags.columns)
    df_exp_sags['comp_cur'] = (df_exp_sags[df_exp_sags.columns[df_exp_sags.columns.str.startswith('comp')]]*i_sc_with_temp*par_nos_with_temp).sum(axis=1)
    df_exp_sags['comp_cur'][df_exp_sags['str_sts_03']==0]=0
    df_exp_sags['exp_sags'] = (df_exp_sags['comp_cur']+df_exp_sags['pred_cur'])
    df['sum_str'] = df_exp_sags['sum_str']
    df['exp_sags'] = df_exp_sags['exp_sags']
    df['pred_cur'] = df_exp_sags['pred_cur']
    print('Success')
    return df

def pred_improv(df):
    print('Sun intensity factor and SAA implementation')
    df_copy = df.copy(deep = True)
    df_copy['pred_cur'] = df_copy['pred_cur']*np.cos(df_copy['sun_ang']*np.pi/180)
    df_copy['exp_sags'] = df_copy['exp_sags']*np.cos(df_copy['sun_ang']*np.pi/180)
    df_copy['doy'] = df_copy.index.strftime('%j').astype('int')
    sun_int_factor = os.path.join(folder_path,'SC1', "sun_int_fac.csv")
    df_int = pd.read_csv(sun_int_factor)
    df_int.dropna(how = 'all', axis = 0, inplace = True)
    df_int.dropna(how = 'all', axis = 1, inplace = True)
    df_copy = df_copy.merge(df_int[['doy','intensity factor']], on = 'doy', suffixes=('', '_y'))
    df_copy.drop(df_copy.filter(regex='_y$').columns, axis=1, inplace=True)
    df_copy['pred_cur'] = df_copy['pred_cur']*df_copy['intensity factor']
    df_copy['exp_sags'] = df_copy['exp_sags']*df_copy['intensity factor']
    df['pred_cur'] = df_copy['pred_cur'].values
    df['exp_sags'] = df_copy['exp_sags'].values
    df['sags'][df['sags']==df['sags'].min()] = 0
    print('Success')
    return df