import numpy as np
import pandas as pd
import math
from .tax_calculator import TaxCalculator

class CashFlowCalculator(object):

    def __init__(self, annual_revenue_mat, price_vec, params ):
        self.params = params
        self.revenue = annual_revenue_mat
        self.price_vec = price_vec
        self.initial_investment = params.initial_investment
        self.equity_portion = params.equity_portion
        self.interest_rate_range = params.interest_rate_range
        self.interest_list = params.interest_list
        if self.interest_list:
            self.interest_diff = params.interest_diff
        self.is_DSRA_requires = params.is_DSRA_requires
        if self.is_DSRA_requires:
            self.DSRA_Year_Start = params.DSRA_Year_Start
            self.DSRA_period = params.DSRA_period

        
    def calc_cash_flow(self):
        
        loan_vec = []
        annual_loan_return_mat = []
        total__loan_return = []
        annual_interes_return_mat = []
        total__interes_return = [] 
        total_taxes = []
        DSRA = []
        annual_cash_flow = []
        if self.interest_list:
            interest_list = np.linspace(self.interest_rate_range[0],self.interest_rate_range[1], 5)
        else:
            interest_list = [self.interest_rate_range]
        #Record interest rate for the current run
        interest_rate_MC = np.repeat(interest_list,len(self.revenue))
        res = {}
        for interest_rate in interest_list:
            
            
            loan, annual_loan_return, annual_interes_return = self._loan_return_calculator(self.initial_investment,
                                                                                self.equity_portion, interest_rate)

            loan_vec.append(loan)
            annual_loan_return_mat.append(annual_loan_return)
            total__loan_return.append(sum(annual_loan_return))
            annual_interes_return_mat.append(annual_interes_return)
            total__interes_return.append(sum(annual_interes_return))

            if self.is_DSRA_requires:
                annual_DSRA = self.DSRA_calculator(annual_loan_return, annual_interes_return)
                DSRA.append(annual_DSRA)
            else:
                annual_DSRA = np.zeros(self.params.years)

            #calculate cash flow
            
            tax_calculator = TaxCalculator(self.revenue, annual_interes_return, self.params)
            
            EBIDTA = self.revenue - tax_calculator.total_expenses 
            annual_corp_tax, total_depreciation = tax_calculator.calc_taxes(EBIDTA)
            total_taxes.append(sum(annual_corp_tax))

            UpfrontFee_Substitute_TaxCapex = tax_calculator.vat_interest_vec
            delta_working_capital = self.calc_delta_working_capital(self.revenue,
                                        tax_calculator.total_expenses, self.params)

            ## Calculate total costs to be reduced from revenue
            costs = annual_loan_return + annual_interes_return + annual_DSRA + \
                annual_corp_tax + tax_calculator.total_expenses + delta_working_capital + UpfrontFee_Substitute_TaxCapex

            annual_cash_flow_i = self.revenue-costs
            annual_cash_flow_i = np.clip(annual_cash_flow_i, a_min=0, a_max =None)
            annual_cash_flow.append(annual_cash_flow_i)
            # print('delta_working_capital: ', delta_working_capital)
            # print('delta_working_capital: ', costs)

            ## update results
            for i,price in enumerate(self.price_vec):
                res[f'interset_{str(interest_rate)}_price_{price}'] = { 
                    'Annual_revenue': list(self.revenue[i]),
                    'OPEX':  list(tax_calculator.total_expenses),
                    'Annual_loan_return':  list(annual_loan_return),
                    'Annual_interes_return':  list(annual_interes_return),
                    'Annual_DSRA':  list(annual_DSRA),
                    'Annual_corp_tax':  list(annual_corp_tax),
                    'Delta_working_capital':  list(delta_working_capital[i]),
                    'UpfrontFee_and_Substitute_TaxCapex':  list(UpfrontFee_Substitute_TaxCapex),
                    'Cash Flow Available for Dividends':  list(annual_cash_flow_i[i])

                    }
                for key in res[f'interset_{str(interest_rate)}_price_{price}']:
                    print(key, ': ', len(res[f'interset_{str(interest_rate)}_price_{price}'][key]))

        df = pd.DataFrame( {'interest_list':interest_list, 
                            'total__loan_return': total__loan_return, 
                            'total__interes_return':total__interes_return,
                            'loan_val':loan_vec, 
                            'total_taxes': total_taxes
                                                        }, index=interest_list)
                            
        
        axes = df[['total__loan_return', 'total__interes_return']].plot.bar(stacked=True)
        axes.legend(loc=2) 

        return interest_rate_MC, annual_cash_flow, res

    def _loan_return_calculator(self, total_investment, equity_portion, interest_rate, grace_period = 12, interest_grace = 6,
                       loan_period = 20, years = 30, yearly_payments =2 ):
        periodic_loan_return = []
        periodic_interes_return = []
        loan = total_investment - total_investment*equity_portion
        remaining_loan = loan
        for i in np.arange(1, years*yearly_payments+1):
            cur_loan_return = 0
            cur_interes_return = 0 
            if i<=loan_period*yearly_payments:
                ## Calc interest returns:
                if i>interest_grace/12*yearly_payments:
                    cur_interes_return= remaining_loan*interest_rate*(1/yearly_payments)
                ## Calc loan return:
                if i>grace_period/12*yearly_payments:          
                    cur_loan_return = loan/((loan_period-grace_period/12)*yearly_payments)
                
            remaining_loan = remaining_loan - cur_loan_return
            periodic_loan_return.append(cur_loan_return)
            periodic_interes_return.append(cur_interes_return)

        annual_loan_return = np.array(periodic_loan_return).reshape(int(len(periodic_loan_return)/yearly_payments), yearly_payments).sum(axis=1)
        annual_interes_return = np.array(periodic_interes_return).reshape(int(len(periodic_interes_return)/2), yearly_payments).sum(axis=1)
        
        return loan, annual_loan_return, annual_interes_return

    def DSRA_calculator(self, annual_loan_return , annual_interes_return):
        debt_window = self.DSRA_period/12 #Convert month to years
        DSRA_balance = []
        for i in range(len(annual_loan_return)): 
            annual_debt = annual_loan_return + annual_interes_return            
            if i < len(annual_loan_return)-1:
                annual_balance_win = annual_debt[i+1:i+1+math.ceil(debt_window)]
                annual_balance = sum(annual_balance_win[0:len(annual_balance_win)-1]) + \
                                annual_balance_win[-1]*(debt_window-int(debt_window))
            else: 
                annual_balance = 0
            DSRA_balance.append(annual_balance)
        DSRA = np.append(np.array(DSRA_balance[0]), np.diff(DSRA_balance))
        return DSRA 


    def calc_delta_working_capital(self, revenue_mat, expenses, params ):
        delta_working_capital_mat = []
        for revenue in revenue_mat:
            recivable = revenue*(params.recivable_sales_cycle/365)
            payable = expenses*(params.payable_sales_cycle/365)
            net_delta_working_capital = recivable - payable
            delta_working_capital = np.append(net_delta_working_capital[0], np.diff(net_delta_working_capital))
            delta_working_capital_mat.append(delta_working_capital)
        return delta_working_capital_mat
