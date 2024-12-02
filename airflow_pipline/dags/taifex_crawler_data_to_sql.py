import pendulum
from airflow.decorators import dag, task
from airflow.providers.http.operators.http import HttpOperator
from tasks import taifex_crawler_to_sql
import json
from datetime import timedelta
from io import StringIO

def check_file_in_response(response):
    try:
        # 將回應內容解碼為指定編碼（big5），並嘗試轉換為 StringIO
        data = StringIO(response.content.decode("big5"))
        # 如果成功轉換並內容不為空，返回 True
        return bool(data.getvalue().strip())
    except Exception as e:
        # 如果發生錯誤，回傳 False
        print(f"Error decoding response: {e}")
        return False


@dag(
    schedule="0 15 * * 1-5",
    start_date=pendulum.datetime(2024, 1, 1, tz="Asia/Taipei"),
    catchup=False,
    tags=["crawler"],
)
def taifex_crawler_data_to_sql():
    http_task = HttpOperator(
    task_id='http_task',
    method='POST',
    http_conn_id='taifex_http_connection',
    endpoint='/cht/3/futDataDown',
    data=json.dumps({
        "down_type": "1",
        "commodity_id": "all",
        "queryStartDate": "{{ (execution_date.in_timezone('Asia/Taipei')).strftime('%Y/%m/%d') }}",
        "queryEndDate": "{{ (execution_date.in_timezone('Asia/Taipei')).strftime('%Y/%m/%d') }}",
    }),
    retries=5,
    retry_delay=timedelta(minutes=1),
    response_check=check_file_in_response,
    )
    date = pendulum.now("Asia/Taipei").format("YYYYMMDD")

    raw_data = taifex_crawler_to_sql.extract_data(date)
    t_data = taifex_crawler_to_sql.transform_data(raw_data)
    taifex_crawler_to_sql.load_to_sql(t_data)

    http_task >> raw_data

taifex_crawler_data_to_sql()