from datetime import timedelta, datetime
from random import randint

from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataProcHiveOperator

USERNAME = 'nnaranov'

default_args = {
    'owner': USERNAME,
    'start_date': datetime(2013, 1, 1, 0, 0, 0)
}

dag = DAG(
    USERNAME + '_data_lake_etl',
    default_args=default_args,
    description='Data Lake ETL tasks',
    schedule_interval="0 0 1 1 *",
)

tables = ('billing', 'issue', 'payment', 'traffic')
ods = []
for table in tables:
	if table == 'billing':
		query = """
			insert overwrite table nnaranov.ods_billing partition (year='{{ execution_date.year }}') 
			select user_id, billing_period, service, tariff, cast(sum as DECIMAL(8,2)), cast(created_at as DATE)
				from nnaranov.stg_billing where year(created_at) = {{ execution_date.year }};
			"""
	elif table == 'issue':
		query = """
			insert overwrite table nnaranov.ods_issue partition (year='{{ execution_date.year }}') 
			select cast(user_id as INT), cast(start_time as TIMESTAMP), cast(end_time as TIMESTAMP), title, description, service
				from nnaranov.stg_issue where year(start_time) = {{ execution_date.year }};
			"""
	elif table == 'payment':
		query = """
			insert overwrite table nnaranov.ods_payment partition (year='{{ execution_date.year }}') 
			select user_id, pay_doc_type, cast(pay_doc_num as INT), account, phone, billing_period, cast(pay_date as DATE), cast(sum as DECIMAL(8,2))
				from nnaranov.stg_payment where year(pay_date) = {{ execution_date.year }};
			"""
	elif table == 'traffic':
		query = """
			insert overwrite table nnaranov.ods_traffic partition (year='{{ execution_date.year }}') 
			select user_id, cast(from_unixtime(traffic_timestamp div 1000) as TIMESTAMP), device_id, device_ip_addr, bytes_sent, bytes_received
				from nnaranov.stg_traffic where year(from_unixtime(traffic_timestamp div 1000)) = {{ execution_date.year }};
			"""
	ods.append(DataProcHiveOperator(
		task_id='ods_' + table,
		dag=dag,
		query=query,
		cluster_name='cluster-dataproc',
		job_name=USERNAME + '_ods_' + table + '_{{ execution_date.year }}_{{ params.job_suffix }}',
                params={"job_suffix": randint(0, 100000)},
		region='europe-west3',
	))
'''
	dm = DataProcHiveOperator(
	task_id='dm_traffic',
	dag=dag,
	query="""
		insert overwrite table nnaranov.dm_traffic partition (year='{{ execution_date.year }}')  
		select user_id, max(bytes_received), min(bytes_received), avg(bytes_received)
		from nnaranov.ods_traffic where year = {{ execution_date.year }} group by user_id;   
		""",
	cluster_name='cluster-dataproc',
	job_name=USERNAME + '_dm_traffic_{{ execution_date.year }}_{{ params.job_suffix }}',
	params={"job_suffix": randint(0, 100000)},
	region='europe-west3',
)
ods >> dm
'''
