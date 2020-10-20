"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2020-08-19

Function: Colocalize cyanobacteria observations with a given list of environmental variables hosted by the CMAP database.
"""



import os, glob
import concurrent.futures
import pycmap
from config.config import API_KEY
from settings import DATA_DIR, COLOCALIZED_DIR
from common import halt, makedir, environmental_datasets
import pandas as pd
import datetime
from dateutil.parser import parse



def cyano_csv_files(cyanoDir):
    """
    Returns a list of path to csv files that hold observations of cyanobacteria.
    """
    return glob.glob(f"{cyanoDir}*.csv")


def add_env_columns(df, envs):
    """
    Adds new columns to the dataframe form each environmental variable.
    """
    for env in envs.values():
        for v in env.get("variables"):
            if v not in df.columns: df[v] = None
    return df
    

def add_env_temporal_coverage(api, envs):
    """
    Adds new entries to the envs dictionary indicating the temporal coverage of each environmental dataset.
    """
    for table, env in envs.items():
        df = api.query(f"SELECT MIN([time]) startTime, MAX([time]) endTime FROM {table}")
        if len(df) > 0:
            envs[table]["startTime"] = df.loc[0, "startTime"]
            envs[table]["endTime"] = df.loc[0, "endTime"]
    return envs


def match(df, api, envs, cyanoFile, rowCount):
    """
    Takes a single-row dataframe containing cyano observations and colocalizes with the 
    environmental variables included in the `envs` argument. The tolerance parametrs 
    are also included in the `envs` argument.
    """ 
    def get_month(dt):
        return parse(dt).month

    def shift_dt(dt, delta):
        delta = float(delta)
        dt = parse(dt)
        dt += datetime.timedelta(days=delta)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def in_time_window(sourceDT, targetMinDT, targetMaxDT):
        targetMinDT = targetMinDT.split(".000Z")[0]
        targetMaxDT = targetMaxDT.split(".000Z")[0]
        return not (
                    parse(sourceDT) < parse(targetMinDT) or 
                    parse(sourceDT) > parse(targetMaxDT)
                    )

    def construc_query(table, env, t, lat, lon, depth):
        variables = env["variables"] 
        timeTolerance = env["tolerances"][0] 
        latTolerance = env["tolerances"][1] 
        lonTolerance = env["tolerances"][2]  
        depthTolerance = env["tolerances"][3]  
        hasDepth = env["hasDepth"] 
        isClimatology = env["isClimatology"]
        inTimeRange = True
        if not isClimatology:
            startTime = env["startTime"]
            endTime = env["endTime"]    
            inTimeRange = in_time_window(t, startTime, endTime)
        selectClause = "SELECT " + ", ".join([f"AVG({v}) {v}" for v in variables]) + " FROM " + table
        timeClause = f" WHERE [time] BETWEEN '{shift_dt(t, -timeTolerance)}' AND '{shift_dt(t, timeTolerance)}' "
        if not inTimeRange or isClimatology: timeClause = f" WHERE [month]={get_month(t)} "
        latClause = f" AND lat BETWEEN {lat-latTolerance} AND {lat+latTolerance} "
        lonClause = f" AND lon BETWEEN {lon-lonTolerance} AND {lon+lonTolerance} "
        depthClause = f" AND depth BETWEEN {depth-depthTolerance} AND {depth+depthTolerance} "
        if not hasDepth: depthClause = ""                
        return selectClause + timeClause + latClause + lonClause + depthClause        


    if len(df) != 1: halt(f"Invalid dataframe input.\nExpected a single row dataframe but received {len(df)} rows.")
    rowIndex = df.index.values[0]
    df.reset_index(drop=True, inplace=True)
    t= df.iloc[0]["time"]
    lat = df.iloc[0]["lat"]
    lon = df.iloc[0]["lon"] 
    depth = 0
    if 'depth' in df.columns: depth = df.iloc[0]["depth"]
    for table, env in envs.items():
        print(f"{rowIndex} / {rowCount-1}\n\t{datetime.datetime.now()}: Colocalizing {table} with {cyanoFile} ...")
        query = construc_query(table, env, t, lat, lon, depth)
        matchedEnv = api.query(query)
        if len(matchedEnv)>0:
            for v in env["variables"]: df.at[0, v] = matchedEnv.iloc[0][v] 
    return df



def main():
    """
    Iterates through the list of cyano datasets and colocalizes them with the specified environmentl variables.
    Colocalized datasets are stored in the "COLOCALIZED_DIR" as csv files.
    """
    def saveColocalizedCSV(df):
        df.to_csv(f"{COLOCALIZED_DIR}{os.path.basename(cyanoFile)}", index=False) 

    cyanoFiles = cyano_csv_files(DATA_DIR)
    api = pycmap.API(token=API_KEY)
    makedir(COLOCALIZED_DIR)
    envs = environmental_datasets()        
    envs = add_env_temporal_coverage(api, envs)

    for cyanoFile in cyanoFiles:
        df = pd.read_csv(cyanoFile)
        df = add_env_columns(df, envs)
        dfs = [df.loc[i].to_frame().T for i in range(len(df))]
        colocalizedDF  = pd.DataFrame({})
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futureObjs = executor.map(match, dfs, [api] * len(dfs), [envs] * len(dfs), [cyanoFile] * len(dfs), [len(dfs)] * len(dfs))
            for fo in futureObjs:
                if len(colocalizedDF) < 1:
                    colocalizedDF = fo
                else:
                    colocalizedDF = pd.concat([colocalizedDF, fo], ignore_index=True)  
        saveColocalizedCSV(colocalizedDF)


                    

#######################################
#                                     #
#                                     #
#                 main                #
#                                     #
#                                     #
#######################################


if __name__ == "__main__":
    main()    