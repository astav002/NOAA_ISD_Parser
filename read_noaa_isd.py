
from operator import add, length_hint
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


CDS_MDS= {
    'var_length': (0, 4),          # begin CDS section
    'usaf_id' : (4, 6), 
    'wban': (10, 5), 
    'date': (15, 8), 
    'gmt': (23, 4),                # "gmt" = Greenwich Mean Time
    'data_source': (27, 1) ,
    'lat': (28, 6) ,
    'long': (34, 7), 
    'report_type': (41, 5), 
    'elev': (46, 5) ,
    'call_letters': (51, 5) ,
    'qc_level': (56, 4) ,
    'wind_dir': (60, 3),             # begin MDS section
    'wind_dir_flag': (63, 1) ,
    'wind_type': (64, 1), 
    'wind_speed': (65, 4) ,
    'wind_speed_flag': (69, 1) ,
    'sky_ceiling': (70, 5), 
    'sky_ceil_flag': (75, 1),
    'sky_ceil_determ': (76, 1), 
    'sky_cavok': (77, 1), 
    'visibility': (78, 6), 
    'vis_flag': (84, 1), 
    'vis_var': (85, 1), 
    'vis_var_flag': (86, 1), 
    'air_temp': (87, 5), 
    'air_temp_flag': (92, 1), 
    'dew_point': (93, 5) ,
    'dew_point_flag': (98, 1), 
    'sea_lev_press': (99, 5), 
    'sea_levp_flag': (104, 1), 
}

add_data = {
    "AA1":{"title": "Precipitation period quanity", 
            "fields": {"pcp_quantity_hours":2,
                       "pcp_depth_dim_mm":4,
                       "pcp_condition_code":1,
                       "pcp_quality_code":1}},
    "AW1":{"title": "Weather Observation", 
            "fields": {"present_wth_obs":2,
                       "quality_code":1}}, 
    "GH1":{"title": "Hourly Solar Data", 
            "fields": {"solarad":5,
                       "solarad_qc":1,
                       "solarad_flag":1,
                       "solarad_min":5,
                       "solarad_min_qc":1,
                       "solarad_min_flag":1,
                       "solarad_max":5,
                       "solarad_max_qc":1,
                       "solarad_max_flag":1,
                       "solarad_std":5,
                       "solarad_std_qc":1,
                       "solarad_std_flag":1}},                                            
}

def parse_add_data(line:str):

    add_results = {}
    for key in add_data.keys():
        try:
            sub = line.split(key)[1]
            prev = 0
            for f_key in add_data[key]["fields"].keys():
                f_length = add_data[key]["fields"][f_key]
                add_results[f_key] = sub[prev:prev+f_length]
                prev = prev+f_length
        except:
            pass
    return add_results
        



def lines_to_dict(fle, lines=2):

    data = []
    f = open(fle, 'r')
    
    for l in f:
        data_hold = dict()
        for key in CDS_MDS.keys():
            start, end = CDS_MDS[key]
            #print("Var {}: Start {} - end {}".format(key, start, end))
            data_hold[key] = l[start:start+end]

        add_dict = parse_add_data(l)
        # if (len(add_dict) > 0):
        #     print(add_dict)
        data.append({**data_hold, **add_dict})
        #data.append(add_dict)

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":

    df = lines_to_dict("C:\\Users\\astav\\Downloads\\723086-93741-2022", lines='all')

    df["pcp_depth_dim_mm"] = pd.to_numeric(df["pcp_depth_dim_mm"].fillna(0))
    df["wind_dir"] = pd.to_numeric(df["wind_dir"])
    fig, ax = plt.subplots(subplot_kw = {'projection':'polar'})
    theta1 = df[df["wind_dir"] != 999]["wind_dir"] / 180 * np.pi
    precip = df[df["wind_dir"] != 999]["pcp_depth_dim_mm"]

    vals, bins = np.histogram(df[df["wind_dir"] != 999]["wind_dir"], bins=36)
    theta = bins[:len(bins)-1]*np.pi / 180
    precip = vals
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.bar(theta, precip, width=360 / 36 * np.pi / 180, alpha=0.5, edgecolor='k')
    print(theta)
    print(precip)
    
    plt.show()

    plt.hist(theta1, bins=16)
    plt.show()
    print(len(df))

