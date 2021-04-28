import numpy as np
import click
import logging
from utils import *
import sys
import traceback


@click.command()
@click.option('--id', '-i', help="Run id as key to the dataset row")
def run(id):
    try:
        # Upload db
        conn = db_connect()
        params_dict = get_data(conn, id)

        calc = Calculations(params_dict, id)
        # Calculate metrics
        print('calc.params: ', calc.params)
        results, mc = calc.run_calculations(calc.params)
        # Update results
        update_results(conn, id, results, mc)

    except Exception as e:
        print("Error reading data from MySQL table: ", e)
        traceback.print_exc()
        ans = update_error(conn, id, e)
        print(ans)

    finally:
        conn.close()
        sys.exit(0)


class Params:
    def __init__(self, params):
        self.__dict__.update(params)


class Calculations:
    def __init__(self, params_dict, id):
        self.params = Params(params_dict)
        self.id = id

    def run_calculations(self, params):
        try:
            mc = False
            annual_revenue_MC = RevenueCalculator(params.cotract_price_range, params.annual_prod, params.degredation,
                                                  params.years, params.yeild, params.inflation)

            if isinstance(params.cotract_price_range, list):
                mc = True
                if len(params.cotract_price_range) == 1:
                    price_vec = params.cotract_price_range
                else:
                    price_vec = annual_revenue_MC.prep_energy_prices_contract(plot=False)
            else:
                price_vec = [params.cotract_price_range]

            annual_revenue_mat = annual_revenue_MC.annual_revenue(price_vec, contract='agreement', plot=True)

            cash_flow_calculator = CashFlowCalculator(annual_revenue_mat, price_vec, params)

            interest_rate_MC, annual_cash_flow, annual_res = cash_flow_calculator.calc_cash_flow()

            metrics = Metrics(annual_cash_flow, params)

            irr_vec, npv_vec, payback_vec, no_payback_count = metrics.metrics_calculator()
            irr_vec = np.array(irr_vec)
            npv_vec = np.array(npv_vec)
            payback_vec = np.array(payback_vec, dtype=np.float64)

            voltality = np.std(npv_vec)/np.sqrt(len(npv_vec))
            print('voltality: ', voltality)
            print('mean IRR: ', np.mean(irr_vec[~np.isnan(irr_vec)]))
            print('mean NPV: ', np.mean(npv_vec[~np.isnan(irr_vec)]))
            print('mean Payback: ', np.mean(payback_vec[~np.isnan(payback_vec)]))
            threshold = 0.02
            prob_lower_then_threshold = sum(irr < threshold for irr in irr_vec)/len(irr_vec)
            print('prob_lower_then_threshold: ', prob_lower_then_threshold)
            valid_ind = ~np.isnan(irr_vec)

            res = {
                'irr_vec': list(irr_vec[valid_ind]),
                'npv_vec': list(npv_vec[valid_ind]),
                'payback_vec': list(payback_vec[valid_ind]),
                'prob_lower_then_threshold': prob_lower_then_threshold,
                'volatility': voltality,
                'mean_IRR': np.mean(irr_vec[~np.isnan(irr_vec)]),
                'mean_NPV': np.mean(npv_vec[~np.isnan(irr_vec)]),
                'mean_payback': np.mean(payback_vec[~np.isnan(payback_vec)])
            }

            # Update mc flag
            if len(annual_res) > 1:
                mc = True
            else:
                print('annual_res: ', annual_res)
                res['annual_results'] = annual_res[list(annual_res.keys())[0]]

            return res, mc

        except Exception as e:
            print(e)
            error_dict = {
                "dev_error": str(e).replace('"', '').replace("'", ''),
                "user_error": f"Error in metric calculation for run_id {self.id}"
            }
            # TODO: For each function it's own error message
            print(error_dict)
            raise Exception(error_dict)


if __name__ == "__main__":
    run()

