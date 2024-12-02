# stock-market-crawler

## 簡介
執行Aiohttp_Async_Spider.py後，輸入起始日期和結束日期後會爬取證交所、櫃買中心與期交所的歷史收盤行情資料，注意日期輸入格式為yyyymmdd。

## 目錄結構
- [安裝步驟](#安裝步驟)
- [使用方式](#使用方式)


## 安裝步驟
### 1. 克隆專案到本地

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. 用`pipenv` 安裝依賴
```bash
pipenv install
```

### 3. 啟動虛擬環境
```bash
pipenv shell
```

### 4. 設定 MySQL 連線
新增一個.env檔，並輸入以下內容:
username="your-username"
password="your-password"
host="your-host"
database="your-database-name"


### 6. 運行專案
```bash
python Aiohttp_Async_Spider.py
```

## 使用方式

1. 運行後會問你起始日期和結束日期
2. 輸入後會開始爬取資料，並將資料載入MySQL
