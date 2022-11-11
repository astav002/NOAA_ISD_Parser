

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import requests
from isd_vars import CDS_MDS, ADD_DATA
import gzip



class ISDParser():

    def __init__(self):
        self.add_data = ADD_DATA
        self.CDS_MDS = CDS_MDS
        self.host_name = "http://www1.ncdc.noaa.gov" #/pub/data/noaa
        self.isd_path = "/pub/data/noaa/"
        self.raw_data_path = ""




    def collect_noaa_isd(self, data_string:str, data_year:str, save_raw:bool=False)->str:
        
        url = self.host_name + self.isd_path + data_year +"/"+data_string+"-"+data_year +".gz"
        r = requests.get(url=url)

        data = gzip.decompress(r.content)
        

        # save the data uncompressed.
        if save_raw:
            f_path= os.path.join(os.getcwd(), data_string+"-"+data_year+".txt")
            self.raw_data_path = f_path
            with open(f_path, 'wb') as f:

                f.write(data)
                f.close


        return data



    def parse_add_data(self, line:str):
        

        add_results = {}
        for key in self.add_data.keys():
            try:
                sub = line.split(key)[1]
                prev = 0
                for f_key in self.add_data[key]["fields"].keys():
                    f_length = self.add_data[key]["fields"][f_key]
                    add_results[f_key] = sub[prev:prev+f_length]
                    prev = prev+f_length
            except:
                pass
        return add_results
            

    def load_noaa_from_file(self):

        
        f = open(self.raw_data_path, 'r')

        return f

    def lines_to_dict(self, raw_data):

        data = []
        
        f = raw_data
        for l in f:
            data_hold = dict()
            for key in self.CDS_MDS.keys():
                start, end = self.CDS_MDS[key]
                #print("Var {}: Start {} - end {}".format(key, start, end))
                data_hold[key] = str(l[start:start+end], encoding='utf-8')

            # now we'll need to run throught he additional data field for the line
            add_dict = self.parse_add_data(str(l, encoding='utf-8'))
            # if (len(add_dict) > 0):
            #     print(add_dict)
            data.append({**data_hold, **add_dict})
            #data.append(add_dict)

        df = pd.DataFrame(data)
        return df



def main(station, year, from_ftp=True, fle_path=os.getcwd(), output_path=os.getcwd()):
    isd = ISDParser()

    if (from_ftp):
        noaa_data = isd.collect_noaa_isd(station, year, save_raw=False)
        noaa_data = noaa_data.splitlines()
    else:
        # set the raw data path first
        isd.raw_data_path = fle_path + station + "-" + year + ".txt"

        # returns the file object but it is iterable
        noaa_data = isd.load_noaa_from_file()
    
    df = isd.lines_to_dict(noaa_data)

    df.to_csv(os.path.join(output_path, "data_files", station + "-" + year + ".csv"))
    
 




if __name__ == "__main__":

    parser = ArgumentParser()


    parser.add_argument("-s", "--site", dest="site_id", 
                        default="723086-93741",
                        help="USAF WBAN site identification") 

    parser.add_argument("-y", "--year", dest="data_year", 
                        default="2022",
                        help="Year of data collection")

    parser.add_argument("-i", "--input", dest="input_file",
                        default="723086-93741-2022"
                        )

                                                                    
    pargs = vars(parser.parse_args())

    
    main(pargs["site_id"], pargs["data_year"])



           



