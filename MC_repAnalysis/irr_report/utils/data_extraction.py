import pandas as pd
import sys

class DataExtraction(object):
    def __init__(self, FIXTURE_DIR):
        try:
            self.db = pd.read_csv(f'{FIXTURE_DIR}\db.csv') 
        except Exception:
            self.db = pd.DataFrame({'id':[], 
                                    'run_name':[],
                                    'input_path':[],
                                    'output_path':[],
                                    'excution_time':[]
                                    })
       
        
    def get_params(self, path):
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
            self.is_DSRA_requires = inputFile['is_DSRA_requires'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter is_DSRA_requires is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.DSRA_Year_Start = inputFile['DSRA_Year_Start'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter DSRA_Year_Start is missing or from unrecognize type")
            sys.exit(exc)
        try:
            self.DSRA_period = inputFile['DSRA_period'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter DSRA_period is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.VAT = inputFile['VAT'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter VAT is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.VAT_loan_interest_rate = inputFile['VAT_loan_interest_rate'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter VAT_loan_interest_rate is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.VAT_loan_return_period = inputFile['VAT_loan_return_period'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter VAT_loan_return_period is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.Depreciation_period = inputFile['Depreciation_period'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter Depreciation_period is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.Depreciation = inputFile['Depreciation'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter Depreciation is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.Corporate_Tax = inputFile['Corporate_Tax'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter Corporate_Tax is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.number_active_days_year_1 = inputFile['number_active_days_year_1'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter number_active_days_year_1 is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.total_number_days_year_1 = inputFile['total_number_days_year_1'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter total_number_days_year_1 is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.number_active_days_last_year = inputFile['number_active_days_year_1'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter number_active_days_year_1 is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.total_number_days_last_year = inputFile['total_number_days_year_1'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter total_number_days_year_1 is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.lease = inputFile['lease'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter lease is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.OandM = inputFile['OandM'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter OandM is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.insurance = inputFile['insurance'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter insurance is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.inverter_reserve = inputFile['inverter_reserve'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter inverter_reserve is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.asset_management = inputFile['asset_management'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter asset_management is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.bank_agency_fees_and_others = inputFile['bank_agency_fees_and_others'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter bank_agency_fees_and_others is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.percent_EBITDA_for_corp_tax = inputFile['percent_EBITDA_for_corp_tax'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter percent_EBITDA_for_corp_tax is missing or from unrecognize type")
            sys.exit(exc)

        try:
            self.vat_substitute_tax = inputFile['vat_substitute_tax'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter vat_substitute_tax is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.recivable_sales_cycle = inputFile['recivable_sales_cycle'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter recivable_sales_cycle is missing or from unrecognize type")
            sys.exit(exc)
        
        try:
            self.payable_sales_cycle = inputFile['payable_sales_cycle'].values[0]
        except (Exception, KeyboardInterrupt) as exc:
            print("Parameter payable_sales_cycle is missing or from unrecognize type")
            sys.exit(exc)        





    
    