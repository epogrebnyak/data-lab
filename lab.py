# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------

CSV_PATHS = {'a': os.path.join("csv", "data_annual.txt")
            ,'q': os.path.join("csv", "data_quarter.txt") 
            ,'m': os.path.join("csv", "data_monthly.txt") }

DEFAULT_START_YEAR = 2011

DIRS = {".png":"png", ".xls":"xls"}

MY_DPI = 96

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

#
# todo:
#     get annual values from monthly 
#     get quarterly values from monthly 
#


# -----------------------------------------------------------------------------

class Indicators():

    def __init__(self, groupname, labels, freq=None, start=None, end=None,
                 default_start_year=DEFAULT_START_YEAR):

        self.basename = groupname                     

        if not start:   
           start = str(default_start_year) + "-01"               

        self.dfa = self.make_df(labels, "a", start, end)
        self.dfq = self.make_df(labels, "q", start, end)
        self.dfm = self.make_df(labels, "m", start, end)
        
        if not freq:
           self.df = self.dfm            
        elif freq in "aqm":
           self.freq = freq
           self.df  = {"a":self.dfa,"q":self.dfq,"m":self.dfm}[freq]  
        else:
           raise Exception("Wrong frequency: " + str(freq)) 
      
    def make_df(self, labels, freq, start, end,  
                dfs={'a': DFA, 'q': DFQ, 'm': DFM}):
        df = dfs[freq]        
        filtered_labels = [x for x in labels if x in df.columns] 
        df = df[filtered_labels].loc[start:end,:]
        if df.empty:
            df["None"]=0
            print("Warning: missing data in", ",".join(labels))
        return df
                   
          
    def to_png(self, my_dpi = MY_DPI, dirs = DIRS):    
        ext = ".png"
        path = os.path.join(dirs[ext], self.freq + "_" + self.basename + ext)
        if not self.df.empty:
            ax = self.df.plot(figsize=(600/my_dpi, 450/my_dpi))
            fig = ax.get_figure()
            fig.savefig(path, dpi = MY_DPI)
            fig.clear()
        return "<img src=\"{0}\">".format(path)                             
        
    def to_excel(self, dirs = DIRS):        
        ext = ".xls"
        path = os.path.join(dirs[ext], self.basename + ext) 
        with pd.ExcelWriter(path) as writer:
           self.dfa.to_excel(writer, sheet_name='Annual')
           self.dfq.to_excel(writer, sheet_name='Quarterly')
           self.dfm.to_excel(writer, sheet_name='Monthly') 
        # todo: clean first column in xls file  
        return "<a href=\"{0}\">{1}</a>".format(path, self.basename + ext)                         
      
    def dump(self):
        self.to_png()
        self.to_excel()


def png_html_stream(groups, freq): 
    for group_names in groups:
        g1, g2 = group_names
        msg1 = Indicators(g1, indicator_collection[g1], freq).to_png()
        if g2:
           msg2 = Indicators(g2, indicator_collection[g2], freq).to_png()
        else:
           msg2 = ""
        yield(msg1)
        yield(msg2)
        yield("<BR>")
        
def make_xls(indicator_collection):
    
    for col in indicator_collection.keys():    
        print(col)
        msg1 = Indicators(col, indicator_collection[col], start="1999-01").to_excel()
        yield(msg1)
        yield("<BR>")

def to_html(filename, gen):
    with open(filename, "w") as html_file:
        html_file.write("<HTML>\n<BODY>\n")
        html_file.write("<a href=\"annual.html\">По годам</a> \
                         <a href=\"quarterly.html\">По кварталам</a> \
                         <a href=\"index.html\">По месяцам</a><br><br>\
                         <a href=\"xls.html\">Файлы Excel</a> \
                         <a href=\"https://github.com/epogrebnyak/data-rosstat-kep/blob/master/output/varnames.md\">\
                         Названия переменных</a><br><br>\n")
        for s in gen:
            html_file.write(s)
        html_file.write("</BODY>\n</HTML>")
        

