from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px


class Metrics(object):
    def __init__(self, cash_flow, params):
        self.cash_flow = cash_flow
        self.cost_of_capital = params.cost_of_capital
        self.initial_equity_investmant = params.initial_investment*params.equity_portion
    
    
    def metrics_calculator(self):
        irr_vec = []
        npv_vec = []
        payback_vec = []
        no_payback_count = 0
        
        for cash_flow in self.cash_flow:
            for year in cash_flow:
                vec = np.append(-self.initial_equity_investmant,year)
                irr = np.irr(vec)
                irr_vec.append(irr)
                npv_vec.append(np.npv(self.cost_of_capital, np.append(-self.initial_equity_investmant,year)))
                ##payback calculation
                payback = self.payback_calculator(vec,self.initial_equity_investmant)
                payback_vec.append(payback)
                if not payback:
                   no_payback_count = no_payback_count + 1  
            
        return irr_vec, npv_vec, payback_vec, no_payback_count

    def payback_calculator(self, vec,initial_equity_investment):
        cum_cashflow = np.cumsum(vec)
        
        if np.any(cum_cashflow>0):
            final_full_year = np.max(np.where(cum_cashflow<=0))
            fraction_year=0

            if final_full_year<len(cum_cashflow)-1:
                fraction_year = -cum_cashflow[final_full_year]/cum_cashflow[final_full_year+1]

            payback_period = final_full_year+fraction_year
            
            return payback_period
        else:
            #TODO: Decide what to do without payback
            return None
        

