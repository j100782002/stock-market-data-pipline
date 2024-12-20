# stock-market-data-pipline

## 專案動機:
投資與交易的核心在於對市場資訊的深入理解。然而，收盤行情資料的取得往往需要耗費大量時間與精力，尤其是對於想要進行長期歷史分析或即時應用的使用者。為了讓用戶能夠更專注於數據分析與應用，而非資料收集的繁瑣流程，我設計了這套系統。
該系統旨在整合證交所、櫃買中心與期交所的歷史與即時收盤行情資料，並自動化更新流程，提供即時且高效的資料存取服務。透過此系統，用戶不再需要耗時整理數據，而是能將更多精力聚焦於分析策略及實際應用，助力他們在投資決策中脫穎而出。

## 使用說明
- 此專案分3個部分，歷史資料爬取、即時資料排程爬取、API取得資料，分別對應stock_market_crawler、airflow_pipline、API資料夾，裡面有寫使用方式。
- 另外請自己準備習慣的資料庫，我專案是使用MySQL。