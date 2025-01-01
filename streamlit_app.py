import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Streamlit 페이지 설정
st.set_page_config(page_title="설문응답공유", page_icon="📃", layout="centered")
st.title("📃 디지털 기반 업무 적용 실천하기!")
st.info(
    """
    **동계 1정 연수 : 디지털 기반 업무의 실제 강의**를 들으신 후, 아이디어를 공유하는 장입니다.  
    선생님들의 창의적인 아이디어를 서로 공유해주세요! 다른 선생님들의 아이디어를 보고 개선시키는 것도 가능합니다. 😊  
    """
)

# 구글 폼 섹션
survey_url = 'https://forms.gle/6MCgNgMEQXRPkW9v8'

st.subheader("⌨️ 설문 응답하기")
st.link_button("설문지 새 창으로 열기", survey_url)
st.components.v1.iframe(src=survey_url, width=None, height=400, scrolling=True)

# 응답 대시보드 섹션
st.subheader("📊 응답 대시보드")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)

    kst = pytz.timezone("Asia/Seoul")
    current_time_kst = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

    if st.button("🔄 데이터 새로고침"):
        st.cache_data.clear()

    df = conn.read()

    if not df.empty:
        data = df.iloc[:, 1].str.split(', ').explode()

        response_count = data.value_counts()
        response_df = response_count.reset_index()
        response_df.columns = ["응답 내용", "응답 수"]
        response_df = response_df.sort_values(by="응답 수", ascending=False)

        total_respondents = len(df)
        st.success(f"**{total_respondents}명**의 응답이 모였습니다! 🕒 **현재 시간:** {current_time_kst}")

        st.subheader("1️⃣ 적용하고 싶은 분야")
        st.bar_chart(response_df.set_index("응답 내용")["응답 수"])

        st.subheader("2️⃣ 실천 아이디어")
        st.write(df.iloc[:, 2].dropna())

        st.subheader("3️⃣ 프롬프트 공유 및 설명")
        st.write(df.iloc[:, 3].dropna())
    else:
        st.warning("현재 응답 데이터가 없습니다. 😔")

except Exception as e:
    st.error("❌ 데이터 불러오기에 실패했습니다. 관리자에게 문의해주세요!")
# 하단 Made by 메시지
st.markdown(
    """
    <div style="text-align: center; padding: 10px; background-color: #f8f9fa; color: #6c757d; border-top: 1px solid #dee2e6;">
        <p><strong>Made with ❤️ by 반포고 황수빈</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)
