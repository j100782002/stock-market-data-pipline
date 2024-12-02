import os
from typing import Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text


app = FastAPI()

# 載入存在環境變數中的資料庫資訊
load_dotenv(override=True)
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")

# 建立 MySQL 連線字串
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

# 定義返回數據模型
class StockInfo(BaseModel):
    StockID: str
    StockName: str
    TradeVolume: Optional[int] = None  # 可為 None，默認值為 None
    Transaction: Optional[int] = None
    TradeValue: Optional[int] = None
    Open: Optional[float] = None
    Max: Optional[float] = None
    Min: Optional[float] = None
    Close: Optional[float] = None
    Change: Optional[float] = None
    date: str

class taifexStockInfo(BaseModel):
    FutureID: str
    date: str
    CopntractDate: str
    Open: Optional[float] = None
    Max: Optional[float] = None
    Min: Optional[float] = None
    Close: Optional[float] = None
    Change: Optional[float] = None
    ChengePer: Optional[float] = None
    Volume: int
    SettlementPrice: Optional[float] = None
    OpenInterest: Optional[float] = None
    TradingSession: str



@app.get("/")
def read_root():
    return {"Hello": "World"}

# 查詢 API 路由
@app.get("/twse", response_model=List[StockInfo])
def get_stock_info(stock_id: str, start_date: str, end_date: str):
    """
    根據股票ID、起始日和結束日查詢股票資訊
    """
    query = text("""
        SELECT *
        FROM twse
        WHERE StockID = :stock_id
          AND date BETWEEN :start_date AND :end_date
        ORDER BY date ASC
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {
            "stock_id": stock_id,
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="No data found for the given parameters")
    
    # 將結果轉換為字典
    stock_info_list = [
        {
            "StockID": row.StockID,
            "date": row.date,
            "StockName": row.StockName,
            "TradeVolume": row.TradeVolume,
            "Transaction": row.Transaction,
            "TradeValue": row.TradeValue,
            "Open": row.Open,
            "Max": row.Max,
            "Min": row.Min,
            "Close": row.Close,
            "Change": row.Change,
        }
        for row in result
    ]
    return stock_info_list


@app.get("/tpex", response_model=List[StockInfo])
def get_tpex_stock_info(stock_id: str, start_date: str, end_date: str):
    """
    根據股票ID、起始日和結束日查詢股票資訊
    """
    query = text("""
        SELECT *
        FROM tpex
        WHERE StockID = :stock_id
          AND date BETWEEN :start_date AND :end_date
        ORDER BY date ASC
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {
            "stock_id": stock_id,
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="No data found for the given parameters")
    
    # 將結果轉換為字典
    stock_info_list = [
        {
            "StockID": row.StockID,
            "date": row.date,
            "StockName": row.StockName,
            "TradeVolume": row.TradeVolume,
            "Transaction": row.Transaction,
            "TradeValue": row.TradeValue,
            "Open": row.Open,
            "Max": row.Max,
            "Min": row.Min,
            "Close": row.Close,
            "Change": row.Change,
        }
        for row in result
    ]
    return stock_info_list


@app.get("/taifex", response_model=List[taifexStockInfo])
def get_taifex_stock_info(Future_id: str, start_date: str, end_date: str):
    """
    根據期貨ID、起始日和結束日查詢股票資訊
    """
    query = text("""
        SELECT *
        FROM taifex
        WHERE FutureID = :FutureID
          AND date BETWEEN :start_date AND :end_date
        ORDER BY date ASC
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {
            "FutureID": Future_id,
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="No data found for the given parameters")
    
    # 將結果轉換為字典
    stock_info_list = [
        {
            "FutureID": row.FutureID,
            "date": row.date,
            "CopntractDate": row.CopntractDate,
            "Open": row.Open,
            "Max": row.Max,
            "Min": row.Min,
            "Close": row.Close,
            "Change": row.Change,
            "ChengePer": row.ChengePer,
            "Volume": row.Volume,
            "SettlementPrice": row.SettlementPrice,
            "OpenInterest": row.OpenInterest,
            "TradingSession": row.TradingSession
        }
        for row in result
    ]
    return stock_info_list
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}