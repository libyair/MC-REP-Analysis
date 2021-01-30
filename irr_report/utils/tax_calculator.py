import pandas as pd
import numpy as np


class TaxCalculator(object):
    def _init__(self, annual_revenue_mat, params):
        self.annual_revenue_mat = annual_revenue_mat
        self.params = params
        self.vat_loan = params.VAT*params.initial_investment
        # self.first_year_portion = params.number_active_days_year_1/params.total_number_days_year_1
        # self.last_year_portion = params.number_active_days_last_year/params.total_number_days_last_year
        self.total_expenses  = self.expenses_calculator()
    
    def calc_taxes(self, EBIDTA):
        total_depreciation = self.plant_depreciation_calculator()
        corp_tax_base = self.annual_revenue_mat - total_depreciation - self.total_expenses
        taxable_EBIDTA = EBIDTA*self.params.percent_EBITDA_for_corp_tax
        deductable_interest  = max(0, min(taxable_EBIDTA, math.ciel()) ) #sum of all interests in the project
        
    
    def plant_depreciation_calculator(self):
        plant_depreciatiopn = []
        substitute_tax_depreciation = []
        # Calc Depreciation basis
        plant_depreciation_basis = self.params.Depreciation*self.params.initial_investment
        substitute_tax_plant_depreciation_basis = self.vat_loan*self.params.substitute_tax
        # Calc annual depreciation reduction ammount 
        annual_plant_depreciation = plant_depreciation_basis/self.params.Depreciation_period
        annual_substitute_tax_depreciation = substitute_tax_plant_depreciation_basis/self.params.Depreciation_period

        for i in range(len(self.params.years)):
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
                ])*self.params.annual_production_capacity)
            
        expenses_vec = []
        for i in range(len(self.params.years)):
            expenses_vec.append(annual_expenses*(1+self.params.inflation)^i)
        
        return np.array(expenses_vec)