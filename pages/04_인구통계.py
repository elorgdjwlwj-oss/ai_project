import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="행정구역별 인구 구조 분석",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드 함수 (캐싱을 통해 성능 최적화)
@st.cache_data
def load_data():
    # 전처리: 천 단위 콤마(,)가 포함된 숫자를 올바르게 읽기 위해 thousands=',' 설정
    df = pd.read_csv("population.csv", thousands=',')
    
    # 연령별 컬럼 정의 (0세부터 100세 이상까지 101개 컬럼)
    age_cols = [col for col in df.columns if '거주자_' in col and ('세' in col or '이상' in col)]
    
    return df, age_cols

try:
    df, age_cols = load_data()
    
    # 스트림릿 웹 화면 구성
    st.title("📊 대한민국 행정구역별 연령별 인구수 분석")
    st.markdown("`population.csv` 데이터를 기반으로 선택한 지역의 인구 분포를 무지개색 꺾은선 그래프로 시각화합니다.")
    st.hr()

    # 1. 행정구역 선택 사이드바 / 셀렉트박스
    # 행정구역 명칭 뒤의 코드 정보(예: (5000000000))를 깔끔하게 보여주기 위해 정렬
    district_list = df['행정구역'].unique()
    selected_district = st.selectbox(
        "🧐 분석할 행정구역을 선택하세요",
        options=district_list,
        index=0
    )

    # 2. 선택된 행정구역의 데이터 추출
    district_data = df[df['행정구역'] == selected_district].iloc[0]
    
    # 가로축에 들어갈 나이 리스트 생성 (0부터 100까지 정수형태)
    ages = list(range(len(age_cols)))
    # 세로축에 들어갈 인구수 리스트 생성 (데이터 타입 정수형 변환)
    populations = [int(district_data[col]) for col in age_cols]

    # 총 인구수 및 간단한 정보 요약
    total_pop_col = [c for c in df.columns if '총인구수' in c][0]
    total_population = int(district_data[total_pop_col])
    
    st.subheader(f"📍 {selected_district} 인구 현황")
    st.metric(label="거주자 총 인구수", value=f"{total_population:,} 명")

    # 3. Plotly를 활용한 무지개색 꺾은선 그래프 생성
    fig = go.Figure()

    # 무지개 색상 그라데이션 생성 (선 내부를 무지개색으로 표현하기 위해 라인 마커에 그라데이션 적용)
    # Plotly에서 완벽한 무지개 효과를 위해 선의 데이터 포인트마다 색상을 부여하는 방식 사용
    fig.add_trace(go.Scatter(
        x=ages,
        y=populations,
        mode='lines+markers',
        name='인구수',
        line=dict(
            width=3,
            color='rgba(100,100,100,0.3)' # 베이스 라인 색상 (연한 회색)
        ),
        marker=dict(
            size=6,
            color=ages, # 나이(0~100)를 기준으로 색상 매핑
            colorscale='Rainbow', # 무지개(Rainbow) 색상축 적용
            showscale=True,
            colorbar=dict(
                title="연령대",
                titleside="top",
                tickmode="array",
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=["0세", "20세", "40세", "60세", "80세", "100세 이상"]
            )
        ),
        # 마우스 오버 시 나타날 툴팁 포맷 (한글 깨짐 없음)
        hovertemplate="<b>나이:</b> %{x}세<br><b>인구수:</b> %{y:,}명<extra></extra>"
    ))

    # 4. 레이아웃 및 10살 단위 구분선(그리드) 설정
    fig.update_layout(
        title=dict(
            text=f"<b>[{selected_district}] 연령별 인구수 추이 (꺾은선)</b>",
            font=dict(size=18)
        ),
        xaxis=dict(
            title="나이 (세)",
            tickmode='linear',
            tick0=0,
            dtick=10, # ⭐ 가로축 10살 단위 설정
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.5)', # 주 그리드 선 (10살 단위)
            minor=dict(
                dtick=1, # 1살 단위 보조선은 연하게 설정
                showgrid=True,
                gridcolor='rgba(240, 240, 240, 0.3)'
            )
        ),
        yaxis=dict(
            title="인구수 (명)",
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.5)'
        ),
        template="plotly_white",
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # 스트림릿 화면에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `population.csv` 파일을 찾을 수 없습니다. GitHub 저장소에 데이터 파일이 올바르게 업로드되었는지 확인해주세요.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")
