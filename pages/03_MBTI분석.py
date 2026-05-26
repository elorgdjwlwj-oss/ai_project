import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="국가별 MBTI 분포 분석기", layout="centered")
st.title("🌍 국가별 MBTI 비율 시각화 대시보드")
st.write("국가를 선택하면 해당 국가의 16가지 MBTI 성격 유형 비율을 분석하여 보여줍니다.")

# 2. 데이터 불러오기 (캐싱 처리로 속도 최적화)
@st.cache_data
def load_data():
    # 동일 디렉토리에 countriesMBTI_16types.csv 파일이 있다고 가정합니다.
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
    
    # 3. 사이드바 또는 메인 화면에 국가 선택 셀렉트박스 배치
    country_list = sorted(df['Country'].unique())
    selected_country = st.selectbox("분석할 국가를 선택하세요:", country_list)
    
    # 4. 선택된 국가의 데이터 추출 및 가공
    country_data = df[df['Country'] == selected_country].iloc[0]
    
    # 'Country' 열을 제외한 MBTI 유형과 비율만 추출
    mbti_types = df.columns[1:]  # INFJ, ISFJ ...
    percentages = [country_data[mbti] * 100 for mbti in mbti_types] # 백분율(%)로 변환
    
    # 데이터프레임으로 변환 후 비율이 높은 순으로 정렬
    plot_df = pd.DataFrame({
        'MBTI': mbti_types,
        'Percentage': percentages
    }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)
    
    # 5. 색상 규칙 정의 (1등은 노란색, 나머지는 하늘색에서 흐려지는 그라데이션)
    # 데이터 개수(16개)만큼 하늘색 색상 강도를 다르게 조절 (rgba 활용)
    colors = []
    n_items = len(plot_df)
    
    for i in range(n_items):
        if i == 0:
            # 1등: 진한 노란색 (Gold / Yellow)
            colors.append('rgba(255, 215, 0, 0.95)')
        else:
            # 나머지: 순위에 따라 하늘색(DeepSkyBlue)의 투명도(Alpha)를 낮춰 흐려지게 설정
            # 2등(i=1)일 때 가장 진하고, 순위가 내려갈수록 흐려짐
            alpha = max(0.95 - (i * 0.05), 0.15) 
            colors.append(f'rgba(0, 191, 255, {alpha})')
            
    # 6. Plotly를 활용한 인터랙티브 막대그래프 생성
    fig = go.Figure(data=[go.Bar(
        x=plot_df['MBTI'],
        y=plot_df['Percentage'],
        text=plot_df['Percentage'].round(2).astype(str) + '%',
        textposition='auto',
        marker_color=colors,
        marker_line=dict(color='rgba(0,0,0,0.1)', width=1)
    )])
    
    # 그래프 레이아웃 설정
    fig.update_layout(
        title=dict(text=f"📊 {selected_country}의 MBTI 유형별 비율 순위", font=dict(size=18)),
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%"),
        margin=dict(l=20, r=20, t=60, b=20),
        height=500,
        plot_bgcolor='rgba(248, 249, 250, 1)' # 깔끔한 연회색 배경
    )
    
    # 7. 스트림릿 화면에 그래프 및 정보 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 간단한 요약 정보 창
    st.info(f"💡 **{selected_country}**에서 가장 많은 성격 유형은 **{plot_df.loc[0, 'MBTI']}**({plot_df.loc[0, 'Percentage']:.2f}%) 입니다.")

except FileNotFoundError:
    st.error("⚠️ 데이터를 찾을 수 없습니다. `countriesMBTI_16types.csv` 파일이 `app.py`와 같은 폴더에 있는지 확인해 주세요.")
