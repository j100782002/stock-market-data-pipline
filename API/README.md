# stock-market-data-FASTAPI## 

專案簡介
獲取MySQL的證交所、櫃買中心與期交所收盤資料。

## 目錄結構
- [專案功能](#專案功能)
- [安裝步驟](#安裝步驟)
- [使用方式](#使用方式)


## 專案功能
- 從證交所、櫃買中心與期交所爬取收盤資料至並載入至MySQL。
- 

## 安裝步驟
### 1. 克隆專案到本地

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. 設定MySQL連線
在code目錄新增一個.env檔，並輸入以下內容:
username="your-username"
password="your-password"
host="your-host"
database="your-database-name"

### 3. 建image
```bash
docker build -t < image-name >:v1 . 
```

### 3. 啟動服務
```bash
docker run -d --name < container-name > -p 80:80 < image-name >
```

### 4. http://localhost:80/docs查看使用方式



