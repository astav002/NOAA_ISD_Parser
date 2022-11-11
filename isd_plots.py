import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os



class PlotISD():

    def __init__(self, **kwargs):

        if "data_dir" in kwargs:
            self.base_dir = kwargs["data_dir"]
        else:
            self.base_dir = os.path.join(os.getcwd(), "data_files")

    def load_df(self, fle):

        df = pd.read_csv(os.path.join(self.base_dir, fle), dtype=object)
        return df

    def set_column_formats(self, df:pd.DataFrame):
        
        df["DATE_TIME"] = pd.to_datetime(df.apply(lambda x: str(x["date"]) + " " +str(x["gmt"]), axis=1), format="%Y%m%d %H%M")
        # adjust by scaling factors
        df["pcp_depth_dim_mm"] = pd.to_numeric(df["pcp_depth_dim_mm"]) / 10
        df["wind_speed"] = pd.to_numeric(df["wind_speed"])
        df["air_temp"] = pd.to_numeric(df["air_temp"])
        df["sea_lev_press"] = pd.to_numeric(df["sea_lev_press"])
        return df

    def plot_wind(self, df):


        
        df["wind_dir"] = pd.to_numeric(df["wind_dir"])
        fig, ax = plt.subplots(subplot_kw = {'projection':'polar'})
        theta1 = df[df["wind_dir"] != 999]["wind_dir"] / 180 * np.pi
        #precip = df[df["wind_dir"] != 999]["pcp_depth_dim_mm"]

        # vals, bins = np.histogram(df[df["wind_dir"] != 999]["wind_dir"], bins=36)
        # theta = bins[:len(bins)-1]*np.pi / 180
        # precip = vals
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        # ax.bar(theta, precip, width=360 / 36 * np.pi / 180, alpha=0.5, edgecolor='k')
        # print(theta)
        # print(precip)
        
  

        ax.hist(theta1, bins=16, edgecolor='k', alpha=0.5, align='mid')
        plt.show()
  

def main():

    isd = PlotISD()
    
    isd_df = isd.load_df("723086-93741-2018.csv")
    isd_df = isd.set_column_formats(isd_df)
    isd.plot_wind(isd_df)  



    plt.figure()
    plt.plot(isd_df["DATE_TIME"], isd_df["pcp_depth_dim_mm"])
    # isd_df = isd_df[isd_df["wind_speed"] < 999]
    # isd_df = isd_df[isd_df["air_temp"] < 999]
    # isd_df = isd_df[isd_df["sea_lev_press"] < 99999]
    # # plt.plot(isd_df["DATE_TIME"], isd_df["wind_speed"])
    # plt.plot(isd_df["DATE_TIME"], isd_df["air_temp"]/isd_df["air_temp"].max())
    # plt.plot(isd_df["DATE_TIME"], isd_df["sea_lev_press"]/isd_df["sea_lev_press"].max())
    plt.show()
    
    print(isd_df.describe())

if __name__ == "__main__":

    main() 