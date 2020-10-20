
"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2020-08-23

Function: Holds cross-project settings and constants.
"""




########### project directories ###########
DATA_DIR = "./data/"                                    # where data files (observations of cyanobacteria) are stored.
COLOCALIZED_DIR = f"{DATA_DIR}colocalized/"             # where the colocalized data files (with evironmental variables) are stored.
COMPILED_DIR = f"{DATA_DIR}compiled/"                   # where the compiled colocalized data files are stored.



#################### data retieval settings #################### 
DEPTH1 = 0          # The lower bound of vertical filter to retrieve the Cyanobacteria observations.
DEPTH2 = 5          # The upper bound of vertical filter to retrieve the Cyanobacteria observations.



########### consistent names for Cyanobacteria studied in the project ###########
PROC = "prochlorococcus_abundance"                      # A consistent label for all "prochlorococcus abundance" related observations.
SYNC = "synechococcus_abundance"                        # A consistent label for all "synechococcus_ abundance" related observations.
PICO = "picoeukaryote_abundance"                        # A consistent label for all "picoeukaryote abundance" related observations.                    


