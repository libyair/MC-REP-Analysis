import warnings
import logging
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bradford


# Change plot style to ggplot (for better and more aesthetic visualisation)
plt.style.use('ggplot')

class RevenueCalculator(object):
    def __init__(self, cotract_price_range,  annual_prod, degredation, years, yeild, inflation):
        self.cotract_price_range = cotract_price_range
        self.annual_prod = annual_prod
        self.degredation = degredation 
        self.years = years 
        self.yeild = yeild
        self.inflation = inflation

    def prep_energy_prices_contract(self, plot):
        #Bratford distribution parameters
        c = 1
        loc=self.cotract_price_range[0]
        scale=self.cotract_price_range[1] - self.cotract_price_range[0]

        price_vec = bradford.rvs(c, loc=loc , scale =scale , size=1000)
        if plot:
            fig, ax = plt.subplots(1, 1)
            ax.hist(price_vec, density=True, histtype='stepfilled', alpha=0.2)
            ax.legend(loc='best', frameon=False)
            plt.show()
            
        return price_vec

    
    def annual_revenue(self, prices, contract, plot):

        #calculate capacity vector and prices matrix:
        capacity_vec = np.append(self.annual_prod*self.yeild, np.ones(self.years-1))
        price_mat = np.column_stack([prices, np.ones((len(prices),self.years-1))])
        for i in np.arange(1,self.years):
            capacity_vec[i] = capacity_vec[i-1]-capacity_vec[i-1]*self.degredation
            
            if contract=='agreement':
                price_mat[:,i] = price_mat[:,i-1]+price_mat[:,i-1]*0#*self.inflation
            elif contract == 'open_market':
                #TODO - Complete logic here
                break
                                
        annual_revenue = price_mat*capacity_vec[:, np.newaxis].T
        total_revenue = annual_revenue.sum(axis=1)
        if plot:
            plt.figure(1)
            plt.hist(total_revenue)

        return annual_revenue



