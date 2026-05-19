import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 Top 10 외국인 인기 관광지",
    page_icon="🗺️",
    layout="wide"
# 데이터 준비 (서울 주요 관광지 Top 10)
tourist_spots = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "desc": "한국의 대표적인 조선시대 법궁, 한복 체험 명소"},
    {"name": "N서울타워", "lat": 37.5512, "lon": 126.9882, "desc": "남산 정상에서 서울 시내를 한눈에 내려다보는 전망대"},
    {"name": "명동 쇼핑거리", "lat": 37.5635, "lon": 126.9850, "desc": "K-뷰티, 길거리 음식, 쇼핑의 중심지"},
    {"name": "북촌한옥마을", "lat": 37.5829, "lon": 126.9835, "desc": "도심 속 실제 주민들이 거주하는 전통 한옥 보존 지역"},
    {"name": "인사동", "lat": 37.5744, "lon": 126.9848, "desc": "한국 전통 공예품, 갤러리, 전통 찻집이 모인 거리"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.5665, "lon": 127.0092, "desc": "자하 하디드가 설계한 세계 최대 규모의 3차원 비정형 건축물"},
    {"name": "홍대거리", "lat": 37.5568, "lon": 126.9239, "desc": "젊은 예술가들의 버스킹, 클럽, 트렌디한 패션의 메카"},
    {"name": "롯데월드타워 & 몰", "lat": 37.5126, "lon": 127.1025, "desc": "세계 5위 높이의 초고층 빌딩과 대형 복합 쇼핑몰"},
    {"name": "이태원 관광특구", "lat": 37.5345, "lon": 126.9943, "desc": "다양한 문화와 이국적인 세계 요리를 즐길 수 있는 곳"},
    {"name": "광장시장", "lat": 37.5701, "lon": 127.0010, "desc": "빈대떡, 육회, 마약김밥 등 한국 시장 음식을 맛보는 필수 코스"}
]

# 2. 타이틀 및 설명
st.title("🗺️ 외국인이 사랑하는 서울 명소 TOP 10")
st.markdown("스트림릿과 폴리움(Folium)을 활용한 서울의 주요 관광지 지도입니다. 마커를 클릭해 정보를 확인해보세요.")

# 3. 화면 레이아웃 분할 (지도 | 상세 정보)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 서울 관광 지도")
    
    # 서울 중심부 좌표로 지도 초기화
    m = folium.Map(location=[37.555, 126.985], zoom_start=12)
    
    # 마커 추가
    for spot in tourist_spots:
        popup_html = f"""
        <div style='width:200px;'>
            <h4><b>{spot['name']}</b></h4>
            <p style='font-size:12px; color:gray;'>{spot['desc']}</p>
        </div>
        """
        folium.Marker(
            location=[spot["lat"], spot["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=spot["name"],
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    
    # 스트림릿에 지도 렌더링 (지도를 움직이거나 클릭해도 반응하도록 반응형 크기 설정)
    st_data = st_folium(m, width="100%", height=500)

with col2:
    st.subheader("ℹ️ 명소 리스트 및 설명")
    
    # 사이드 리스트 형태로 깔끔하게 표시
    for idx, spot in enumerate(tourist_spots, 1):
        with st.expander(f"{idx}. {spot['name']}"):
            st.write(spot['desc'])
            st.caption(f"위도: {spot['lat']}, 경도: {spot['lon']}")

# 4. 푸터
st.markdown("---")
st.caption("Data source: 한국관광공사 및 외래관광객 조사 기반 트렌드 재구성")
