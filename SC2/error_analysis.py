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
warnings.filterwarnings('ignore')

folder_path = os.getcwd()


def get_error(df1):
    print('Obtaining error')
    df1['diff_sags'] = df1['sags'] - df1['exp_sags']
    df1['sags_error_per'] = df1['diff_sags']/df1['exp_sags']
    error_per_sags = (np.mean(df1[(abs(df1['lat'])<40) & (df1['sun_lit']==True) & (df1['PL']==False)]['sags_error_per'].values))
    print('Success')
    return df1, 100*error_per_sags


def plot_sags(df1, mission_name, data_start, data_end):
    print('SAGS time-series plot')
    plt.figure(figsize = (20,10))
    plt.plot(df1['exp_sags'][:300], label = 'estimated SAGS', marker = '*')
    plt.plot(df1['sags'][:300], label = 'observed SAGS', marker = '*')
    plt.title(mission_name+'_'+data_start+'_to_'+data_end+' \nestimation and observation of SAGS current')
    plt.xticks(rotation = 45)
    plt.grid()
    plt.xlabel('Timestamp')
    plt.ylim(0,75)
    plt.legend()
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'_SAGS_estimation_vs_observation.png'
    plt.savefig(results_dir+plot_name)
    plot_1 = results_dir+plot_name
    #plt.show()
    print('Success')
    return plot_1
    


# In[139]:


def plot_sags_error(df1, mission_name, data_start, data_end):
    print('SAGS error plot')
    error_per_sags = 100*df1['sags_error_per'][(df1['sun_lit']==True) & (df1['PL']==False)].values
    mean_error_per_sags = []
    for i in range(2000):
        mean_error_per_sags.append(np.random.choice(error_per_sags, size = 400).mean())
        i = i+1
    mean_error_sags = np.array(mean_error_per_sags).mean()
    eighty_error_sags = (np.round(np.quantile(mean_error_per_sags, 0.05),2), np.round(np.quantile(mean_error_per_sags, 0.95),2))
    pmerror_sags = str(np.round(mean_error_sags,2))  + "\u00B1" + str(np.round((eighty_error_sags[1] - mean_error_sags),2))
    plt.figure(figsize = (20,10))
    sns.histplot(mean_error_per_sags, kde = True, label = 'Error in prediction', color = 'magenta')
    plt.title(mission_name+'_'+data_start+'_to_'+data_end+' percentage error\n in SAGS estimation and observation')
    plt.xlabel('Error (in %)')
    plt.ylabel('Count')
    plt.axvline(eighty_error_sags[0], ls = '--', color = 'red')
    plt.axvline(eighty_error_sags[1], ls = '--', color = 'red')
    plt.grid()
    plt.annotate('The mean of error percent\n with 90% confidence\n is in {}'.format(pmerror_sags), xy = (eighty_error_sags[0],50))
    results_dir = os.path.join(folder_path, 'Plots/')
    plot_name = mission_name+'_'+data_start+'_to_'+data_end+'sags_error_percent_distribution.png'
    plt.savefig(results_dir+plot_name)
    plot_2 =results_dir+plot_name
    #plt.show()
    print('Success')
    return plot_2,eighty_error_sags

def valid_points_error(df1):
    print('Non-polar points error')
    pole_def = 50
    all_points = 100*df1['sags_error_per'][(abs(df1['lat'])<pole_def) & (df1['sun_lit']==True) & (df1['PL']==False)]
    mean_error_per_valid_sags = []
    for i in range(2000):
        mean_error_per_valid_sags.append(np.random.choice(all_points, size = 400).mean())
        i = i+1
    mean_error_valid_sags = np.array(mean_error_per_valid_sags).mean()
    eighty_error_valid_sags = (np.round(np.quantile(mean_error_per_valid_sags, 0.05),2), np.round(np.quantile(mean_error_per_valid_sags, 0.95),2))
    print('Success')
    return mean_error_valid_sags, eighty_error_valid_sags

