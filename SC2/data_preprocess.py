import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import seaborn as sns
import datetime
from datetime import timedelta
import os
from itertools import chain
from pyquaternion import quaternion as qt
from astropy.time import Time
from astropy import coordinates
import astropy.units as u
import datetime
import warnings
warnings.filterwarnings('ignore')


def get_data(cleanfilename,frame_no):
    print('Data preprocessing initiated')
    df = pd.read_csv(cleanfilename)
    df['Timestamp']= pd.to_datetime(df.Timestamp,format='%Y-%m-%d %H:%M:%S.%f',errors='coerce')
    df = df.set_index('Timestamp')
    if any("duty_1" in s for s in df.columns) & any("duty_2" in s for s in df.columns):
        df['duty_1'] = df['duty_1']/100
        df['duty_2'] = df['duty_2']/100
        df = df.rename(columns = {'duty_1':'str_sts_01', 'duty_2':'str_sts_02'})
    df = df.reindex(sorted(df.columns), axis=1)
    bfill_params = ['sags']
    df_bfill = df[bfill_params]
    df_bfill = df_bfill.fillna(method = 'bfill')
    df = df.drop(columns=bfill_params)
    df = df.fillna(method = 'ffill')
    df = pd.merge(df,df_bfill, on = 'Timestamp')
    df = df.dropna(axis  =0)
    df1 = df[df['frame']==int(frame_no)]
    df1.dropna(axis =0, how = 'any' , inplace = True)
    df1 = df1.resample('30S').mean()
    df1.dropna(axis =0, how = 'all' , inplace = True)
    data_start = (df1.index[0]).strftime('%d-%b-%yT%H_%M')
    data_end = (df1.index[-1]).strftime('%d-%b-%yT%H_%M')
    print('Data preprocessing completeded')
    return df1, data_start, data_end

def get_all_points(df1):
    print('Getting SAA, eclipse and PL operation')
    if any("pnl11_pr_temp" in s for s in df1.columns) & any("pnl22_pr_temp" in s for s in df1.columns):
        df1= df1.rename(columns = {'pnl11_pr_temp':'prt_11', 'pnl22_pr_temp':'prt_22'})
    time_t = np.array(df1.index)
    time = Time(time_t,scale='utc')
    cood = coordinates.get_sun(time)
    eci_xyz = cood.cartesian.xyz.value
    ax_deg = []
    ay_deg = []
    az_deg = []
    for i in range (len(df1)):
        q = qt.Quaternion(np.array([df1['q_4'].values,df1['q_1'].values, df1['q_2'].values, df1['q_3'].values]).T[i])
        q = q/q.norm
        q_bf = qt.Quaternion([1,0,0,0])
        q_rotate = q_bf*q.inverse
        vector = q_rotate.rotate(eci_xyz.T[i])/np.linalg.norm(q_rotate.rotate(eci_xyz.T[i]))
        ax_deg.append(np.arccos((np.dot([1,0,0],vector)))*180/np.pi)
        ay_deg.append(np.arccos((np.dot([0,1,0],vector)))*180/np.pi)
        az_deg.append(np.arccos((np.dot([0,0,1],vector)))*180/np.pi)
    df1['sun_ang'] = 180 - np.array(az_deg)
    df1['sun_ang'][df1['sun_ang']>60] = 60

    df1['ecl'] = df1['str_sts_03']==0
    df1['pre_ecl'] = True
    df1['post_ecl'] = True
    for i in range(len(df1)-8):
        df1['pre_ecl'][i] = df1['ecl'][i+8]==True
    for i in range(len(df1)-8):
        df1['post_ecl'][i+8] = df1['ecl'][i]==True
    df1['pre_ecl'] = (df1['pre_ecl']==True) & (df1['ecl']== False)
    df1['post_ecl'] = (df1['post_ecl']==True) & (df1['ecl']== False)
    df1['sun_lit'] = (df1['ecl']==False) & (df1['pre_ecl']== False) & (df1['post_ecl']== False)
    df1['PL'] = df1['sun_ang']>60
    print('Success')
    return df1