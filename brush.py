# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------

CSV_PATHS = {'a': os.path.join("csv", "data_annual.txt")
            ,'q': os.path.join("csv", "data_quarter.txt") 
            ,'m': os.path.join("csv", "data_monthly.txt") }

# -----------------------------------------------------------------------------
# Import data 

def read_dataframes(paths = CSV_PATHS):

    def to_ts(year):
        return pd.Timestamp(datetime(int(year),12,31))        
        
    dfa = pd.read_csv(paths['a'], converters = {'year':to_ts}, index_col = 'year')    
    dfq = pd.read_csv(paths['q'], converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
    dfm = pd.read_csv(paths['m'], converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
    return dfa, dfq, dfm

DFA, DFQ, DFM =  read_dataframes() 


# -----------------------------------------------------------------------------
# TODO: Add BRENT




# -----------------------------------------------------------------------------
# Brush/transform data, add variables
       
def deaccumulate(df):
    df2 = df.copy()
    for i in range(len(df)):
        if df.index[i].month > 1:
            df2.iloc[i] = df.iloc[i]-df.iloc[i-1]
        else: 
            df2.iloc[i] = df.iloc[i] 
    return df2

rev = deaccumulate(DFM["GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub"])
exp = deaccumulate(DFM["GOV_CONSOLIDATED_EXPENSE_ACCUM_bln_rub"])            
DFM["GOV_CONSOLIDATED_EXPENSE_bln_rub"] = exp
DFM["GOV_CONSOLIDATED_REVENUE_bln_rub"] = rev
DFM["GOV_CONSOLIDATED_DEFICIT_bln_rub"] = rev-exp

fed = deaccumulate(DFM["GOV_FEDERAL_SURPLUS_ACCUM_bln_rub"])
subfed = deaccumulate(DFM["GOV_SUBFEDERAL_SURPLUS_ACCUM_bln_rub"])

DFM["GOV_FEDERAL_SURPLUS_bln_rub"] = fed 
DFM["GOV_SUBFEDERAL_SURPLUS_bln_rub"] = subfed
DFM["GOV_CONSOLIDATED_SURPLUS_bln_rub"] = fed + subfed 


ex = DFM["TRADE_GOODS_EXPORT_bln_usd"]
im = DFM["TRADE_GOODS_IMPORT_bln_usd"]
DFM["TRADE_GOODS_NET_EXPORT_bln_usd"] = ex-im

# todo:
#     get annual values from monthly 
#     get quarterly values from monthly 


profits = ["NONFINANCIALS_PROFIT_CONSTRUCTION_bln_rub", "NONFINANCIALS_PROFIT_MANUF_bln_rub",
           "NONFINANCIALS_PROFIT_MINING_bln_rub", "NONFINANCIALS_PROFIT_POWER_GAS_WATER_bln_rub",
           "NONFINANCIALS_PROFIT_TRANS_COMM_bln_rub"]

for df in [DFA, DFQ]:
    df["NONFINANCIALS_PROFIT_EX_AGRO_bln_rub"] = df[profits].sum(axis=1) / 1000

inv = DFA[["NONFINANCIALS_PROFIT_EX_AGRO_bln_rub", "I_bln_rub"]]

