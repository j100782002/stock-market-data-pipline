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
    輸入日期就能抓當日的上貴收盤行情\n
    格式yyyymmdd
    ''' 
    # 處理日期讓其方便放進API網址中
    date = str(date)
    yyyy = date[0:4]
    mm = date[4:6]
    dd = date[6:]

    # 將日期變數帶入API網址
    url = (
        "https://www.tpex.org.tw/www/zh-tw/afterTrading/otc"
        f"?date={yyyy}%2F{mm}%2F{dd}&type=AL&id=&response=json"
    )

    # 取得API內容
    response = requests.get(url)
    data = response.json()
    # 處裡遇到假日股市沒開時得到的資料
    if not data["tables"][0]["data"]:
        return {"date": "holiday"}
    return {"date": date, "data": data["tables"][0]["data"]}

def transform_data(data: dict) -> pd.DataFrame:
    '''
    轉換爬下來的資料，只留下需要的欄位
    '''
    # DF欄位
    columns = ["StockID","StockName", "Close", "Change",
            "Open", "Max", "Min", "TradeVolume",
            "TradeValue", "Transaction", "最後買價","最後買量<br>(千股)", 
            "最後賣價", "最後賣量<br>(千股)", "發行股數", 
            "次日漲停價", "次日跌停價"            
            ]
    
    # 如果是假日回傳一個空的DF
    if data["date"] == "holiday":
        return pd.DataFrame(columns=columns)
    
    # 建立DF
    df = pd.DataFrame(data=data["data"], columns=columns)

    # 刪掉不需要的欄位
    df = df.drop(columns=["最後買價", "最後買量<br>(千股)", "最後賣價", "最後賣量<br>(千股)", "發行股數", "次日漲停價", "次日跌停價"])
    
    # 這兩欄的數字有逗號，為了將其資料格式轉為int，先將逗號拿掉
    columns_with_commas = ["TradeVolume", "TradeValue","Transaction"]
    df[columns_with_commas] = df[columns_with_commas].replace(",", "", regex=True)

    # 將需要轉換為整數的欄位
    int_columns = ["TradeVolume", "Transaction", "TradeValue", ]

    # 將需要轉換為浮點數的欄位
    float_columns = ["Open", "Max", "Min", "Close", "Change"]

    # 將指定的欄位轉換為整數類型 (int)，並支援 NaN 值
    df[int_columns] = df[int_columns].apply(pd.to_numeric, errors='coerce').astype("Int64")

    # 將指定的欄位轉換為浮點數類型 (float)，並支援 NaN 值
    df[float_columns] = df[float_columns].apply(pd.to_numeric, errors='coerce')

    df["date"] = data["date"]
    return df


def load_to_sql(data: pd.DataFrame):
    '''
    將轉換後的資料傳進MySQL
    '''
    # 將 DataFrame 插入到 MySQL 中
    # 如果資料表已存在，可將 `if_exists` 設為 'append' 以追加資料
    data.to_sql(name='tpex', con=engine, if_exists='append', index=False)


# raw_data = extract_data(20211103)
# data = transform_data(raw_data)
# load_to_sql(data)