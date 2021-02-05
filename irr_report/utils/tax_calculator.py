import pandas as pd
import numpy as np
import math


class TaxCalculator(object):
    def __init__(self, annual_revenue_mat, annual_interest_return_loan, params):
        self.annual_revenue_mat = annual_revenue_mat
        self.params = params
        self.vat_loan_vec, self.vat_interest_vec = self.vat_facility(params)
        
        # self.first_year_portion = params.number_active_days_year_1/params.total_number_days_year_1
        # self.last_year_portion = params.number_active_days_last_year/params.total_number_days_last_year
        self.total_expenses  = self.expenses_calculator()
        self.annual_interest_return_loan = annual_interest_return_loan
    
    def calc_taxes(self, EBIDTA):
        total_depreciation = self.plant_depreciation_calculator()
        annual_corp_tax_mat = []
        for cur_EBIDTA in EBIDTA:
            taxable_EBIDTA = cur_EBIDTA*self.params.percent_EBITDA_for_corp_tax
            total_interest = self.annual_interest_return_loan + 2*self.vat_interest_vec
            deductable_interest = np.zeros(self.params.years)
            for i in range(self.params.years):
                deductable_interest[i] = max(0, min(taxable_EBIDTA[i], total_interest[i]))
            
            annual_corp_tax_base = (cur_EBIDTA - \
                total_depreciation - deductable_interest).clip(min=0)
            annual_corp_tax = annual_corp_tax_base*self.params.Corporate_Tax
            annual_corp_tax_mat.append(annual_corp_tax)
        return np.array(annual_corp_tax)
        
    
    def plant_depreciation_calculator(self):
        plant_depreciatiopn = []
        substitute_tax_depreciation = []
        # Calc Depreciation basis
        plant_depreciation_basis = self.params.Depreciation*self.params.initial_investment
        substitute_tax_plant_depreciation_basis = self.vat_loan*self.params.vat_substitute_tax
        # Calc annual depreciation reduction ammount 
        annual_plant_depreciation = plant_depreciation_basis/self.params.Depreciation_period
        annual_substitute_tax_depreciation = substitute_tax_plant_depreciation_basis/self.params.Depreciation_period

        for i in range(self.params.years):
            # check with Ranjith if this is important
            # if i == 0: 
            #     cur_plant_depretiation = annual_plant_depreciation*self.first_year_portion
            #     cur_substitute_tax_depreciation = annual_substitute_tax_depreciation*self.first_year_portion
            # else:
            cur_plant_depretiation = min(
                                        annual_plant_depreciation, \
                                        plant_depreciation_basis - sum(plant_depreciatiopn)
                                                )

            cur_substitute_tax_depreciation = min(
                                        annual_substitute_tax_depreciation, \
                                        substitute_tax_plant_depreciation_basis - sum(substitute_tax_depreciation)
                                                )

            plant_depreciatiopn.append(cur_plant_depretiation)
            substitute_tax_depreciation.append(cur_substitute_tax_depreciation)
            
        return np.array(plant_depreciatiopn) + np.array(substitute_tax_depreciation)


    def expenses_calculator(self):
        annual_expenses = np.sum(np.array([
            self.params.lease, 
            self.params.OandM, 
            self.params.insurance, 
            self.params.inverter_reserve, 
            self.params.asset_management, 
            self.params.bank_agency_fees_and_others
                ])*self.params.annual_prod)
            
        expenses_vec = []
        for i in range(self.params.years):
            expenses_vec.append(annual_expenses*(1+self.params.inflation)**i)

        return np.array(expenses_vec)


    def vat_facility(self, params):
        remain_return_priod = params.VAT_loan_return_period
        #loan
        self.vat_loan = params.VAT*params.initial_investment
        vat_loan_vec = np.zeros(params.years)
        monthly_loan_return = self.vat_loan/remain_return_priod
        temp_vat_loan = self.vat_loan
        #interst
        vat_interest = params.VAT_loan_interest_rate
        interest_loan_vec = np.zeros(params.years)
        

        for i in range(params.years):
            if remain_return_priod>=12:
                # Case where there is more than a year for payment
                vat_loan_vec[i] = monthly_loan_return*12
                cur_period  = 12
                
            elif remain_return_priod>0:
                # Case where there is less than a year for payment
                vat_loan_vec[i] = temp_vat_loan
                cur_period  = remain_return_priod
                
            else:
                # Case where payment done
                vat_loan_vec[i] = 0 
                cur_period =0 
            
            # calc interest
            interest_loan_vec[i] = temp_vat_loan*vat_interest*remain_return_priod/12
            #update params
            remain_return_priod = remain_return_priod- cur_period
            temp_vat_loan = temp_vat_loan - vat_loan_vec[i]
        
        return vat_loan_vec, interest_loan_vec
            