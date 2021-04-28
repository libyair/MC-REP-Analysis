import numpy as np
import pandas as pd
import MySQLdb as m
import time
from envparse import env


def get_params(inputFile):

    param_dic = {}
    missing_params = []
    try: 
        param_dic['cotract_price_range'] = inputFile['contract_tarrif_range'].values[0]
        if isinstance(param_dic['cotract_price_range'], str):
            param_dic['cotract_price_range'] = eval(inputFile['contract_tarrif_range'].values[0])
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('cotract_price_range')
    
    try: 
        param_dic['annual_prod'] =  inputFile['annual_production_capacity'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['degredation'] = inputFile['production_degredeation'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['years'] = inputFile['project_years'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['yeild'] = inputFile['yeild'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['inflation'] = inputFile['inflation'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['initial_investment'] = inputFile['initial_investment'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['equity_portion'] = inputFile['equity_portion'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['interest_rate_range'] = inputFile['interest_rate_range'].values[0]
        param_dic['interest_list'] = False
        if isinstance(param_dic['interest_rate_range'], str):
            # got a list
            param_dic['interest_rate_range'] = eval(inputFile['interest_rate_range'].values[0])
            param_dic['interest_list'] = True
            param_dic['interest_diff'] = inputFile['interest_diff'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['cost_of_capital'] = inputFile['cost_of_capital'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['is_DSRA_requires'] = inputFile['is_DSRA_requires'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['DSRA_Year_Start'] = inputFile['DSRA_Year_Start'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    try:
        param_dic['DSRA_period'] = inputFile['DSRA_period'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['VAT'] = inputFile['VAT'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['VAT_loan_interest_rate'] = inputFile['VAT_loan_interest_rate'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['VAT_loan_return_period'] = inputFile['VAT_loan_return_period'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['Depreciation_period'] = inputFile['Depreciation_period'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['Depreciation'] = inputFile['Depreciation'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['Corporate_Tax'] = inputFile['Corporate_Tax'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['number_active_days_year_1'] = inputFile['number_active_days_year_1'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['total_number_days_year_1'] = inputFile['total_number_days_year_1'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['number_active_days_last_year'] = inputFile['number_active_days_year_1'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['total_number_days_last_year'] = inputFile['total_number_days_year_1'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['lease'] = inputFile['lease'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['OandM'] = inputFile['OandM'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['insurance'] = inputFile['insurance'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['inverter_reserve'] = inputFile['inverter_reserve'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['asset_management'] = inputFile['asset_management'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['bank_agency_fees_and_others'] = inputFile['bank_agency_fees_and_others'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['percent_EBITDA_for_corp_tax'] = inputFile['percent_EBITDA_for_corp_tax'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['vat_substitute_tax'] = inputFile['vat_substitute_tax'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')
    
    try:
        param_dic['recivable_sales_cycle'] = inputFile['recivable_sales_cycle'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    try:
        param_dic['payable_sales_cycle'] = inputFile['payable_sales_cycle'].values[0]
    except (Exception, KeyboardInterrupt) as exc:
        missing_params.append('annual_prod')

    return param_dic, missing_params


def convert(o):
    if isinstance(o, np.int64):
        return int(o)


def _db_connect():
    env.read_envfile('env_config.env')
    db_host = env('DB_HOST')
    db_port = env.int('DB_PORT')
    db_user = env('DB_USER')
    db_pass = env('DB_PASS')
    db_name = env('DB_NAME')

    conn = m.connect(host=db_host,
                     user=db_user,
                     port=db_port,
                     passwd=db_pass,
                     db=db_name)
    return conn

def update_db(data):
    conn = _db_connect()
    cur = conn.cursor()

    cur_date = time.strftime('%Y-%m-%d %H:%M:%S')
    name = data.get('name')
    params = data.get('params')
    creator = data.get('creator')

    insert_query = f"""
    INSERT INTO rundata (date, name, creator, status, params) 
    VALUES ('{cur_date}', '{name}', '{creator}', 'running', '{params}');
    """
    cur.execute(insert_query)
    conn.commit()
    id_ = cur.lastrowid
    return id_


def get_run_results(id):
    conn = _db_connect()
    cur = conn.cursor(m.cursors.DictCursor)
    select_query = f"""
            SELECT * FROM rundata WHERE id ={id};
            """
    cur.execute(select_query)
    conn.commit()
    res = cur.fetchall()
    return res


def get_run_history_data(username):
    conn = _db_connect()
    cur = conn.cursor(m.cursors.DictCursor)
    insert_query = f"""
                SELECT * FROM rundata WHERE creator ='{username}';
                """

    cur.execute(insert_query)
    conn.commit()
    res = cur.fetchall()
    run_history_df = pd.DataFrame(res)
    return run_history_df[['name', 'id', 'date', 'status']]









