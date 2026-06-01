import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("📈 서울 기온 연도별 분석")

uploaded_file = st.file_uploader(
    "CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file is not None:

    # 데이터 읽기
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # 날짜 처리
    df["날짜"] = pd.to_datetime(df["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    # 월/일 선택
    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "월 선택",
            sorted(df["월"].unique())
        )

    with col2:
        selected_day = st.selectbox(
            "일 선택",
            sorted(
                df[df["월"] == selected_month]["일"].unique()
            )
        )

    # 필터링
    filtered = df[
        (df["월"] == selected_month) &
        (df["일"] == selected_day)
    ].copy()

    filtered = filtered.sort_values("연도")

    filtered = filtered.dropna(
        subset=["최고기온(℃)", "최저기온(℃)"]
    )

    st.subheader(
        f"{selected_month}월 {selected_day}일 연도별 최고·최저기온"
    )

    fig, ax = plt.subplots(figsize=(14, 6))

    years = filtered["연도"].values
    max_temp = filtered["최고기온(℃)"].values
    min_temp = filtered["최저기온(℃)"].values

    # 최고기온 무지개색
    cmap = plt.cm.rainbow
    colors = cmap(np.linspace(0, 1, len(years)))

    for i in range(len(years)-1):
        ax.plot(
            years[i:i+2],
            max_temp[i:i+2],
            color=colors[i],
            linewidth=2.5
        )

    # 범례용
    ax.plot(
        [],
        [],
        color="red",
        linewidth=3,
        label="최고기온"
    )

    # 최저기온
    ax.plot(
        years,
        min_temp,
        color="#87CEFA",
        linewidth=2.5,
        marker="o",
        label="최저기온"
    )

    ax.set_title(
        f"{selected_month}월 {selected_day}일 연도별 기온 변화",
        fontsize=16
    )

    ax.set_xlabel("연도")
    ax.set_ylabel("기온(℃)")

    ax.grid(True, alpha=0.3)

    ax.legend()

    st.pyplot(fig)

    st.dataframe(
        filtered[
            ["연도", "최저기온(℃)", "최고기온(℃)"]
        ],
        use_container_width=True
    )

else:
    st.info("CSV 파일을 업로드하세요.")
# 날짜 변환
df["날짜"] = pd.to_datetime(
    df["날짜"],
    errors="coerce",
    format="mixed"
)

# 날짜 변환 실패 행 제거
df = df.dropna(subset=["날짜"])
