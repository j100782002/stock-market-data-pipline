from dotenv import load_dotenv
import os 
import pandas as pd
import requests
from io import StringIO
from sqlalchemy import create_engine

# 載入存在環境變數中的資料庫資訊
load_dotenv(override=True)
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")

# 建立 MySQL 連線字串
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

def extract_data(date: str) -> pd.DataFrame:
    """
    期交所爬蟲\n
    格式yyyymmdd
    """
    # 處理日期讓其方便放進API網址中
    date = str(date)
    yyyy = date[0:4]
    mm = date[4:6]
    dd = date[6:]

    # API網址
    url = "https://www.taifex.com.tw/cht/3/futDataDown"
    
    # post需要戴的參數
    form_data = {
        "down_type": "1",
        "commodity_id": "all",
        "queryStartDate": f"{yyyy}/{mm}/{dd}",
        "queryEndDate": f"{yyyy}/{mm}/{dd}" ,
    }
    
    # 取得內容
    response = requests.post(url, data=form_data)
    
    # 因為response會下載一個檔案，這邊將內容用StringIO存取，用big5編碼
    data = StringIO(response.content.decode("big5")) 
    # 將下載的CSV建成DF，不要index 
    df = pd.read_csv(data, index_col=False)
    return df

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    '''
    轉換爬下來的資料，只留下需要的欄位
    '''
    # 刪掉不需要的欄位 
    df = data.drop(columns=["最後最佳買價", "最後最佳賣價", "歷史最高價", "歷史最低價", "是否因訊息面暫停交易", "價差對單式委託成交量"])

    # 將欄位改成英文
    df.rename(columns={"交易日期": "date", "契約": "FutureID", "到期月份(週別)":"CopntractDate",
                   "開盤價": "Open", "最高價": "Max", "最低價": "Min", "收盤價": "Close", 
                   "漲跌價": "Change", "漲跌%": "ChengePer", "成交量": "Volume", "結算價": "SettlementPrice", 
                    "未沖銷契約數": "OpenInterest", "交易時段": "TradingSession"}, inplace=True)
    
    # 將TradingSession欄位內容改成英文
    df["TradingSession"] = df["TradingSession"].map({"一般": "Position", "盤後": "AfterMarket"})

    # 將欄位改成float
    df["ChengePer"] = df["ChengePer"].str.replace("%", "")
    float_columns = ["Open", "Max", "Min", "Close", "Change", "ChengePer", "SettlementPrice", "OpenInterest"]
    df[float_columns] = df[float_columns].apply(pd.to_numeric, errors='coerce')
    # 改日期格式
    df["date"] = df["date"].replace("/", "", regex=True)
    return df

def load_to_sql(data: pd.DataFrame):
    '''
    將轉換後的資料傳進MySQL
    '''
    # 將 DataFrame 插入到 MySQL 中
    # 如果資料表已存在，可將 `if_exists` 設為 'append' 以追加資料
    data.to_sql(name='taifex', con=engine, if_exists='append', index=False)

# raw_data = extract_data(20241104)
# data = transform_data(raw_data)

# load_to_sql(data)