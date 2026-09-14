
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
# 그래프 도감 2
# 일관객 합계 TOP 5 영화의 날짜별 변화
# ========================================
st.divider()

st.header("📈 그래프 2. 일관객 합계 TOP 5 영화의 날짜별 변화")

st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)

# 영화별 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

# TOP 5 영화 이름
top5_movie_names = top5_movies["영화명"].tolist()

# TOP 5 영화의 날짜별 데이터만 추출
top5_df = df[
    df["영화명"].isin(top5_movie_names)
].copy()

# 날짜순 정렬
top5_df = top5_df.sort_values(["날짜", "영화명"])

# 선 그래프 만들기
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수 (명)",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,d",
        "영화명": True
    }
)

# 마우스를 올렸을 때 표시되는 정보
fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}<br>"
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)

# 그래프 디자인
fig2.update_layout(
    hovermode="x unified",
    height=600,
    legend_title_text="영화"
)

fig2.update_yaxes(
    tickformat=",d",
    rangemode="tozero"
)

# 그래프 출력
st.plotly_chart(
    fig2,
    use_container_width=True
)

# 그래프 해석 문구 자리
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "전체 기간 일관객 합계가 큰 TOP 5 영화의 날짜별 관객 변화를 "
    "비교하여 영화마다 관객이 증가하고 감소하는 시점과 흥행 추이의 차이를 알 수 있습니다."
)

# TOP 5 영화별 일관객 합계 표
st.subheader("🏆 일관객 합계 TOP 5")

top5_display = top5_movies.copy()
top5_display["일관객"] = top5_display["일관객"].map(
    lambda x: f"{x:,.0f}명"
)

top5_display.index = range(1, len(top5_display) + 1)

st.dataframe(
    top5_display,
    use_container_width=True
)


# ========================================
# 그래프 도감 3
# 날짜별 박스오피스 10위권 일관객 합계
# ========================================
st.divider()

st.header("📊 그래프 3. 날짜별 박스오피스 10위권 일관객 합계")

st.write(
    "날짜별로 그날 박스오피스 10위권 영화들의 일관객을 모두 더해 "
    "전체 관객 규모의 변화를 살펴봅니다."
)

# 날짜별 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 가장 관객 합계가 컸던 날 3일
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("일관객", ascending=False)
)

# 영역 그래프 만들기
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계 (명)"
    },
    markers=True
)

# 마우스를 올렸을 때 표시되는 정보
fig3.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "10위권 일관객 합계: %{y:,}명"
    "<extra></extra>"
)

# 가장 관객 합계가 큰 날 3일을 그래프 위에 표시
annotations = []

for _, row in top3_days.iterrows():
    annotations.append(
        dict(
            x=row["날짜"],
            y=row["일관객"],
            text=(
                f"{row['날짜'].strftime('%m월 %d일')}<br>"
                f"{row['일관객']:,.0f}명"
            ),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-60,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=12, color="black")
        )
    )

# 그래프 디자인
fig3.update_layout(
    height=600,
    hovermode="x unified",
    annotations=annotations
)

fig3.update_yaxes(
    tickformat=",d",
    rangemode="tozero"
)

# 그래프 출력
st.plotly_chart(
    fig3,
    use_container_width=True
)

# 그래프 해석 문구 자리
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "날짜별 박스오피스 10위권 일관객 합계를 비교하여 "
    "전체 영화관 관객 규모가 증가하거나 감소하는 시기와 "
    "관객이 가장 많았던 날을 알 수 있습니다."
)

# 관객 합계가 가장 컸던 날 3일 표
st.subheader("🏆 일관객 합계가 가장 컸던 날 TOP 3")

top3_display = top3_days.copy()

top3_display["날짜"] = top3_display["날짜"].dt.strftime("%Y-%m-%d")

top3_display["일관객"] = top3_display["일관객"].map(
    lambda x: f"{x:,.0f}명"
)

top3_display.index = range(1, len(top3_display) + 1)

st.dataframe(
    top3_display,
    use_container_width=True
)


# ========================================
# 그래프 도감 4
# 영화별 일관객 합계 TOP 10
# ========================================
st.divider()

st.header("📊 그래프 4. 영화별 일관객 합계 TOP 10")

st.write(
    "전체 기간 동안 영화별 일관객을 모두 더해 "
    "관객이 가장 많았던 영화 TOP 10을 가로 막대그래프로 보여 줍니다."
)

# 영화별 일관객 합계 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        등장일수=("날짜", "nunique")
    )
    .reset_index()
)

