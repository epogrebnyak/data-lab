# -*- coding: utf-8 -*-
# 9:58 29.09.2016	10:28 29.09.2016

import pandas as pd
from datetime import date, datetime

DFA_PATH = "data_annual.txt"
DFQ_PATH = "data_quarter.txt"
DFM_PATH = "data_monthly.txt"
CSV_PATHS = {'a': DFA_PATH, 'q': DFQ_PATH, 'm': DFM_PATH}

DEFAULT_FREQUENCY = "m"
VALID_FREQUENCIES = "aqm"
DEFAULT_BACKSHIFT = 5
# backshift operator 
T = 5

def year_backshift(T=5):
    cur_year = date.today().year
    return str(cur_year-T) + "-01"
    
DEFAULT_START = year_backshift()

def read_csv_as_dataframes(paths = CSV_PATHS):

    def to_ts(year):
        return pd.Timestamp(datetime(int(year),12,31))
        
    #dfa = pd.read_csv(paths['a'], index_col = 0)
    dfa = pd.read_csv(paths['a'], converters = {'year':to_ts},          index_col = 'year')
    dfq = pd.read_csv(paths['q'], converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
    dfm = pd.read_csv(paths['m'], converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
    return {'a': dfa, 'q': dfq, 'm': dfm}
 
DATAFRAMES = read_csv_as_dataframes() 

class Indicator():

    def _set_frequency(self, freq):
        freq = freq.lower()
        if freq not in VALID_FREQUENCIES :
            raise Exeption("Invalid frequency: " + freq + 
                           "\nAccepted: " + ", ".join(VALID_FREQUENCIES))        
        else:
            return DATAFRAMES[freq]    
        
    def _filter_labels(self, labels):
        # convert to list if one label is given
        if isinstance(labels, str):
            labels = [labels]
        # labels not in column names omitted         
        return [x for x in labels if x in self.dataframe.columns]        
    
    def _roll_date_back(self, start, t = DEFAULT_BACKSHIFT):
        last_index = self.dataframe.index[-1]
        if isinstance(last_index, pd.tslib.Timestamp):
            return str(last_index.year-t) + "-01"
        else:
            return self.dataframe.index[-1]-t
    
    def __init__(self, label_values, freq=DEFAULT_FREQUENCY, start=None, end=None):
        self.dataframe = self._set_frequency(freq)        
        self.labels    = self._filter_labels(label_values)
        start          = self._roll_date_back(start)
        self.df = self.dataframe.loc[start:end,self.labels] 
        # filename base
        self.basename = "+".join(self.labels) 
        
    def _make_filename(self, filename, ext):
        if not filename:
            filename = self.basename + ext
        elif "." not in filename:
            filename = filename + ext
        return filename             
        
    def to_png(self, filename=None):    
        filename = self._make_filename(filename, ".png")
        ax = self.df.plot()
        fig = ax.get_figure()
        fig.savefig(filename)                              
        
    def to_excel(self, filename=None):
        filename = self._make_filename(filename, ".xls")
        self.df.to_excel(filename)

    def dump(self, basename=None):
        self.to_png(basename)
        self.to_excel(basename)        

        
# gdp   ВВП
# cpi   инфляция
# fx    курс
# pb    платежный баланс 
# cap   инвестиции
# hh    доходы и расходы населения
# gov   госрасходы 
# oil   нефть


# FINAL USE:
#
#

# EVALUATE:
#     не надо обрезать ряды на стадии хранения данных, нужно только для рисунков
#     for testing must have different frequencies a and q and m
#     страница html с месяцами, кварталами и годами + сохранить 
#     все сохранять
#     сразу делать app в интернете

# TODO 1:
#     завести нефть 
#     обрабатывать значения (разности и темпы роста) - для создания новых переменных

# TODO 2:
#     снимать сезонность
#     сделать инерционный прогноз

# ENHANCE:
#     подписи осей графика + количество белого


cpi = Indicator(["CPI_rog", "CPI_NONFOOD_rog", "CPI_FOOD_rog", "CPI_SERVICES_rog"])
cpi.dump("CPI")

gdp = Indicator(["I_yoy", "GDP_yoy", "IND_PROD_yoy", "RETAIL_SALES_yoy"], freq="m") # was "q"
gdp.dump("GDP")

gov = Indicator(["GOV_CONSOLIDATED_EXPENSE_ACCUM_bln_rub", "GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub"], freq="m") # was "a"
gov.dump("GOV")

fx = Indicator(["RUR_EUR_eop", "RUR_USD_eop" ], freq="m")
fx.dump("FX")

bop = Indicator(["TRADE_GOODS_EXPORT_bln_usd", "TRADE_GOODS_IMPORT_bln_usd"])
bop.dump("BOP")

hh = Indicator(["RETAIL_SALES_yoy", "HH_REAL_DISPOSABLE_INCOME_yoy", "SOC_WAGE_yoy"])
hh.dump("HH")

credit = Indicator(["CREDIT_TOTAL_bln_rub", "CORP_DEBT_bln_rub"])
credit.dump("CREDIT")

real1 = Indicator(["TRANS_RAILLOAD_mln_t", "TRANS_bln_t_km", "PROD_E_TWh", "CONSTR_bln_rub_fix"])
real1.dump("REAL1")

real2 = Indicator(["TRANS_RAILLOAD_mln_t", "TRANS_bln_t_km", "PROD_E_TWh", "CONSTR_bln_rub_fix"])
real2.dump("REAL2")





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