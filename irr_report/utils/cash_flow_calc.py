import numpy as np
import pandas as pd

class CashFlowCalculator(object):

    def __init__(self, annual_revenue_mat, params ):
        self.revenue = annual_revenue_mat
        self.cash_flow_data = params.cash_flow_data
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
        columns = ['Total Expenses',
                # 'DSRA',
                'Interest VAT facility', #VAT 
                'Taxes', 
                'Delta Working Capital',
                'Upfront Fee + Substitute Tax Capex'
                ]
        costs = self.cash_flow_data[columns].sum(axis=1)
        loan_vec = []
        annual_loan_return_mat = []
        total__loan_return = []
        annual_interes_return_mat = []
        total__interes_return = [] 
        DSRA = []
        annual_cash_flow = []
        zero_cash_flow = []
        if self.interest_list:
            interest_list = np.linspace(self.interest_rate_range[0],self.interest_rate_range[1], 5)
        else:
            interest_list = [self.interest_rate_range]
        #Record interest rate for the current run
        interest_rate_MC = np.repeat(interest_list,len(self.revenue))
        for interest_rate in interest_list:
            
            
            loan, annual_loan_return, annual_interes_return = self._loan_return_calculator(self.initial_investment,
                                                                                self.equity_portion, interest_rate)

            loan_vec.append(loan)
            annual_loan_return_mat.append(annual_loan_return)
            total__loan_return.append(sum(annual_loan_return))
            annual_interes_return_mat.append(annual_interes_return)
            total__interes_return.append(sum(annual_interes_return))

            if self.DSRA_period:
                annual_DSRA = self.DSRA_calculator(annual_loan_return , annual_interes_return)
                DSRA.append(annual_DSRA)
                print(DSRA)

            #calculate cash flow
            self.revenue[0][0] = self.revenue[0][0]+ 29229 #TODO : add this as a parameter
            # EBIDTA = self.revenue - self.cash_flow_data['Total Expenses'].values.T 
            # operating_cash_flow = EBIDTA - self.cash_flow_data['Taxes'].values.T - self.cash_flow_data['Delta Working Capital'].values.T \
            #                                 - self.cash_flow_data['Upfront Fee + Substitute Tax Capex'].values.T
            
            # Cash_Flow_Available_after_VAT = operating_cash_flow - self.cash_flow_data['Interest'].values.T
            # Cash_Flow_Available_for_Loans = Cash_Flow_Available_after_VAT - self.cash_flow_data['DSRA'].values.T

            costs = costs + annual_loan_return + annual_interes_return + annual_DSRA
            costs = costs.T
            annual_cash_flow_i = self.revenue-costs.values
            annual_cash_flow_i = np.clip(annual_cash_flow_i, a_min=0, a_max =None)
            annual_cash_flow.append(annual_cash_flow_i)
          
        df = pd.DataFrame( {'interest_list':interest_list, 
                            'total__loan_return': total__loan_return, 
                            'total__interes_return':total__interes_return,
                            'loan_val':loan_vec}, index=interest_list)
        
        axes = df[['total__loan_return', 'total__interes_return']].plot.bar(stacked=True)
        axes.legend(loc=2) 

        return interest_rate_MC, annual_cash_flow

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
        debt_window = self.self.DSRA_period/12 #Convert month to years
        DSRA_balance = []
        for i in range(len(annual_loan_return)):        
            annual_balance_win = annual_loan_return[i:i+math.ceil(debt_window)]
            annual_balance = sum(annual_balance_win[0:len(annual_balance_win)-1]) + annual_balance_win[-1]*(debt_window-int(debt_window))
            DSRA_balance.append(annual_balance)
            
        DSRA = np.append(np.array(DSRA_balance[0]), np.diff(DSRA_balance))
        return DSRA 


        
