import pandas as pd
import numpy as np

def z_transform(theta) -> np.array:
    # theta = np.deg2rad(theta)
    return np.array([
        [np.cos(theta), np.sin(theta), 0],
        [-np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

def get_lat_lon(df1):
    print('Getting lat and lon')
    x = df1['sc_x_pos'] # example x-coordinate in km
    y = df1['sc_y_pos'] # example y-coordinate in km
    z = df1['sc_z_pos'] # example z-coordinate in km
    
    sidAng = 3.158594230000000*180/np.pi # rad
    sidEpoch = pd.Timestamp("2024-3-23 0:0:0.0")
    siderial_rate = 1.140792231481478e-05 + 360/86400 # deg/s
    
    df1['Sidereal (rad)'] = np.deg2rad( (sidAng  + siderial_rate * ((df1.index - sidEpoch)/np.timedelta64(1, 's'))) % 360 )
    
    for i in range(0, len(df1)):
        sat_pos_vec = np.array([    x[i],
                                    y[i],
                                    z[i]])

        sat_pos_vec = np.reshape(sat_pos_vec, (3, -1))
        sat_pos_vec = np.dot(z_transform(df1['Sidereal (rad)'][i]), sat_pos_vec)        # in the ECEF frame
        x[i] = sat_pos_vec[0]
        y[i] = sat_pos_vec[1]
        z[i] = sat_pos_vec[2]
    longitude = np.arctan2(y, x)
    altitude = np.sqrt(x*x + y*y + z*z)
    latitude = np.arcsin(z/altitude)
    
    df1['lon'] = (longitude)*180/np.pi
    df1['lat'] = (latitude)*180/np.pi
    df1['alt'] = (altitude) - 6371
    print('Success')
    return df1