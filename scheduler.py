import os
import time
import glob
from scraper import get_yahoo_eps_estimate_selenium, save_to_csv

def get_tracked_tickers():
    csv_files = glob.glob("data/*_yahoo_eps.csv")
    tickers = [os.path.basename(f).split("_")[0] for f in csv_files]
    return tickers

def update_all():
    tickers = get_tracked_tickers()
    print(f"총 {len(tickers)}개 티커 업데이트 시작: {tickers}")
    for ticker in tickers:
        data = get_yahoo_eps_estimate_selenium(ticker)
        if data:
            save_to_csv(data)
            print(f"[{ticker}] 업데이트 완료")
        else:
            print(f"[{ticker}] 업데이트 실패")

if __name__ == "__main__":
    while True:
        update_all()
        print("모든 티커 업데이트 완료. 1시간 대기 중...")
        time.sleep(60 * 60)  # 1시간마다 반복
