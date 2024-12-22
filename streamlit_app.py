import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Streamlit 페이지 설정
st.set_page_config(page_title="행사 신청", page_icon="📃")
st.title("📃 행사 신청 사이트")
st.info("골든래빗고 행사 신청 사이트입니다. 아래의 양식에 맞게 기입하여 '제출'버튼을 눌러주세요. 현재시간까지 신청 현황은 아래에서 확인할 수 있습니다.")

# 신청자 현황 대시보드
st.subheader("신청자 현황 대시보드")
st.write("현재까지 신청자 현황입니다. 신청 시 참고해주세요.")

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.write(f"**현재 시간:** {current_time}")

# 새로고침 버튼 추가
if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()  # 페이지를 다시 실행하여 데이터를 갱신

# 데이터 읽기
df = conn.read()

# 신청 날짜 데이터 처리 및 시각화
if not df.empty:
    dates = df['신청 날짜'].str.split(', ').explode()
    st.bar_chart(dates.value_counts())
else:
    st.warning("현재 신청 데이터가 없습니다.")

# 구글 폼 삽입
iframe_url = 'https://forms.gle/tqcE1P23xVwPm1LT9'
st.components.v1.iframe(src=iframe_url, width=None, height=500, scrolling=True)
