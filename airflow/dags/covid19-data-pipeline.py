import json
from datetime import datetime

from airflow import DAG
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.dates import days_ago

# def get_covid19_report_today():

#     import requests
#     import logging
#     import sys, traceback

#     LOGGER = logging.getLogger("airflow.task")
#     LOGGER.info("Fetching data...")

#     url = 'https://covid19.th-stat.com/api/open/today'
#     LOGGER.info("URL : {}".format(url))

#     try:

#         LOGGER.info("Request to the URL...")
#         response = requests.get(url)
#         LOGGER.info("Transform to JSON...")
#         data = response.json()
#         LOGGER.info("Writing to file...")
#         # LOGGER.info('Responding from API : {}'.format(json.dumps(data)))
#         with open('data.json', 'w') as f:
#             LOGGER.debug('Write temp file to : {}'.format(f.name))
#             json.dump(data, f)

#     except:
#         LOGGER.error('Cannot fetch the data!!!')

#     return data


def save_data_into_db(**kwargs):

    import logging
    import sys, traceback
    import traceback

    LOGGER = logging.getLogger("airflow.task")
    LOGGER.info("Saving data...")

    # Pulling data from previous task instance (or "ti")
    ti = kwargs['ti']
    LOGGER.info("Sync XCom to pull data from previous task by ID...")

    data = ti.xcom_pull(task_ids='get_covid19_report_today')
    LOGGER.info("Data : {}".format(data))

    data = json.loads(data)

    # "covid19_db" was declare in Admin > Connections via AirFlow's UI
    mysql_hook = MySqlHook(mysql_conn_id='covid19_db')
        
    insert = """
        INSERT INTO daily_covid19_reports (
            confirmed,
            recovered,
            hospitalized,
            deaths,
            new_confirmed,
            new_recovered,
            new_hospitalized,
            new_deaths,
            update_date,
            source,
            dev_by,
            server_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    dt = datetime.strptime(data.get('UpdateDate'), '%d/%m/%Y %H:%M')
    mysql_hook.run(insert, parameters=(data.get('Confirmed'),
                                    data.get('Recovered'),
                                    data.get('Hospitalized'),
                                    data.get('Deaths'),
                                    data.get('NewConfirmed'),
                                    data.get('NewRecovered'),
                                    data.get('NewHospitalized'),
                                    data.get('NewDeaths'),
                                    dt,
                                    data.get('Source'),
                                    data.get('DevBy'),
                                    data.get('SeverBy')))


default_args = {
    'owner': 'dataength',
    'start_date': datetime(2020, 7, 1),
    'email': ['test@mailhog.local'],
    'provide_context': True  # to support task instance for XComms with kwargs['ti']
}
with DAG('covid19_data_pipeline',
         schedule_interval='@daily',
         default_args=default_args,
         description='A simple data pipeline for COVID-19 report',
         catchup=False) as dag:

    # t1 = PythonOperator(
    #     task_id='get_covid19_report_today',
    #     python_callable=get_covid19_report_today
    # )

    t1 = SimpleHttpOperator(
        task_id='get_covid19_report_today',
        method='GET',
        http_conn_id='https_covid19_api',
        endpoint='/api/open/today',
        headers={"Content-Type":"application/json"},
        xcom_push=True,
        dag=dag
    )

    t2 = PythonOperator(
        task_id='save_data_into_db',
        python_callable=save_data_into_db
    )

    t3 = EmailOperator(
        task_id='send_email',
        to=['test@mailhog.local'],
        subject='Your COVID-19 report today is ready',
        html_content='Please check your dashboard. :)'
    )

    t1 >> t2 >> t3