# 일관객 합계가 큰 순서로 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .copy()
)

# 가로 막대그래프는 위에서부터 큰 값이 오도록
top10_movies = top10_movies.sort_values(
    "일관객합계",
    ascending=True
)

# 그래프 만들기
fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 일관객 합계 TOP 10",
    labels={
        "일관객합계": "기간 내 일관객 합계 (명)",
        "영화명": "영화"
    },
    hover_data={
        "일관객합계": ":,d",
        "등장일수": True
    },
    text="일관객합계"
)

# 막대에 표시할 텍스트
fig4.update_traces(
    texttemplate="%{text:,}명",
    textposition="outside",
    hovertemplate=
    "영화: %{y}<br>"
    "기간 내 일관객 합계: %{x:,}명<br>"
    "10위권에 든 날수: %{customdata[0]}일"
    "<extra></extra>",
    customdata=top10_movies[["등장일수"]].values
)

# 그래프 디자인
fig4.update_layout(
    height=600,
    yaxis={
        "categoryorder": "total ascending"
    },
    margin=dict(l=20, r=100, t=80, b=50)
)

fig4.update_xaxes(
    tickformat=",d",
    rangemode="tozero"
)

# 그래프 출력
st.plotly_chart(
    fig4,
    use_container_width=True
)

# 그래프 해석 문구 자리
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "기간 내 일관객 합계가 큰 영화들을 비교하여 "
    "어떤 영화가 가장 많은 관객을 모았는지와 "
    "10위권에 등장한 날수를 알 수 있습니다."
)

# TOP 10 표
st.subheader("🏆 영화별 일관객 합계 TOP 10")

top10_display = top10_movies.copy()

top10_display = top10_display.sort_values(
    "일관객합계",
    ascending=False
)

top10_display["일관객합계"] = top10_display["일관객합계"].map(
    lambda x: f"{x:,.0f}명"
)

top10_display["등장일수"] = top10_display["등장일수"].map(
    lambda x: f"{x}일"
)

top10_display.index = range(1, len(top10_display) + 1)

st.dataframe(
    top10_display,
    use_container_width=True
)


# ========================================
# 그래프 도감 5
# 월 × 요일별 일관객 합계 히트맵
# ========================================
st.divider()

st.header("📊 그래프 5. 월 × 요일별 일관객 합계 히트맵")

st.write(
    "날짜에서 월과 요일을 뽑아, "
    "월별·요일별 일관객 합계를 색으로 비교합니다."
)

# 데이터 복사
heatmap_df = df.copy()

# 월 추출
heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 요일 추출
# dayofweek: 월요일=0, 일요일=6
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek

heatmap_df["요일명"] = heatmap_df["요일"].map(
    dict(enumerate(weekday_names))
)

# 월 × 요일별 일관객 합계
heatmap_data = (
    heatmap_df
    .groupby(["월", "요일", "요일명"], as_index=False)["일관객"]
    .sum()
)

# 요일 순서를 월요일 → 일요일로 고정
heatmap_data["요일명"] = pd.Categorical(
    heatmap_data["요일명"],
    categories=weekday_names,
    ordered=True
)

# 피벗 테이블
heatmap_pivot = heatmap_data.pivot(
    index="월",
    columns="요일명",
    values="일관객"
)

# 월 순서 정렬
heatmap_pivot = heatmap_pivot.sort_index()

# 월 이름 표시
heatmap_pivot.index = [
    f"{month}월"
    for month in heatmap_pivot.index
]

# 히트맵 만들기
fig5 = px.imshow(
    heatmap_pivot,
    labels=dict(
        x="요일",
        y="월",
        color="일관객 합계 (명)"
    ),
    x=weekday_names,
    y=heatmap_pivot.index,
    color_continuous_scale="YlOrRd",
    aspect="auto",
    title="월 × 요일별 일관객 합계"
)

# 마우스를 올렸을 때 표시되는 정보
fig5.update_traces(
    hovertemplate=
    "월: %{y}<br>"
    "요일: %{x}<br>"
    "일관객 합계: %{z:,}명"
    "<extra></extra>"
)

# 그래프 디자인
fig5.update_layout(
    height=600
)

# 그래프 출력
st.plotly_chart(
    fig5,
    use_container_width=True
)

# 그래프 해석 문구 자리
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "월과 요일에 따른 일관객 합계를 색의 진하기로 비교하여 "
    "어느 월과 요일에 박스오피스 10위권 관객이 많았는지 알 수 있습니다."
)
