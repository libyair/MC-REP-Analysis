from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import click
import logging
from utils import *
import plotly.express as px


@click.command()
@click.option('--path', '-p', help="The path to the file and file name containing the data")
def run(path=None):
    
    #Upload db
    FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'resources')
    params = DataExtraction(FIXTURE_DIR)
    ## Get setting 
    if not path:
        run_settings = GetSettings(FIXTURE_DIR, params.db)
    
            
    params.get_params(run_settings.input_path)
    
    annual_revenue_MC = RevenueCalculator(params.cotract_price_range, params.annual_prod, params.degredation, params.years, params.yeild, \
                                                        params.inflation )
    
    if isinstance(params.cotract_price_range, list):
        if len(params.cotract_price_range)==1:
            price_vec = params.cotract_price_range
        else:
            price_vec  = annual_revenue_MC.prep_energy_prices_contract(plot=False) 
    else: 
        price_vec = [params.cotract_price_range] 
    
    
    annual_revenue_mat = annual_revenue_MC.annual_revenue(price_vec, contract='agreement', plot=True)
    
    cash_flow_calculator = CashFlowCalculator(annual_revenue_mat, params)

    interest_rate_MC, annual_cash_flow = cash_flow_calculator.calc_cash_flow()

    metrics = Metrics(annual_cash_flow, params)

    irr_vec , npv_vec, payback_vec, no_payback_count = metrics.metrics_calculator()
    # print(irr_vec, npv_vec, payback_vec)
    irr_vec = np.array(irr_vec)
    npv_vec = np.array(npv_vec)
    payback_vec=np.array(payback_vec, dtype=np.float64)

    voltality = np.std(npv_vec)/np.sqrt(len(npv_vec))
    print('voltality: ', voltality)
    print('mean IRR: ', np.mean(irr_vec[~np.isnan(irr_vec)]))
    print('mean NPV: ', np.mean(npv_vec[~np.isnan(irr_vec)]))
    print('mean Payback: ', np.mean(payback_vec[~np.isnan(payback_vec)]))


    treshold = 0.02
    prob_lower_then_threshold = sum(irr<treshold for irr in irr_vec)/len(irr_vec)
    print('prob_lower_then_threshold: ',prob_lower_then_threshold)
    valid_ind = ~np.isnan(irr_vec)
    res = pd.DataFrame({#'price':  price_vec[valid_ind], \
                        #'interest_rate' : interest_rate_MC[valid_ind], \
                        'irr_vec': irr_vec[valid_ind], \
                        'npv_vec': npv_vec[valid_ind], \
                             'payback_vec':payback_vec[valid_ind]})
                             
    res.to_csv(f'{run_settings.output_path}\{run_settings.run_name}_results.csv')
    # if len(res)>1:
    #     figure = px.histogram(res, x="irr_vec")
    #     figure.show()
    
if __name__ == "__main__":
    run()