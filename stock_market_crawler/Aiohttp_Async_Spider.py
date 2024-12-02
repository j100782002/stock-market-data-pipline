from dotenv import load_dotenv
from datetime import datetime, timedelta
import os 

import asyncio
from sqlalchemy import create_engine

import twse_crawler_to_sql
import tpex_crawler_to_sql
import taifex_crawler_to_sql


# 定義主協程函數，用於調用三個 API 爬蟲
async def main(start_date_str, end_date_str):
    # 將日期字串轉換為 datetime 對象，日期格式為 "YYYYMMDD"
    start_date = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")
    
    # 產生包含起始日到終止日之間的所有日期的列表
    date_list = [(start_date + timedelta(days=i)).strftime("%Y%m%d") for i in range((end_date - start_date).days + 1)]
    

     # 定義抓取指定日期的協程
    async def fetch_date(api_module, date):
        # 調用 API 模組中的資料抓取函數，使用日期參數
        raw_data = api_module.extract_data(date)
        # 調用 API 模組中的資料清理函數
        transformed_data = api_module.transform_data(raw_data)
        # 調用 API 模組中的資料上傳函數，將清理後的資料上傳到 MySQL
        api_module.load_to_sql(transformed_data)
        # 每抓取一天的資料後休眠 5 秒
        await asyncio.sleep(5)
    

    # 遍歷所有日期，為每個日期運行三個 API 的抓取函數
    for date in date_list:
        task1 = asyncio.create_task(fetch_date(twse_crawler_to_sql, date))
        task2 = asyncio.create_task(fetch_date(tpex_crawler_to_sql, date))
        task3 = asyncio.create_task(fetch_date(taifex_crawler_to_sql, date))

        # 等待三個抓取任務完成
        await task1
        await task2
        await task3
        
        
# 獲取當前的事件循環
loop = asyncio.get_event_loop()
# 運行主協程函數直到完成，指定日期範圍
start_date_str = input("起始日期:")
end_date_str = input("結束日期:")
loop.run_until_complete(main(start_date_str, end_date_str))
# 關閉事件循環
loop.close()
