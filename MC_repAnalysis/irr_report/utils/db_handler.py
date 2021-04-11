import MySQLdb as m
from envparse import env
import traceback
import json

def db_connect():
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


def get_data(conn, id):
    try:
        cur = conn.cursor()

        insert_query = f"""
        SELECT params FROM rundata WHERE id ={id}
        """
        cur.execute(insert_query)
        conn.commit()
        params = cur.fetchall()[0][0]
        return json.loads(params)

    except Exception as e:
        error_dict = {
            "dev_error": e.replace('"', '').replace("'", ''),
            "user_error": f"Error getting data for run id {id}"
        }
        raise Exception(error_dict)


def update_error(conn, id, error_dict):
    print('here1')
    cur = conn.cursor()
    print('here2')
    error_query = f"""
        UPDATE rundata 
        SET error_message = '{str(error_dict).replace("'", '"')}', status='failed'  
        WHERE id = {id};
        """
    print('error_query: ', error_query)
    try:
        cur.execute(error_query)
        conn.commit()
    except (m.Error, m.Warning) as e:
        print(e)
    return 1


def update_results(conn, id, results, mc):
    try:
        cur = conn.cursor()
        result_update_query = f"""
            UPDATE rundata 
            SET results = '{str(results).replace("'", '"')}', status = 'success', MC = {mc}
            WHERE id = {id};
            """
        print('result_update_query: ', result_update_query)
        cur.execute(result_update_query)
        conn.commit()

    except Exception as e:
        error_dict = {
            "dev_error": e.replace('"', '').replace("'", ''),
            "user_error": f"Error saving results for run id {id}"
        }
        raise Exception(error_dict)
