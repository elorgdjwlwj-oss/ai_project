import streamlit as st
import pandas as pd

st.set_page_config(page_title="야구선수 인기순위", layout="wide")

data = [
    [1, "김서현", "한화 이글스", 100],
    [2, "윤동희", "롯데 자이언츠", 96],
    [3, "김도영", "KIA 타이거즈", 94],
    [4, "구자욱", "삼성 라이온즈", 92],
    [5, "류현진", "한화 이글스", 91],
    [6, "박해민", "LG 트윈스", 89],
    [7, "강민호", "삼성 라이온즈", 88],
    [8, "최형우", "KIA 타이거즈", 86],
    [9, "원태인", "삼성 라이온즈", 85],
    [10, "김원중", "롯데 자이언츠", 84]
]

df = pd.DataFrame(
    data,
    columns=["순위", "선수", "팀", "인기점수"]
)

st.title("⚾ 야구선수 인기순위 TOP 10")

st.dataframe(df, use_container_width=True)

st.bar_chart(
    df.set_index("선수")["인기점수"]
)

player = st.selectbox(
    "선수 선택",
    df["선수"]
)

info = df[df["선수"] == player].iloc[0]

st.subheader(player)
st.write(f"순위 : {info['순위']}위")
st.write(f"소속팀 : {info['팀']}")
st.write(f"인기점수 : {info['인기점수']}")
