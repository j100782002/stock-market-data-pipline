import pendulum
from airflow.decorators import dag, task

from tasks import tpex_crawler_to_sql

@dag(
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2024, 1, 1, tz="Asia/Taipei"),
    catchup=False,
    tags=["crawler"],
)
def tpex_crawler_data_to_sql():
    date = pendulum.now("Asia/Taipei").format("YYYYMMDD")

    raw_data = tpex_crawler_to_sql.extract_data(date)
    t_data = tpex_crawler_to_sql.transform_data(raw_data)
    tpex_crawler_to_sql.load_to_sql(t_data)

tpex_crawler_data_to_sql()