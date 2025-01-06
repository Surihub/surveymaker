import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Streamlit 페이지 설정
st.set_page_config(page_title="행사 신청", page_icon="📃")
st.title("📃 디지털 기반 업무 적용 실천하기!")
st.info("**동계 1정 연수 : 디지털 기반 업무의 실제 강의**를 들으신 후, 아이디어를 공유하는 장입니다. 선생님들의 창의적인 아이디어를 서로 공유해주세요! 다른 선생님들의 아이디어를 보고 개선시키는 것도 가능합니다:)")

# 구글 폼 삽입
iframe_url = 'https://forms.gle/6MCgNgMEQXRPkW9v8'
st.components.v1.iframe(src=iframe_url, width=None, height=500, scrolling=True)

# 신청자 현황 대시보드
st.subheader("공유된 응답 대시보드")
# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 한국 시간 (KST) 설정
kst = pytz.timezone("Asia/Seoul")
current_time_kst = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

# 새로고침 버튼 추가
if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()  # 페이지를 다시 실행하여 데이터를 갱신

# 데이터 읽기
df = conn.read()


# 신청 날짜 데이터 처리 및 시각화
if not df.empty:
    data = df.iloc[:, 1].str.split(', ').explode()
    response_count = data.value_counts()
    
    # 응답자 총합
    total_respondents = len(df)
    st.write(f"**{total_respondents}명**의 응답이 모였네요! **현재 시간:** {current_time_kst}")
    
    # Matplotlib을 이용한 원그래프
    # st.subheader("응답자 현황: 원그래프")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        response_count.values, 
        labels=response_count.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=sns.color_palette("pastel"),
        textprops={'fontsize': 12}
    )
    # ax.set_title("응답자 현황", fontsize=16, fontweight="bold")
    
    # Streamlit에 그래프 표시
    st.pyplot(fig)
else:
    st.warning("현재 신청 데이터가 없습니다.")
