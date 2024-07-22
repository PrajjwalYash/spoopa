import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = [20, 10]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['axes.grid'] = True
import seaborn as sns
import os
import warnings


folder_path = os.getcwd()

def lat_dist_sags_error(df1, data_start, data_end, mission_name):
    print('Lon-lat distribution SAGS')
    path = os.path.join(folder_path,'SC1', "pole_def_mw.csv")
    pole_def = pd.read_csv(path)
    n_pole_def = pole_def['n_pole_def'][pole_def['Month'] == (df1.index[0]).strftime('%b')].values[0]
    s_pole_def = pole_def['s_pole_def'][pole_def['Month'] == (df1.index[0]).strftime('%b')].values[0]
    n_h = (df1[(df1['lat']<n_pole_def) & (df1['lat']>0) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_sags'].values)
    n_p = (df1[(df1['lat']>n_pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_sags'].values)
    s_h = (df1[(df1['lat']<0) & (df1['lat']>-s_pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_sags'].values)
    s_p = (df1[(df1['lat']<-s_pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_sags'].values)
    n_h = n_h[~np.isnan(n_h)]
    n_p = n_p[~np.isnan(n_p)]
    s_h = s_h[~np.isnan(s_h)]
    s_p = s_p[~np.isnan(s_p)]
    number = (len(n_h), len(n_p), len(s_h), len(s_p))
    np_mean_error_per = []
    nh_mean_error_per = []
    sh_mean_error_per = []
    sp_mean_error_per = []
    n = 50
    if number[1]>n:
            for i in range(2000):
                np_mean_error_per.append(np.random.choice(n_p, size = 85).mean())
                i = i+1
            np_eighty_error = (np.round(np.quantile(np_mean_error_per, 0.05),2), np.round(np.quantile(np_mean_error_per, 0.95),2))
    if number[0]>n:
            for i in range(2000):
                nh_mean_error_per.append(np.random.choice(n_h, size = 85).mean())
                i = i+1
            nh_eighty_error = (np.round(np.quantile(nh_mean_error_per, 0.05),2), np.round(np.quantile(nh_mean_error_per, 0.95),2))
    if number[2]>n:
            for i in range(2000):
                sh_mean_error_per.append(np.random.choice(s_h, size = 85).mean())
                i = i+1
            sh_eighty_error = (np.round(np.quantile(sh_mean_error_per, 0.05),2), np.round(np.quantile(sh_mean_error_per, 0.95),2))
    if number[3]>n:
            for i in range(2000):
                sp_mean_error_per.append(np.random.choice(s_p, size = 85).mean())
                i = i+1
            sp_eighty_error = (np.round(np.quantile(sp_mean_error_per, 0.05),2), np.round(np.quantile(sp_mean_error_per, 0.95),2))
    if number[1]>n:
        pmerrornp = str(np.round(np.mean(np_mean_error_per),2))  + "\u00B1" + str(np.round((np_eighty_error[1] - np.mean(np_mean_error_per)),2))
    if number[0]>n:
        pmerrornh = str(np.round(np.mean(nh_mean_error_per),2))  + "\u00B1" + str(np.round((nh_eighty_error[1] - np.mean(nh_mean_error_per)),2))
    if number[2]>n:
        pmerrorsh = str(np.round(np.mean(sh_mean_error_per),2))  + "\u00B1" + str(np.round((sh_eighty_error[1] - np.mean(sh_mean_error_per)),2))
    if number[3]>n:
        pmerrorsp = str(np.round(np.mean(sp_mean_error_per),2))  + "\u00B1" + str(np.round((sp_eighty_error[1] - np.mean(sp_mean_error_per)),2))

    plt.figure(figsize = (20,10))
    if number[1]>n:
        sns.histplot(np_mean_error_per, kde = True, label = 'North Pole error in A :{}'.format(pmerrornp),color  = 'blue')
    if number[0]>n:
        sns.histplot(nh_mean_error_per, kde = True, label = 'North Hemisphere error in A :{}'.format(pmerrornh),color = 'green' )
    if number[3]>n:
        sns.histplot(sp_mean_error_per, kde = True, label = 'South Pole error in A :{}'.format(pmerrorsp),color = 'cyan')
    if number[2]>n:
        sns.histplot(sh_mean_error_per, kde = True , label = 'South Hemisphere error in A :{}'.format(pmerrorsh),color = 'brown')
    
    plt.title(mission_name+'_'+data_start+'_to_'+data_end+'\n error in SAGS current prediction - latitude wise')
    plt.xlabel('Overgeneration (in A)')
    plt.ylabel('Count\nThe number of points at NHemisphere, NPole,\n SHemisphere, SPole are respectively  {}'.format(number))
    plt.legend(loc='upper left', ncols=2)
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'error_latitude_wise.png'
    plt.grid()
    plt.savefig(results_dir+plot_name)
    plot_3 = results_dir+plot_name
    #plt.show()
    print('Success')
    return plot_3



def exp_isc(df1, L_I, data_start, data_end, mission_name, temp, ref):
    print('Isc time-series plot')
    df1['exp_isc'] = 0.5122416
    df1['exp_isc'] = (df1['exp_isc']+(temp[:,-1]-ref)*0.000358)
    doy = df1.index.strftime('%j').astype('int')[0]
    sun_int_factor = os.path.join(folder_path,'SC1', "sun_int_fac.csv")
    df_int = pd.read_csv(sun_int_factor)
    df_int.dropna(how = 'all', axis = 0, inplace = True)
    df_int.dropna(how = 'all', axis = 1, inplace = True)
    int_fac = df_int['intensity factor'][df_int['doy']==doy].values
    df1['exp_isc'] = L_I*int_fac*df1['exp_isc']
    df1['exp_isc'] = df1['exp_isc']*np.cos(df1['sun_ang']*np.pi/180)
    df1['exp_isc'][df1['sags']<10] = min(df1['isc'])
    plt.figure(figsize = (20,10))
    plt.plot(df1['exp_isc'][:500],marker = '*', label = 'expected Isc')
    plt.plot(df1['isc'][:500], marker = '*',label = 'observed Isc')
    plt.grid()
    plt.ylim(0.4,0.6)
    plt.title(mission_name+'_'+data_start+' - Expected and Observed Isc')
    
    plt.ylabel('Isc (in A)')
    plt.xlabel('Timestamp')
    plt.legend()
    plt.xticks(rotation = 45)
    
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'expected_vs_obs_Isc.png'
    plt.savefig(results_dir+plot_name)
    plot_4 = results_dir+plot_name
    #plt.show()
    print('Success')
    return df1, plot_4


def lat_dist_isc_error(df1, data_start, data_end, mission_name):
    print('Isc lon-lat distribution')
    path = os.path.join(folder_path,'SC1', "pole_def_mw.csv")
    pole_def = pd.read_csv(path)
    n_pole_def = pole_def['n_pole_def'][pole_def['Month'] == (df1.index[0]).strftime('%b')].values[0]
    s_pole_def = pole_def['s_pole_def'][pole_def['Month'] == (df1.index[0]).strftime('%b')].values[0]
    df1['diff_isc'] = df1['isc'] - df1['exp_isc']
    n_h = 1000*(df1[(df1['lat']<n_pole_def) & (df1['lat']>0) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_isc'].values)
    n_p = 1000*(df1[(df1['lat']>n_pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_isc'].values)
    s_h = 1000*(df1[(df1['lat']<0) & (df1['lat']>-s_pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_isc'].values)
    s_p = 1000*(df1[(df1['lat']<-s_pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]['diff_isc'].values)
    n_h = n_h[~np.isnan(n_h)]
    n_p = n_p[~np.isnan(n_p)]
    s_h = s_h[~np.isnan(s_h)]
    s_p = s_p[~np.isnan(s_p)]
    number = (len(n_h), len(n_p), len(s_h), len(s_p))
    np_mean_error_per = []
    nh_mean_error_per = []
    sh_mean_error_per = []
    sp_mean_error_per = []
    n = 50
    if number[1]>n:
            for i in range(2000):
                np_mean_error_per.append(np.random.choice(n_p, size = 85).mean())
                i = i+1
            np_eighty_error = (np.round(np.quantile(np_mean_error_per, 0.05),2), np.round(np.quantile(np_mean_error_per, 0.95),2))
    if number[0]>n:
            for i in range(2000):
                nh_mean_error_per.append(np.random.choice(n_h, size = 85).mean())
                i = i+1
            nh_eighty_error = (np.round(np.quantile(nh_mean_error_per, 0.05),2), np.round(np.quantile(nh_mean_error_per, 0.95),2))
    if number[2]>n:
            for i in range(2000):
                sh_mean_error_per.append(np.random.choice(s_h, size = 85).mean())
                i = i+1
            sh_eighty_error = (np.round(np.quantile(sh_mean_error_per, 0.05),2), np.round(np.quantile(sh_mean_error_per, 0.95),2))
    if number[3]>n:
            for i in range(2000):
                sp_mean_error_per.append(np.random.choice(s_p, size = 85).mean())
                i = i+1
            sp_eighty_error = (np.round(np.quantile(sp_mean_error_per, 0.05),2), np.round(np.quantile(sp_mean_error_per, 0.95),2))
    if number[1]>n:
        pmerrornp = str(np.round(np.mean(np_mean_error_per),2))  + "\u00B1" + str(np.round((np_eighty_error[1] - np.mean(np_mean_error_per)),2))
    if number[0]>n:
        pmerrornh = str(np.round(np.mean(nh_mean_error_per),2))  + "\u00B1" + str(np.round((nh_eighty_error[1] - np.mean(nh_mean_error_per)),2))
    if number[2]>n:
        pmerrorsh = str(np.round(np.mean(sh_mean_error_per),2))  + "\u00B1" + str(np.round((sh_eighty_error[1] - np.mean(sh_mean_error_per)),2))
    if number[3]>n:
        pmerrorsp = str(np.round(np.mean(sp_mean_error_per),2))  + "\u00B1" + str(np.round((sp_eighty_error[1] - np.mean(sp_mean_error_per)),2))
    
    plt.figure(figsize = (20,10))
    if number[1]>n:
        sns.histplot(np_mean_error_per, kde = True, label = 'North Pole error in mA :{}'.format(pmerrornp),color  = 'blue')
    if number[0]>n:
        sns.histplot(nh_mean_error_per, kde = True, label = 'North Hemisphere error in mA :{}'.format(pmerrornh),color = 'green' )
    if number[3]>n:
        sns.histplot(sp_mean_error_per, kde = True, label = 'South Pole error in mA :{}'.format(pmerrorsp),color = 'cyan')
    if number[2]>n:
        sns.histplot(sh_mean_error_per, kde = True , label = 'South Hemisphere error in mA :{}'.format(pmerrorsh),color = 'brown')
    
    plt.title(mission_name+'_'+data_start+'_to_'+data_end+'\n overgeneration in Isc - latitude wise')
    plt.xlabel('Overgeneration (in mA)')
    plt.ylabel('Count\nThe number of points at NHemisphere, NPole,\n SHemisphere, SPole are respectively  {}'.format(number))
    plt.legend(loc='upper left', ncols=2)
    results_dir = os.path.join(folder_path, 'Plots//')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'isc_error_latitude_wise.png'
    plt.grid()
    plt.savefig(results_dir+plot_name)
    plot_5 = results_dir+plot_name
    #plt.show()
    print('Success')
    return df1, plot_5, np_eighty_error, sp_eighty_error


def isc_sags_ratio(df1, data_start, data_end, mission_name):
    print('Isc and SAGS ratio')
    df1['isc_ratio'] = df1['isc']/df1['exp_isc']
    plt.figure(figsize = (20,10))
    plt.plot(((df1['isc'][200:400]/df1['exp_isc'][200:400])-1)*100, marker = '*', label = 'Isc ratio')
    plt.plot(((df1['sags'][200:400]/df1['exp_sags'][200:400])-1)*100, marker = '*', label = 'SAGS ratio')
    plt.legend()
    plt.title(mission_name+'_'+data_start+'_Isc and SAGS overgeneration - Isc and SAGS compared', fontsize  =20)
    plt.yticks()
    plt.ylabel('Overgeneration in % ')
    plt.xlabel('Timestamp')
    plt.grid()
    plt.ylim(-1,10)
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'ratio.png'
    plt.savefig(results_dir+plot_name)
    plot_6 = results_dir+plot_name
    #plt.show()
    print('Success')
    return df1, plot_6


def lat_lon_dist_sags(df1, data_start, data_end, mission_name):
    print('Lon-lat plot SAGS')    
    df1['sags_error_per'] = 100 * df1['diff_sags'] / df1['sags']
    df_alb = df1[df1['sun_lit']==True][['lat', 'lon', 'sags_error_per']]
    df_alb_array = df_alb.values
    x = df_alb_array[:, 1]
    y = df_alb_array[:, 0]
    z = df_alb_array[:, 2]
    plt.figure(figsize=(20,10))
    plt.scatter(x, y, c=z, cmap='plasma', s=200, vmin=0, vmax=5)  
    plt.title(mission_name + data_start + '_to_' + data_end + '\nSAGS overgeneration mapped')
    plt.colorbar(label='SAGS overgeneration in %')  
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name + data_start + '_to_' + data_end + 'SAGS_mapped_lat_lon_visualization.png'
    plt.savefig(results_dir+plot_name)
    plot_8 = os.path.join(results_dir, plot_name)
    plt.savefig(results_dir+plot_name)
    #plt.show()
    print('Success')
    return df1, plot_8


def lat_lon_dist_isc(df1, data_start, data_end, mission_name):
    print('Lon-lat plot Isc')
    df1['isc_error_per'] = 100*df1['diff_isc']/df1['isc']
    df_alb = df1[df1['sun_lit']==True][['lat', 'lon', 'isc_error_per']]
    df_alb_array = df_alb.values
    x = df_alb_array[:, 1]
    y = df_alb_array[:, 0]
    z = df_alb_array[:, 2]
    plt.figure(figsize=(20,10))
    plt.scatter(x, y, c=z, cmap='plasma', s=200, vmin=0, vmax=5)  
    plt.title(mission_name + data_start + '_to_' + data_end + '\nI_sc overgeneration mapped')
    plt.colorbar(label='I_sc overgeneration in %')  
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+data_start+'_to_'+data_end+'I_sc_mapped_lat_lon_visualiztion.png'
    plot_9 = results_dir+plot_name
#     fig.write_image(results_dir+plot_name)
    plt.savefig(results_dir+plot_name)
    #plt.show()
    print('Success')
    return df1, plot_9

