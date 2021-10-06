import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import sys
import os 

def add_path():
    sys.path.insert(0,'/root/work/Zeeman_PHYS439/code/modules')
    

def convert_vb_all(col_name = 'vb', new_col_name = 'b'):

    for (dirpath, dirnames, filenames) in os.walk('data'):

        if 'converted' not in dirpath:
            ### we don't want to converted the files which have been converted.
            for f in filenames:
                if f.endswith('.csv'):

                    _df =pd.read_csv(dirpath+os.sep+f)

                    if col_name in _df.names:
                        ###do something
                    ### CONVERSION part####
                        _df[new_col_name] = _df[col_name].apply(conversion)

                        try:
                            os.mkdir(dirpath+os.sep+'converted')
                        except FileExistsError:
                            continue
                        _df.to_csv(dirpath+os.sep+'converted'+os.sep+f)

                    else:
                        continue
                        


add_path()  ## This is what adds the modules folder to sys.path
