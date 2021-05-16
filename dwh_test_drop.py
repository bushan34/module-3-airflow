#DROP VIEW nnaranov.view_payment_2013;
#DROP VIEW nnaranov.view_payment_2014
/*
SQL_CONTEXT = {
    'DROP_VIEW_PAYMENT': """
          drop view if exists nnaranov.view_payment_{{ execution_date.year }};
     """
}
username = 'nnaranov'
default_args = {
    'owner': username,
    'depends_on_past': False,
    'start_date': datetime(2013, 1, 1, 0, 0, 0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=120),
}

dag = DAG(
    username + '.dwh_test_drop',
    default_args=default_args,
    description='DWH Drop',
    schedule_interval="0 0 1 1 *",
    concurrency=1,
    max_active_runs=1,
)

drop_view_payment = PostgresOperator(
    task_id='DROP_VIEW_PAYMENT',
    dag=dag,
    sql=SQL_CONTEXT['DROP_VIEW_PAYMENT']
*/
