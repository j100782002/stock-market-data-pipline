import os
import pendulum
from airflow.decorators import dag, task
from dotenv import load_dotenv
from tasks import twse_crawler_to_sql
from sqlalchemy import create_engine
import pandas as pd

@dag(
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2024, 1, 1, tz="Asia/Taipei"),
    catchup=False,
    tags=["crawler"],
)
def twse_crawler_data_to_sql():
    date = pendulum.now("Asia/Taipei").format("YYYYMMDD")
    
    raw_data = twse_crawler_to_sql.extract_data(date)
    t_data = twse_crawler_to_sql.transform_data(raw_data)
    twse_crawler_to_sql.load_to_sql(t_data)

twse_crawler_data_to_sql()