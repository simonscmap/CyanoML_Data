"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2020-08-19

Function: Retrieve Cyanobacteria measurements in CMAP and store them on local disk.
"""



import pycmap
from settings import DEPTH1, DEPTH2, DATA_DIR
from config.config import API_KEY
from common import makedir, cyano_datasets


def retrieve(api, dataset, depth1, depth2):
    table, fields = dataset[0], ", ".join(dataset[1])
    hasDepth = api.has_field(table, "depth")
    if hasDepth: 
        fields = f" [time], lat, lon, depth, {fields} "
        whereClause = f" WHERE depth BETWEEN {depth1} AND {depth2} "
    else:        
        fields = f" [time], lat, lon, {fields} "
        whereClause = ""
    query = f"SELECT {fields} FROM {table} {whereClause}"
    return api.query(query)



def main():
    """
    Iterates through the list of datasets containing measurements of cyanobacteria.
    The measurements are retrieved and stored in individual csv files on local disk.
    """
    api = pycmap.API(token=API_KEY)
    makedir(DATA_DIR)
    cyanos = cyano_datasets()
    for dataset in cyanos:
        print("\n********************************")
        print("Downloading ", dataset, " ...")
        print("********************************\n")
        data = retrieve(api, dataset, DEPTH1, DEPTH2)
        data.to_csv(f"{DATA_DIR}{dataset[0]}.csv", index=False)







#######################################
#                                     #
#                                     #
#                 main                #
#                                     #
#                                     #
#######################################

if __name__ == "__main__":    
    main()    
