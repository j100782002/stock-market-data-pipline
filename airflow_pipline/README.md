# airflow-pipline## 

專案簡介
週一到週五下午3點會去檢查證交所、櫃買中心與期交所網站的當日收盤資料是否釋出，如果釋出會開始ETL，將當日資料載入至MySQL。

## 目錄結構
- [專案功能](#專案功能)
- [安裝步驟](#安裝步驟)
- [使用方式](#使用方式)


## 專案功能
- 從證交所、櫃買中心與期交所爬取收盤資料至並載入至MySQL。


## 安裝步驟
### 1. 克隆專案到本地

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. 設定MySQL連線
在根目錄新增一個.env檔，並輸入以下內容:
username="your-username"
password="your-password"
host="your-host"
database="your-database-name"

### 3. 啟動服務
```bash
docker compose up -d
```

### 4. 到airflow web(localhost:8080)設定http sensor和http operator的connection
設定以下三個connection:
-Conn id : twse_http_connection
Conn type : HTTP
Host :https://www.twse.com.tw
-Conn id : tpex_http_connection
Conn type : HTTP
Host :https://www.tpex.org.tw
-Conn id taifex_http_connection
Conn type : HTTP
Host :https://www.taifex.com.tw


### 4. 開始排程
