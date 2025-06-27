from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import os
import time

def get_yahoo_eps_estimate_selenium(ticker):
    options = Options()
    options.add_argument("--headless")  # 눈에 안 보이게 백그라운드 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis"
    driver.get(url)
    time.sleep(5)  # JS 로딩 대기

    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        target_table = None
        for table in tables:
            if "Avg. Estimate" in table.text and "No. of Analysts" in table.text:
                target_table = table
                break

        if not target_table:
            print(f"[{ticker}] EPS 테이블을 찾을 수 없습니다.")
            driver.quit()
            return None

        rows = target_table.find_elements(By.TAG_NAME, "tr")
        result = {
            "ticker": ticker,
            "date": datetime.date.today().isoformat(),
            "eps_avg": None,
            "eps_high": None,
            "eps_low": None,
            "analysts": None
        }

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 3:
                continue
            label = cols[0].text.strip().lower()
            value = cols[2].text.strip()

            try:
                if "avg" in label:
                    result["eps_avg"] = float(value)
                elif "high" in label:
                    result["eps_high"] = float(value)
                elif "low" in label:
                    result["eps_low"] = float(value)
                elif "no. of analysts" in label:
                    result["analysts"] = int(value)
            except:
                continue

        driver.quit()
        return result

    except Exception as e:
        print(f"[{ticker}] 오류: {e}")
        driver.quit()
        return None


def save_to_csv(data: dict):
    if not data:
        return
    df = pd.DataFrame([data])
    path = f"data/{data['ticker']}_yahoo_eps.csv"
    if os.path.exists(path):
        df.to_csv(path, mode='a', header=False, index=False)
    else:
        df.to_csv(path, index=False)
    print(f"[{data['ticker']}] 저장 완료")


# 테스트 실행
if __name__ == "__main__":
    for ticker in ["AAPL", "MSFT", "GOOG"]:
        d = get_yahoo_eps_estimate_selenium(ticker)
        save_to_csv(d)
