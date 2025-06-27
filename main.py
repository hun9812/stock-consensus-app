import streamlit as st
import pandas as pd
import os
from scraper import get_yahoo_eps_estimate_selenium, save_to_csv

st.set_page_config(page_title="EPS 예측 추적기", layout="wide")
st.title("📈 EPS 예측 데이터 분석기")

# 🔍 티커 직접 입력
ticker = st.text_input("티커를 입력하세요 (예: AAPL)", value="AAPL").upper().strip()

# 📥 즉시 수집 버튼
if st.button("📥 즉시 수집하기"):
    st.info(f"{ticker} 데이터 수집 중...")
    data = get_yahoo_eps_estimate_selenium(ticker)
    if data:
        save_to_csv(data)
        st.success(f"{ticker} 데이터 수집 완료! 새로고침 중...")
        st.rerun()
    else:
        st.error(f"{ticker} 데이터 수집 실패")

# 📁 파일 경로
path = f"data/{ticker}_yahoo_eps.csv"

# 📊 데이터 시각화
if os.path.exists(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])

    st.subheader("📋 최신 예측")
    st.dataframe(df.sort_values("date", ascending=False).head(1))

    st.subheader("📈 평균 EPS 예측 추이")
    st.line_chart(df.set_index("date")[["eps_avg"]])

    st.subheader("📉 EPS 범위 (Low ~ High)")
    st.area_chart(df.set_index("date")[["eps_low", "eps_high"]])
else:
    st.warning("❗ 수집된 데이터가 없습니다. 상단에서 수집 버튼을 눌러주세요.")
