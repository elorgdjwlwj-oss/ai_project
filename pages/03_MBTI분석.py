import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정
st.set_page_config(page_title="글로벌 MBTI 데이터 분석기", layout="centered")
st.title("🌍 글로벌 MBTI 데이터 시각화 대시보드")

# 2. 데이터 불러오기 (캐싱 처리)
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
    mbti_types = df.columns[1:]  # INFJ, ISFJ ... 16가지 유형 추출

    # 탭 메뉴 구성 (1. 국가별 조회 / 2. MBTI별 조회)
    tab1, tab2 = st.tabs(["🏳️‍🌈 국가별 MBTI 비율", "🧩 MBTI별 국가 순위 (Top 10)"])

    # ---------------------------------------------------------
    # TAB 1: 국가별 MBTI 비율 (1등부터 내림차순, 초록 그라데이션)
    # ---------------------------------------------------------
    with tab1:
        st.subheader("국가별 MBTI 분포 확인")
        country_list = sorted(df['Country'].unique())
        selected_country = st.selectbox("분석할 국가를 선택하세요:", country_list, key="country_select")
        
        # 선택된 국가 데이터 추출 및 백분율 변환
        country_data = df[df['Country'] == selected_country].iloc[0]
        percentages = [country_data[mbti] * 100 for mbti in mbti_types]
        
        # 1등부터 나오도록 내림차순(ascending=False) 정렬
        plot_df_country = pd.DataFrame({
            'MBTI': mbti_types,
            'Percentage': percentages
        }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)
        
        # 초록색 그라데이션 색상 설계 (1등 노란색, 이후 초록색 명도 조절)
        colors_country = []
        n_items_country = len(plot_df_country)
        for i in range(n_items_country):
            if i == 0:
                colors_country.append('rgba(255, 215, 0, 0.95)')  # 1등: 골드/노란색
            else:
                # 순위가 내려갈수록 진한 초록(ForestGreen 계열)에서 투명도를 낮춰 흐려지게 만듦
                alpha = max(0.95 - (i * 0.05), 0.15)
                colors_country.append(f'rgba(34, 139, 34, {alpha})')
        
        # Plotly 막대그래프 생성
        fig_country = go.Figure(data=[go.Bar(
            x=plot_df_country['MBTI'],
            y=plot_df_country['Percentage'],
            text=plot_df_country['Percentage'].round(2).astype(str) + '%',
            textposition='auto',
            marker_color=colors_country,
            marker_line=dict(color='rgba(0,0,0,0.1)', width=1)
        )])
        
        fig_country.update_layout(
            title=dict(text=f"📊 {selected_country}의 MBTI 비율 순위 (높은 순)", font=dict(size=16)),
            xaxis_title="MBTI 유형",
            yaxis_title="비율 (%)",
            yaxis=dict(ticksuffix="%"),
            margin=dict(l=20, r=20, t=60, b=20),
            height=500,
            plot_bgcolor='rgba(245, 247, 245, 1)'
        )
        st.plotly_chart(fig_country, use_container_width=True)
        st.info(f"💡 **{selected_country}**의 최다 MBTI 유형은 **{plot_df_country.loc[0, 'MBTI']}**({plot_df_country.loc[0, 'Percentage']:.2f}%) 입니다.")


    # ---------------------------------------------------------
    # TAB 2: MBTI별 국가 순위 (Top 10, 높은 순, 초록 그라데이션)
    # ---------------------------------------------------------
    with tab2:
        st.subheader("MBTI별 가장 비율이 높은 국가 Top 10")
        selected_mbti = st.selectbox("조회할 MBTI 유형을 선택하세요:", sorted(mbti_types), key="mbti_select")
        
        # 해당 MBTI 비율을 기준으로 내림차순 정렬 후 상위 10개국 추출
        top10_df = df[['Country', selected_mbti]].copy()
        top10_df[selected_mbti] = top10_df[selected_mbti] * 100  # 백분율 변환
        top10_df = top10_df.sort_values(by=selected_mbti, ascending=False).head(10).reset_index(drop=True)
        
        # 초록색 그라데이션 색상 설계 (1등 노란색, 이후 2~10등 초록색 그라데이션)
        colors_mbti = []
        n_items_mbti = len(top10_df)
        for i in range(n_items_mbti):
            if i == 0:
                colors_mbti.append('rgba(255, 215, 0, 0.95)')  # 1등: 골드/노란색
            else:
                # 10개 데이터이므로 조금 더 촘촘하게 흐려지도록 투명도 조정
                alpha = max(0.95 - (i * 0.08), 0.20)
                colors_mbti.append(f'rgba(34, 139, 34, {alpha})')
                
        # Plotly 막대그래프 생성
        fig_mbti = go.Figure(data=[go.Bar(
            x=top10_df['Country'],
            y=top10_df[selected_mbti],
            text=top10_df[selected_mbti].round(2).astype(str) + '%',
            textposition='auto',
            marker_color=colors_mbti,
            marker_line=dict(color='rgba(0,0,0,0.1)', width=1)
        )])
        
        fig_mbti.update_layout(
            title=dict(text=f"🏆 전 세계 {selected_mbti} 비율이 가장 높은 국가 TOP 10", font=dict(size=16)),
            xaxis_title="국가",
            yaxis_title="비율 (%)",
            yaxis=dict(ticksuffix="%"),
            margin=dict(l=20, r=20, t=60, b=20),
            height=500,
            plot_bgcolor='rgba(245, 247, 245, 1)'
        )
        st.plotly_chart(fig_mbti, use_container_width=True)
        st.success(f"🎉 전 세계에서 **{selected_mbti}** 비율이 가장 높은 나라는 **{top10_df.loc[0, 'Country']}**({top10_df.loc[0, selected_mbti]:.2f}%) 입니다.")

except FileNotFoundError:
    st.error("⚠️ 데이터를 찾을 수 없습니다. `countriesMBTI_16types.csv` 파일이 `app.py`와 같은 폴더에 있는지 확인해 주세요.")