if __name__ == "__main__":
    
    indicator_collection = {
      "CPI":["CPI_rog", "CPI_NONFOOD_rog", "CPI_FOOD_rog", "CPI_SERVICES_rog"]
    , "GDP":["I_yoy", "GDP_yoy", "IND_PROD_yoy", "RETAIL_SALES_yoy"]
    , "GOV":["GOV_CONSOLIDATED_EXPENSE_bln_rub", "GOV_CONSOLIDATED_REVENUE_bln_rub", "GOV_CONSOLIDATED_DEFICIT_bln_rub"]
    , "GOV2": ["GOV_FEDERAL_SURPLUS_bln_rub", "GOV_SUBFEDERAL_SURPLUS_bln_rub", "GOV_CONSOLIDATED_SURPLUS_bln_rub"]
    , "FX" :["RUR_EUR_eop", "RUR_USD_eop" ]
    , "BOP":["TRADE_GOODS_EXPORT_bln_usd", "TRADE_GOODS_IMPORT_bln_usd", "TRADE_GOODS_NET_EXPORT_bln_usd"]
    , "CREDIT":["CREDIT_TOTAL_bln_rub", "CORP_DEBT_bln_rub"]
    , "REAL":["TRANS_bln_t_km", "CONSTR_bln_rub_fix"]
    , "REAL2":["TRANS_RAILLOAD_mln_t", "PROD_E_TWh"]
    }
    
    groups = [("GDP", "CPI"), 
              ("GOV", "GOV2"),
              ("FX", None), 
              ("BOP", "CREDIT"), 
              ("REAL", "REAL2")]
     
    pages = {"m":"index.html"
       , "a":"annual.html"
       , "q":"quarterly.html"}
       
       
    for freq in "aqm": 
       pass        
       gen = png_html_stream(groups, freq)
       to_html(pages[freq], gen)

    gen = make_xls(indicator_collection)
    to_html("xls.html", gen)
    # todo: also generate annual/monthly/qtr total file with group by name
            
            
## gdp   ВВП
## cpi   инфляция
## fx    курс
## pb    платежный баланс 
## cap   инвестиции
## hh    доходы и расходы населения
## gov   госрасходы 
## oil   нефть
#
#
## FINAL USE:
##
##
#
## EVALUATE:
##     не надо обрезать ряды на стадии хранения данных, нужно только для рисунков
##     for testing must have different frequencies a and q and m
##     страница html с месяцами, кварталами и годами + сохранить 
##     все сохранять
##     сразу делать app в интернете
#
## TODO 1:
##     завести нефть 
##     обрабатывать значения (разности и темпы роста) - для создания новых переменных
#
## TODO 2:
##     снимать сезонность
##     сделать инерционный прогноз
#
## ENHANCE:
##     подписи осей графика + количество белого

