# -*- coding: utf-8 -*-
# 9:58 29.09.2016	10:28 29.09.2016

import pandas as pd
from datetime import date, datetime

#
# 1. Страница 4 рисунка
# =====================
#
# Нарисовать 4 графика на страницу, в каждом по одному временному ряду. 
#
#

#p = Page(["GDP", "CPI", "PPI", ""], header="", freq="m", start=None, end=None)


#
# 2. Один риснок
# ==============
#
# Нарисовать рисунок с одним временным рядом. 
#
# May use plotting archives
# https://github.com/epogrebnyak/plotting
# https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/getter/plots.py
#



DFA_PATH = "data_annual.txt"
DFQ_PATH = "data_quarter.txt"
DFM_PATH = "data_monthly.txt"

DEFAULT_FREQUENCY = "m"
VALID_FREQUENCIES = "aqm"

def year_backshift(T=5):
    return pd.Timestamp(datetime(date.today().year-T, 1, 1))
    
DEFAULT_START = year_backshift()

dfa = pd.read_csv(DFA_PATH, index_col = 0)
dfq = pd.read_csv(DFQ_PATH, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
dfm = pd.read_csv(DFM_PATH, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
DATAFRAMES = {'a': dfa, 'q': dfq, 'm': dfm}

class Indicator():

    def set_frequency(self, freq):
        freq = freq.lower()
        if freq not in VALID_FREQUENCIES :
            raise Exeption("Invalid frequency: " + freq + 
                           "\nAccepted: " + ", ".join(VALID_FREQUENCIES))        
        else:
            return DATAFRAMES[freq]    
        
    def filter_labels(self, labels):
        # convert to list if one label is given
        if isinstance(labels, str):
            labels = [labels]
        # labels not in column names omitted         
        return [x for x in labels if x in self.dataframe.columns]        
    
    def __init__(self, label_values, freq=DEFAULT_FREQUENCY, start=DEFAULT_START, end=None):
        self.dataframe = self.set_frequency(freq)        
        self.labels = self.filter_labels(label_values)
        self.df = self.dataframe.loc[start:end,self.labels] 
        # filename base
        self.basename = "+".join(self.labels) 
        
    def to_png(self):
        filename = self.basename + ".png"
        ax = self.df.plot()
        fig = ax.get_figure()
        fig.savefig(filename)                              
        
    def to_excel(self):
        filename = self.basename + ".xls"
        self.df.to_excel(filename)

    def dump(self):
        self.to_png()
        self.to_excel()        
        
cpi = Indicator(["CPI_rog", "CPI_NONFOOD_rog", "CPI_FOOD_rog", "CPI_SERVICES_rog"])
cpi.to_png()
cpi.to_excel()

gdp = Indicator(["I_yoy", "GDP_yoy", "IND_PROD_yoy", "RETAIL_SALES_yoy"], freq="q")
gdp.dump()


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