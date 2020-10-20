

# Simons CMAP Article: Case Study
This repository contains a few Python scripts demonstrating how to retrieve and colocalize data sets.
The resulting colocalized data sets are then used to train a predictive machine learning model for sea surface cell abundance of Cyanobacteria Prochlorococcus, Synechococcus, and Picoeukaryotes. 



## Usage
Before running any of the scripts, register at https://simonscmap.com/ and get an API_KEY. Store your API_KEY in the `./config/config.py` file.

`collect.py` retrieves a predefined list of data sets that contain measurements of Cyanobacteria abundances. The retrieved data sets are stored at `./data/` directory in form of csv files.

`colocalize.py` colocalizes the retrieved data sets with a given number of ancillary environmental variables. The colocalized data sets are stored at `./data/colocalied/` directory in form of csv files.

`compiler.py` concatenates the colocalized data sets in form of a single csv file at `./data/compiled/` directory.



## Dependency
[pycmap](https://github.com/simonscmap/pycmap)