"""
Timeseries (131):
AGRO_PRODUCTION_rog                          CONSTR_bln_rub_fix                          
CONSTR_rog                                   CONSTR_yoy                                  
CORP_DEBT_OVERDUE_BUDGET_bln_rub             CORP_DEBT_OVERDUE_SUPPLIERS_bln_rub         
CORP_DEBT_OVERDUE_bln_rub                    CORP_DEBT_bln_rub                           
CORP_RECEIVABLE_OVERDUE_BUYERS_bln_rub       CORP_RECEIVABLE_OVERDUE_bln_rub             
CORP_RECEIVABLE_bln_rub                      CPI_ALCOHOL_rog                             
CPI_FOOD_BASKET_rog                          CPI_FOOD_BASKET_rub                         
CPI_FOOD_BASKET_ytd                          CPI_FOOD_rog                                
CPI_NONFOOD_rog                              CPI_RETAIL_BASKET_rog                       
CPI_RETAIL_BASKET_rub                        CPI_RETAIL_BASKET_ytd                       
CPI_SERVICES_rog                             CPI_rog                                     
CREDIT_TOTAL_bln_rub                         DWELL_mln_m2                                
DWELL_rog                                    DWELL_yoy                                   
GDP_bln_rub                                  GDP_yoy                                     
GOV_CONSOLIDATED_DEFICIT_bln_rub             GOV_CONSOLIDATED_DEFICIT_gdp_percent        
GOV_CONSOLIDATED_EXPENSE_ACCUM_bln_rub       GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub      
GOV_FEDERAL_EXPENSE_ACCUM_bln_rub            GOV_FEDERAL_REVENUE_ACCUM_bln_rub           
GOV_FEDERAL_SURPLUS_ACCUM_bln_rub            GOV_SUBFEDERAL_EXPENSE_ACCUM_bln_rub        
GOV_SUBFEDERAL_REVENUE_ACCUM_bln_rub         GOV_SUBFEDERAL_SURPLUS_ACCUM_bln_rub        
HH_FINANCE_DEPOSITS_SBERBANK_bln_rub         HH_FINANCE_DEPOSITS_bln_rub                 
HH_REAL_DISPOSABLE_INCOME_yoy                IND_PROD_rog                                
IND_PROD_yoy                                 IND_PROD_ytd                                
I_bln_rub                                    I_rog                                       
I_yoy                                        NONFINANCIALS_PROFIT_CONSTRUCTION_bln_rub   
NONFINANCIALS_PROFIT_MANUF_bln_rub           NONFINANCIALS_PROFIT_MINING_bln_rub         
NONFINANCIALS_PROFIT_POWER_GAS_WATER_bln_rub NONFINANCIALS_PROFIT_TRANS_COMM_bln_rub     
PRICE_EGGS_rub_per_1000                      PRICE_INDEX_CARGO_TRANSPORT_rog             
PRICE_INDEX_CONSTRUCTION_rog                 PRICE_INDEX_INVESTMENT_rog                  
PRICE_INDEX_LIVESTOCK_PRODUCTS_rog           PROD_AGRO_EGGS_mln                          
PROD_AGRO_EGGS_yoy                           PROD_AGRO_MEAT_th_t                         
PROD_AGRO_MEAT_yoy                           PROD_AUTO_BUS_units                         
PROD_AUTO_PSGR_th                            PROD_AUTO_TRUCKS_AND_CHASSIS_th             
PROD_AUTO_TRUCKS_th                          PROD_BYCYCLES_th                            
PROD_COAL_mln_t                              PROD_E_TWh                                  
PROD_FOOTWEAR_mln_pair                       PROD_GASOLINE_mln_t                         
PROD_NATURAL_AND_ASSOC_GAS_bln_m3            PROD_NATURAL_GAS_bln_m3                     
PROD_OIL_mln_t                               PROD_PAPER_th_t                             
PROD_RAILWAY_CARGO_WAGONS_units              PROD_RAILWAY_PSGR_WAGONS_units              
PROD_STEEL_th_t                              PROD_WOOD_INDUSTRIAL_mln_solid_m3           
PROD_WOOD_ROUGH_mln_solid_m3                 RETAIL_SALES_FOOD_INCBEV_AND_TABACCO_bln_rub
RETAIL_SALES_FOOD_INCBEV_AND_TABACCO_rog     RETAIL_SALES_FOOD_INCBEV_AND_TABACCO_yoy    
RETAIL_SALES_NONFOOD_GOODS_bln_rub           RETAIL_SALES_NONFOOD_GOODS_rog              
RETAIL_SALES_NONFOOD_GOODS_yoy               RETAIL_SALES_bln_rub                        
RETAIL_SALES_rog                             RETAIL_SALES_yoy                            
RETAIL_STOCKS_bln_rub                        RETAIL_STOCKS_days_of_trade                 
RETAIL_STOCKS_rog                            RETAIL_USLUGI_bln_rub                       
RETAIL_USLUGI_rog                            RETAIL_USLUGI_yoy                           
RUR_EUR_eop                                  RUR_USD_eop                                 
SBERBANK_AVG_HH_DEPOSIR_rub                  SOC_EMPLOYED_mln                            
SOC_EMPLOYED_yoy                             SOC_MONEY_INCOME_PER_CAPITA_rub             
SOC_MONEY_INCOME_PER_CAPITA_yoy              SOC_PENSION_rub                             
SOC_REAL_MONEY_INCOME_yoy                    SOC_UNEMPLOYED_REGISTERED_BENEFITS_th       
SOC_UNEMPLOYED_REGISTERED_th                 SOC_UNEMPLOYED_bln                          
SOC_UNEMPLOYED_yoy                           SOC_UNEMPLOYMENT_RATE_percent               
SOC_WAGE_ARREARS_mln_rub                     SOC_WAGE_ARREARS_rog                        
SOC_WAGE_rog                                 SOC_WAGE_rub                                
SOC_WAGE_yoy                                 TRADE_GOODS_EXPORT_bln_usd                  
TRADE_GOODS_EXPORT_rog                       TRADE_GOODS_EXPORT_yoy                      
TRADE_GOODS_IMPORT_bln_usd                   TRADE_GOODS_IMPORT_rog                      
TRADE_GOODS_IMPORT_yoy                       TRANS_COM_bln_t_km                          
TRANS_COM_rog                                TRANS_COM_yoy                               
TRANS_RAILLOAD_mln_t                         TRANS_RAILLOAD_rog                          
TRANS_RAILLOAD_yoy                           TRANS_bln_t_km                              
TRANS_rog                                    TRANS_yoy                                   
TURNOVER_CATERING_bln_rub                    TURNOVER_CATERING_rog                       
TURNOVER_CATERING_yoy      
"""    