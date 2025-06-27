import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="EPS 예측 추적기", layout="wide")
st.title("📈 EPS 예측 데이터 분석기")

# 🔍 티커 직접 입력
ticker = st.text_input("티커를 입력하세요 (예: AAPL)", value="AAPL").upper().strip()

# ❌ Streamlit Cloud에서는 selenium이 안 되므로 이 부분은 제거하거나 대체 필요
# from scraper import get_yahoo_eps_estimate_selenium, save_to_csv

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
    st.warning("❗ 수집된 데이터가 없습니다. GitHub Actions를 통해 자동 수집되도록 설정되어 있어야 합니다.")
