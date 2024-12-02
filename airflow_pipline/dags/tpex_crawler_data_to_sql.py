import time
from datetime import timedelta
import json
import pendulum
from airflow.decorators import dag, task

from tasks import tpex_crawler_to_sql
from airflow.providers.http.operators.http import HttpOperator

@dag(
    schedule="0 15 * * 1-5",
    start_date=pendulum.datetime(2024, 1, 1, tz="Asia/Taipei"),
    catchup=False,
    tags=["crawler"],
)
def tpex_crawler_data_to_sql():
    http_task = HttpOperator(
    task_id='http_task',
    method='POST',
    http_conn_id='tpex_http_connection',
    endpoint='/www/zh-tw/afterTrading/otc',
    data=json.dumps({
        "date": "{{ (execution_date.in_timezone('Asia/Taipei')).strftime('%Y%2F%m%2F%d') }}",
        "type": "AL",
        "response": "json",
    }),
    retries=5,
    retry_delay=timedelta(minutes=1),
    response_check=lambda response: response.json().get("stat") == "ok",
    )

    date = pendulum.now("Asia/Taipei").format("YYYYMMDD")

    raw_data = tpex_crawler_to_sql.extract_data(date)
    t_data = tpex_crawler_to_sql.transform_data(raw_data)
    tpex_crawler_to_sql.load_to_sql(t_data)

    http_task >> raw_data
    

tpex_crawler_data_to_sql()