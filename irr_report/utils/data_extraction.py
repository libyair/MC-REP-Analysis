import pandas as pd
import sys

class DataExtraction(object):
    def __init__(self, path):
        
        self.path = path 
        
        try:
            inputFile = pd.read_csv(f'{path}\inputFile.csv')
        except (Exception, KeyboardInterrupt) as exc:
            print("Error while trying to load params from path: File may not exist")
            sys.exit(exc)
         
        try:
            self.cotract_price_range = inputFile['contract_tarrif_range'].values[0]
            if isinstance(self.cotract_price_range, str):
                self.cotract_price_range = eval(inputFile['contract_tarrif_range'].values[0])
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter cotract_price_range is missing or from unrecognize type")
            sys.exit(exc)
            
        try: 
            self.annual_prod =  inputFile['annual_production_capacity'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter annual_production_capacity is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.degredation = inputFile['production_degredeation'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter degredation is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.years = inputFile['project_years'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter project_years is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.yeild = inputFile['yeild'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter yeild is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.inflation = inputFile['inflation'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter inflation is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.initial_investment = inputFile['initial_investment'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter initial_investment is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.equity_portion = inputFile['equity_portion'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter equity_portion is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.interest_rate_range = inputFile['interest_rate_range'].values[0]
            self.interest_list = False
            if isinstance(self.interest_rate_range, str):
                # got a list
                self.interest_rate_range = eval(inputFile['interest_rate_range'].values[0])
                self.interest_list = True
                self.interest_diff = inputFile['interest_diff'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("At least one of interest_rate_range or interest_diff  parameter is missing or from unrecognize type")
            raise
            sys.exit(exc)
        try:
            self.cost_of_capital = inputFile['cost_of_capital'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter cost_of_capital is missing or from unrecognize type")
            sys.exit(exc)

        try: 
            self.cash_flow_data = pd.read_csv(f'{path}\cash_flow_data.csv')            
        except (Exception, KeyboardInterrupt) as exc:
            print("Error while trying to load cash_flow_data.csv from path: File may not exist in path")
            sys.exit(exc)





    
    