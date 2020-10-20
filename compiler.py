"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2020-08-22

Function: Compiles all of the colocalized cyano datasets into a single csv file.
"""



import os, sys, glob
import pycmap
from config.config import API_KEY
from settings import PROC, SYNC, PICO, COLOCALIZED_DIR, COMPILED_DIR
from common import halt, makedir, env_vars
import pandas as pd




def scale_factor(table):
    """
    Multiplies the cyano abundance measurements with a constant factor. 
    For example: 
    The Seaflow dataset reports the abundance values in units of cell/uL while 
    all other datasets are in cell/mL. This means that seaflow abundance values 
    should be multiplied with a 1000 factor.
    """ 
    factor = 1
    table = table.lower()
    if table.find('seaflow') != -1: factor = 1000
    return factor



def rename_cyano_columns(df):
    """
    Renames the cyano abundance column titles to predefined values.
    """ 
    cols = list(df.columns)
    for i, col in enumerate(df.columns):
        if col.lower().find("pro") != -1 and col.lower().find("abun") != -1:     # prochlorococcus abundance
            cols[i] = PROC
        elif col.lower().find("syn") != -1 and col.lower().find("abun") != -1:   # synechococcus abundance
            cols[i] = SYNC
        elif col.lower().find("pico") != -1 and col.lower().find("abun") != -1:  # picoeukaryote abundance
            cols[i] = PICO
    df.columns = cols        
    return df.columns        


def insert_column(df, colTitle, colIndex, fillValue):
    """
    Inserts a new column `colTitle`, to the dataframe `df` at location `colIndex` with initial value `fillValue`.
    """
    if colTitle not in df.columns:
        df.insert(colIndex, colTitle, fillValue, True)
    return df    


def unify(cyanoFile):
    """
    Takes a colocalized cyano filepath and ensures that it will have identical columns as other colocalized files.
    It also ensures that all cyano observations are in the same units [cell/ml].
    """
    # columns:
    # time | lat | lon | depth | table | cruise | <PROC> | <SYNC> | <PICO> | env_var1 | ... | env_var_n     
    df = pd.read_csv(cyanoFile)
    table = os.path.splitext(os.path.basename(cyanoFile))[0]
    df.columns = rename_cyano_columns(df)

    df = insert_column(df, "depth", 3, 0)
    df = insert_column(df, "table", 4, table)
    df = insert_column(df, "cruise", 5, None)
    df = insert_column(df, PROC, 6, None)
    df = insert_column(df, SYNC, 7, None)
    df = insert_column(df, PICO, 8, None)

    columns = ["time", "lat", "lon", "depth", "table", "cruise", PROC, SYNC, PICO] + env_vars()
    if list(df.columns) != columns:    
        print(df.columns)
        halt(f"Invalid columns:\n{cyanoFile}")

    factor = scale_factor(table)
    df[PROC] = factor * df[PROC]
    df[SYNC] = factor * df[SYNC]
    df[PICO] = factor * df[PICO]

    df = df[columns]
    return df

     


def main():
    """
    Iterates through the list of colocalized cyano datasets and compile them into a single csv file.
    The compiled file is stored in the "COMPILED_DIR" as a csv file.
    """
    print(
        """

            ##########################################################
            #                                                        #
            #                                                        #
            #         Compiling Colocalized Cyano Datasets           #
            #                                                        #
            #                                                        #
            ##########################################################

            
        """
    )
    cyanoFiles = glob.glob(f"{COLOCALIZED_DIR}*.csv")
    makedir(COMPILED_DIR)
    dfCompiled  = pd.DataFrame({})
    for cyanoFile in cyanoFiles:
        print(f"Compiling {cyanoFile}")
        data = unify(cyanoFile)
        if len(dfCompiled ) < 1:
            dfCompiled = data
        else:
            dfCompiled = pd.concat([dfCompiled, data], ignore_index=True)    
    dfCompiled.to_csv(f"{COMPILED_DIR}compiled.csv", index=False)        

                    

#######################################
#                                     #
#                                     #
#                 main                #
#                                     #
#                                     #
#######################################


if __name__ == "__main__":
    main()                        