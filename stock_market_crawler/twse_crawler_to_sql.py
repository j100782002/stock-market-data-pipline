from dotenv import load_dotenv
import os 
import pandas as pd
import requests
from sqlalchemy import create_engine

# 載入存在環境變數中的資料庫資訊
load_dotenv(override=True)
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")

# 建立 MySQL 連線字串
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

def extract_data(date: str) -> dict:
    '''
    輸入日期就能爬當日的大盤收盤行情\n
    輸入格式yyyymmdd
    '''
    # 將輸入值改成字串
    date = str(date)
    # 將日期變數帶入API網址
    url = (
        "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX"
        f"?date={date}&type=ALL&response=json"
    )
    # 取得API內容
    response = requests.get(url)
    data = response.json()
    # 處裡遇到假日股市沒開時得到的資料
    if data["stat"] == "很抱歉，沒有符合條件的資料!":
        return {"date": "holiday"}
    return {"date":date, "data": data["tables"][8]["data"]}


def transform_data(data: dict) -> pd.DataFrame:
    '''
    轉換爬下來的資料，只留下需要的欄位
    '''
    # DF欄位
    columns = [
    "StockID", "StockName", "TradeVolume", "Transaction", "TradeValue",
    "Open", "Max", "Min", "Close", "Dir", 
    "Change", "最後揭示買價", "最後揭示買量", "最後揭示賣價", 
    "最後揭示賣量", "本益比"
    ]

    # 如果是假日回傳一個空的DF
    if data["date"] == "holiday":
        return pd.DataFrame(columns=columns)
    
    # 建立DF
    df = pd.DataFrame(data=data["data"], columns=columns)

    # 原始資料將漲跌分成兩欄，一欄為+-，一欄為值，這邊將兩欄合為一欄，並刪除原始欄位
    df["Dir"] = df["Dir"].str.split(">").str[1].str[0]
    df["Change_new"] = df["Dir"] + df["Change"]
    df = df.drop(columns=["Dir", "Change"])
    df.rename(columns={"Change_new": "Change"}, inplace=True)

    # 刪除不需要的欄位
    df = df.drop(columns=["最後揭示買價", "最後揭示買量", "最後揭示賣價", "最後揭示賣量", "本益比"])

    # 這兩欄的數字有逗號，為了將其資料格式轉為int，先將逗號拿掉
    columns_with_commas = ["TradeVolume", "TradeValue", "Transaction"]
    df[columns_with_commas] = df[columns_with_commas].replace(",", "", regex=True)

    # 將需要轉換為整數的欄位
    int_columns = ["TradeVolume", "Transaction", "TradeValue", ]

    # 將需要轉換為浮點數的欄位
    float_columns = ["Open", "Max", "Min", "Close", "Change"]

    # 將指定的欄位轉換為整數類型 (int)，並支援 NaN 值
    df[int_columns] = df[int_columns].apply(pd.to_numeric, errors='coerce').astype("Int64")

    # 將指定的欄位轉換為浮點數類型 (float)，並支援 NaN 值
    df[float_columns] = df[float_columns].apply(pd.to_numeric, errors='coerce')

    # 建立日期欄位
    df["date"] = data["date"]
    return df


def load_to_sql(data: pd.DataFrame):
    '''
    將轉換後的資料傳進MySQL
    '''
    # 將 DataFrame 插入到 MySQL 中
    # 如果資料表已存在，可將 `if_exists` 設為 'append' 以追加資料
    data.to_sql(name='twse', con=engine, if_exists='append', index=False)



# raw_data = extract_data(20040811)
# t_data = transform_data(raw_data)
# load_to_sql(t_data)
