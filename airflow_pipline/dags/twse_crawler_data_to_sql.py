import pendulum
from airflow.decorators import dag, task

from tasks import twse_crawler_to_sql
from airflow.providers.http.sensors.http import HttpSensor

@dag(
    schedule="0 15 * * 1-5",
    start_date=pendulum.datetime(2024, 1, 1, tz="Asia/Taipei"),
    catchup=False,
    tags=["twse"],
)
def twse_crawler_data_to_sql():
    task_http_sensor_check = HttpSensor(
    task_id="twse_check",
    http_conn_id="twse_http_connection",
    endpoint="/rwd/zh/afterTrading/MI_INDEX",
    method='GET',
    request_params={
        'date': '{{ (execution_date.in_timezone("Asia/Taipei")).strftime("%Y%m%d") }}',
        'type': 'ALL',
        'response': 'json'
    },
    response_check=lambda response: response.json().get("stat") == "OK",
    poke_interval=5,
    )
    date = pendulum.now("Asia/Taipei").format("YYYYMMDD")
    
    
    raw_data = twse_crawler_to_sql.extract_data(date)
    t_data = twse_crawler_to_sql.transform_data(raw_data)
    twse_crawler_to_sql.load_to_sql(t_data)

    task_http_sensor_check >> raw_data

twse_crawler_data_to_sql()