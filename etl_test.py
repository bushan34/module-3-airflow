from datetime import timedelta, datetime
from random import randint

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
#from airflow.operators.python_operator import PythonOperator
#SQL Scripts
SQL_CONTEXT = {
	'PAYMENT': """
		insert overwrite table nnaranov.pro_ods_payment partition (year='{{ execution_date.year }}') 
            	select user_id, pay_doc_type, cast(pay_doc_num as INT), account, phone, billing_period, cast(pay_date as DATE), cast(sum as DECIMAL(8,2))
           	from nnaranov.stg_payment where year(pay_date) = {{ execution_date.year }};
		""",
	'MDM':	"""
            insert overwrite table nnaranov.pro_ods_mdm partition (year='{{ execution_date.year }}') 
            select id, district, registered_at, billing_mode, is_vip
            from mdm.user where year(from_unixtime(registered_at div 1000)) = {{ execution_date.year }};
            """,
}

def get_phase(task_phase):
    tasks = []
    for task in SQL_CONTEXT[task_phase]:
        query = SQL_CONTEXT[task_phase][task]
        tasks.append(PostgresOperator(
            task_id='pro_etl_'.format(task_phase, task),
            dag=dag,
            sql=query
        ))
    return tasks
	
USERNAME = 'nnaranov'
default_args = {
    'owner': USERNAME,
    'start_date': datetime(2010, 1, 1, 0, 0, 0)
}

dag = DAG(
    USERNAME + '.etl_test',
    default_args=default_args,
    description='ETL tasks project',
    schedule_interval="0 0 1 1 *",
	concurrency=1,
    max_active_runs=1,
)
