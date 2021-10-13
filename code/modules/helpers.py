import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import sys
import os 
<<<<<<< HEAD
import pickle
=======
from zeeman import ZeemanLab as ZL

convert = ZL().convert
>>>>>>> 16bb7def6b883977045bc023bc98c308f9da0715

def add_path():
    sys.path.insert(0,'/root/work/Zeeman_PHYS439/code/modules')
    

def convert_column_all(col_name = 'vh', new_col_name = 'b_mT'):
    for (dirpath, dirnames, filenames) in os.walk('data'):
        if 'converted' not in dirpath:
            ### we don't want to converted the files which have been converted.
            for f in filenames:
                if f.endswith('.csv'):
                    _df =pd.read_csv(dirpath+os.sep+f)
                    if col_name in _df.columns:
                        ### CONVERSION part####

                        _df[new_col_name] = _df[col_name].apply(convert)

                        try:
                            os.mkdir(dirpath+os.sep+'converted')
                        except FileExistsError:
                            continue
                        _df.to_csv(dirpath+os.sep+'converted'+os.sep+f)

                    else:
                        ### Don't have the column we are looking for
                        continue

<<<<<<< HEAD
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
                        
def save_obj(obj, name, directory):
    with open(directory+os.sep+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name,directory):
    with open(directory+os.sep+ name + '.pkl', 'rb') as f:
        return pickle.load(f)
=======

def convert_column(file_path, col_name, new_col_name):
        if 'converted' not in file_path:
            ### we don't want to converted the files which have been converted.
            if file_path.endswith('.csv'):
                _df = pd.read_csv(file_path)

                if col_name in _df.columns:
                    _df[new_col_name] = _df[col_name].apply(convert)

                    try:
                        os.mkdir(os.path.dirname(file_path)+os.sep+'converted')

                    except FileExistsError:
                        pass
                        
                    _df.to_csv(os.path.dirname(file_path)+os.sep+'converted'+\
                    os.sep+os.path.basename(file_path))
                    print('Converted successfully')

                else:
                    ### Don't have the column we are looking for
                    print('Specified column name doesn\'t exist in the .csv file.')


def list_files(startpath):
    """
    gives you a tree structure to the directory
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def get_file_path(f_string):
    possible = []
    for (dirpath, dirnames, filenames) in os.walk('data'):
        for f in filenames:
            if f.endswith('.csv') and f_string in f:
                possible.append(dirpath+os.sep+f)

    if len(possible) >1:
        print(*possible, sep = '\n')
        idx = int(input('Out of these converted files, which do you need: '))

        return possible[idx - 1]

    if len(possible) == 0:
        print('No such file found.')
        return

    if len(possible) == 1:
        return possible[0]

>>>>>>> 16bb7def6b883977045bc023bc98c308f9da0715


