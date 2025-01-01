import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Streamlit 페이지 설정
st.set_page_config(page_title="설문응답공유", page_icon="📃")
st.title("📃 디지털 기반 업무 적용 실천하기!")
st.info("**동계 1정 연수 : 디지털 기반 업무의 실제 강의**를 들으신 후, 아이디어를 공유하는 장입니다. 선생님들의 창의적인 아이디어를 서로 공유해주세요! 다른 선생님들의 아이디어를 보고 개선시키는 것도 가능합니다:)")

# 구글 폼 삽입
iframe_url = 'https://forms.gle/6MCgNgMEQXRPkW9v8'
st.components.v1.iframe(src=iframe_url, width=None, height=500, scrolling=True)
st.subheader("공유된 응답 대시보드")

with st.expander("공유된 응답 살펴보기"):
    try:
        # 구글 시트 연결
        conn = st.connection("gsheets", type=GSheetsConnection)

        # 한국 시간 (KST) 설정
        kst = pytz.timezone("Asia/Seoul")
        current_time_kst = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

        # 새로고침 버튼 추가
        if st.button("🔄 데이터 새로고침"):
            st.cache_data.clear()

        # 데이터 읽기
        df = conn.read()

        if not df.empty:
            data = df.iloc[:, 1].str.split(', ').explode()

            # 응답 수 계산
            response_count = data.value_counts()

            # 응답 데이터를 시각화하기 위해 데이터프레임으로 변환
            response_df = response_count.reset_index()
            response_df.columns = ["응답 내용", "응답 수"]

            # 응답 수 기준으로 내림차순 정렬
            response_df = response_df.sort_values(by="응답 수", ascending=False)
            # st.write(response_df)

            # 응답자 총합
            total_respondents = len(df)
            st.write(f"**{total_respondents}명**의 응답이 모였네요! **현재 시간:** {current_time_kst}")

            # Streamlit 바 차트로 시각화
            st.subheader("1. 적용하고 싶은 분야")
            st.bar_chart(response_df.set_index("응답 내용")["응답 수"], color="#ffaa00", horizontal=True)
            st.subheader("2. 실천 아이디어")
            st.write(df.iloc[:, 2])
            st.subheader("3. 프롬프트 공유 및 설명")
            st.write(df.iloc[:, 3].dropna())
        else:
            st.warning("현재 신청 데이터가 없습니다.")

    except Exception as e:
        st.error("데이터를 불러올 수 없네요!")
