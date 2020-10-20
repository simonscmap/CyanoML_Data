"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2020-08-19

Function: Holds popular functions that are invoked across the project. 
"""



import os, sys
from settings import PROC, SYNC, PICO
import numpy as np
import pandas as pd
from colorama import Fore, Back, Style, init


def halt(msg):
        """
        Prints an error message and terminates the program.
        """
        msg = '\n' + msg
        init(convert=True)
        print(Fore.RED + msg, file=sys.stderr)    
        print(Style.RESET_ALL, end='')
        sys.exit(1)
        return



def makedir(directory):
    """
    Creates a new directory if doesn't exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return


def cyano_datasets():
    """
    Compiles a list of Cyanobacteria datasets.
    Each element is a tuple representing a dataset where the first element is the table name 
    and the second element is a list of field names to be retrieved. 
    """
    cyanos = []
    cyanos.append(("tblSeaFlow", ["cruise", "abundance_prochloro", "abundance_synecho", "abundance_picoeuk"]))
    cyanos.append(("tblFlombaum", ["prochlorococcus_abundance_flombaum", "synechococcus_abundance_flombaum"]))
    cyanos.append(("tblGlobal_PicoPhytoPlankton", ["prochlorococcus_abundance", "synechococcus_abundance", "picoeukaryote_abundance"]))
    cyanos.append(("tblJR19980514_AMT06_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Zubkov", "synechococcus_abundance_P700A90Z_Zubkov", "picoeukaryotic_abundance_PYEUA00A_Zubkov"]))
    cyanos.append(("tblJR20030512_AMT12_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Zubkov", "synechococcus_abundance_P700A90Z_Zubkov", "picoeukaryotic_abundance_PYEUA00A_Zubkov"]))
    cyanos.append(("tblJR20030910_AMT13_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Zubkov", "synechococcus_abundance_P700A90Z_Zubkov", "picoeukaryotic_abundance_PYEUA00A_Zubkov"]))
    cyanos.append(("tblJR20040428_AMT14_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Zubkov", "synechococcus_abundance_P700A90Z_Zubkov", "picoeukaryotic_abundance_PYEUA00A_Zubkov"]))
    cyanos.append(("tblD284_AMT15_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Zubkov", "synechococcus_abundance_P700A90Z_Zubkov"]))
    cyanos.append(("tblD294_AMT16_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblD299_AMT17_Flow_Cytometry", ["prochlorococcus_abundance_P701A90Z_Zubkov", "synechococcus_abundance_P700A90Z_Zubkov", "picoeukaryotic_abundance_PYEUA00A_Zubkov"]))
    cyanos.append(("tblJR20081003_AMT18_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblJC039_AMT19_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblJC053_AMT20_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblD371_AMT21_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblJC079_AMT22_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblJR20131005_AMT23_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblJR20140922_AMT24_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblJR15001_AMT25_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    cyanos.append(("tblDY110_AMT29_flow_cytometry", ["prochlorococcus_abundance_P701A90Z_Tarran", "synechococcus_abundance_P700A90Z_Tarran", "picoeukaryotic_abundance_PYEUA00A_Tarran"]))
    return cyanos


def environmental_datasets():
    """
    Compiles a dict of environmental vaiables to be colocalized with cyanobacteria measurements.
    Each item key represents the table name of the environmental dataset, and the item's value again is a dict 
    containing the variables names, tolerance parameters, and two flags indicating if the dataset has 'depth' column, 
    and if the dataset represents a climatology product, repectively. The tolerance parametrs specify the temporal [days], 
    latitude [deg], longitude [deg], and depth [m] tolerances, respectively. 
    """
    envs = {
           "tblSST_AVHRR_OI_NRT": {
                                   "variables": ["sst"],
                                   "tolerances": [1, 0.25, 0.25, 5],
                                   "hasDepth": False,
                                   "isClimatology": False
                                   },
           "tblCHL_REP": {
                          "variables": ["chl"],
                          "tolerances": [4, 0.25, 0.25, 5],
                          "hasDepth": False,
                          "isClimatology": False
                          },
           "tblSSS_NRT": {
                          "variables": ["sss"],
                          "tolerances": [1, 0.25, 0.25, 5],
                          "hasDepth": False,
                          "isClimatology": False
                          },
           "tblModis_PAR": {
                            "variables": ["PAR"],
                            "tolerances": [1, 0.25, 0.25, 5],
                            "hasDepth": False,
                            "isClimatology": False
                            },
           "tblAltimetry_REP": {
                                "variables": ["sla", "adt", "ugosa", "vgosa"],
                                "tolerances": [1, 0.25, 0.25, 5],
                                "hasDepth": False,
                                "isClimatology": False
                                },
           "tblPisces_NRT": {
                             "variables": ["NO3", "PO4", "Fe", "O2", "Si", "PP"],
                             "tolerances": [4, 0.5, 0.5, 5],
                             "hasDepth": True,
                             "isClimatology": False
                             },
           "tblWOA_Climatology": {
                                  "variables": ["density_WOA_clim", "salinity_WOA_clim", "nitrate_WOA_clim", "phosphate_WOA_clim", "silicate_WOA_clim", "oxygen_WOA_clim"],
                                  "tolerances": [1, 0.75, 0.75, 5],
                                  "hasDepth": True,
                                  "isClimatology": True
                                  }
           }
    return envs


def env_vars():
    """
    Reurns a list of environmental variables to be colocalized with cyano observations.
    """
    envs = environmental_datasets()
    vars = []
    for _, env in envs.items():
        vars += env["variables"]
    return vars    


