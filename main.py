
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------
# 기본 설정
# ----------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("365일간의 영화 데이터를 시간의 흐름에 따라 살펴보는 그래프 도감입니다.")

# ----------------------------------------
# 데이터 불러오기
# ----------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 관객수 열을 숫자 형식으로 변환
    df["일관객"] = pd.to_numeric(
        df["일관객"],
        errors="coerce"
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write(e)
    st.stop()


# ----------------------------------------
# 데이터 기본 정보
# ----------------------------------------
st.sidebar.header("데이터 정보")
st.sidebar.write(f"전체 기록 수: {len(df):,}개")
st.sidebar.write(
    f"조회 기간: {df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}"
)

# ========================================
# 그래프 도감 1
# 영화별 날짜에 따른 일관객 변화
# ========================================
st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)

# 영화 드롭다운
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")

# 선 그래프 만들기
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수 (명)"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,d"
    }
)

# 그래프 디자인
fig.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

fig.update_yaxes(
    tickformat=",d",
    rangemode="tozero"
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# 그래프 해석 문구 자리
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "선택한 영화의 날짜별 일관객 변화를 통해 "
    "시간의 흐름에 따른 관객 수의 증가와 감소 추이를 알 수 있습니다."
)


# ========================================
# 그래프 도감 2 (추가 예정)
# ========================================
st.divider()

st.header("📊 그래프 2. 추가 예정")

st.write(
    "앞으로 새로운 그래프를 이 구역에 추가할 예정입니다."
)

st.info("예시: 영화별 누적관객 변화, 스크린 수와 관객 수의 관계 등")


# ========================================
# 그래프 도감 3 (추가 예정)
# ========================================
st.divider()

st.header("📊 그래프 3. 추가 예정")

st.write(
    "새로운 데이터 분석 그래프를 이 구역에 추가할 예정입니다."
)
