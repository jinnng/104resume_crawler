# 104resume_crawler
Fetch resumes from 104 website, and parse via ChatGPT
# 建置環境

### Python 安裝

版本: Python 3.11
[Python 3.11 下載連結](https://www.python.org/downloads/release/python-3110/)

### 環境設定

1. Clone 專案 autohunter：
   - git clone 專案autohunter


2. (選用) Python 虛擬環境：

   - 安裝 virtualenv：
    ```cmd
    pip install virtualenv
    ```

    - 建立虛擬環境：

    ```cmd
    virtualenv venv
    ```

    - 啟動虛擬環境：

    ```cmd
    .\venv\Scripts\activate
    ```

    - 離開虛擬環境：

    ```cmd
    deactivate
    ```

3. 安裝套件：

    ```cmd
    pip install -r requirements.txt
    ```

4. 將 workspace 資料放置於本機


5. 設定環境變數：

    ```cmd
    set PYTHONPATH=%PYTHONPATH%;'your local development path'
    Set "OPENAI_API_BASE=<https://gptrd.enoir.org/v1>"
    Set OPENAI_API_KEY='your OpenAI key'
    Set WORKSPACE="step 3 path"  # 換成步驟3 workspace 放置的路徑
    Set "SEARCH_URL=<https://vip.104.com.tw/search/searchResult?kws=.NET>"
    ```

### 程式執行

```cmd
cd scripts
python website_grab.py
```

# 執行結果

workspace路徑下產生以日期為名稱之資料夾，包含
1. match_report_yyyymmdd_id.csv
   - 記錄人員是否適合邀請面試


2. report資料夾
   - 記錄AI分析結果文字檔


3. resume資料夾
   - 存放履歷html


4. resume_text資料夾
   - 存放履歷文字檔
