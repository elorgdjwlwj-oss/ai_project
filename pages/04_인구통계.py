# Streamlit 제주 인구 연령 그래프 앱

## 파일 구성

아래 두 개 파일을 같은 폴더에 저장한 뒤 Streamlit Cloud에 업로드하세요.

---

# 1. app.py

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# -----------------------------
# 한글 폰트 설정
# -----------------------------
# Streamlit Cloud에서도 최대한 안정적으로 한글 표시
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title='제주 인구 연령 분석',
    layout='wide'
)

st.title('📊 제주 연령별 인구 분석')

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('population.csv', encoding='utf-8')
    return df


df = load_data()

# -----------------------------
# 컬럼 확인
# -----------------------------
# 숫자 나이 컬럼만 추출
age_columns = []

for col in df.columns:
    try:
        age = int(str(col).replace('세', '').replace(' ', ''))
        age_columns.append(col)
    except:
        pass

# 정렬
age_columns = sorted(
    age_columns,
    key=lambda x: int(str(x).replace('세', '').replace(' ', ''))
)

# -----------------------------
# 행정구 선택
# -----------------------------
region_col = df.columns[0]
regions = df[region_col].tolist()

selected_region = st.selectbox(
    '행정구를 선택하세요',
    regions
)

# -----------------------------
# 선택 지역 데이터 추출
# -----------------------------
row = df[df[region_col] == selected_region].iloc[0]

ages = []
populations = []

for col in age_columns:
    age_num = int(str(col).replace('세', '').replace(' ', ''))

    value = row[col]

    try:
        value = int(str(value).replace(',', ''))
    except:
        value = 0

    ages.append(age_num)
    populations.append(value)

# -----------------------------
# 그래프 생성
# -----------------------------
fig, ax = plt.subplots(figsize=(16, 7))

# 무지개 색상 생성
colors = plt.cm.rainbow(np.linspace(0, 1, len(ages)))

# 선 그래프
for i in range(len(ages) - 1):
    ax.plot(
        ages[i:i+2],
        populations[i:i+2],
        color=colors[i],
        linewidth=2.5
    )

# 점 표시
ax.scatter(
    ages,
    populations,
    c=colors,
    s=40
)

# 제목 및 축
ax.set_title(
    f'{selected_region} 연령별 인구 분포',
    fontsize=20,
    fontweight='bold'
)

ax.set_xlabel('나이', fontsize=14)
ax.set_ylabel('인구수', fontsize=14)

# -----------------------------
# 가로축 10살 단위 구분선
# -----------------------------
ax.set_xticks(range(0, max(ages)+1, 10))
ax.grid(axis='x', linestyle='--', alpha=0.6)

# 세로축 격자
ax.grid(axis='y', linestyle=':', alpha=0.3)

# 여백
plt.tight_layout()

# 출력
st.pyplot(fig)

# -----------------------------
# 데이터 테이블
# -----------------------------
st.subheader('연령별 데이터')

chart_df = pd.DataFrame({
    '나이': ages,
    '인구수': populations
})

st.dataframe(chart_df, use_container_width=True)
```

---

# 2. requirements.txt

```txt
streamlit
pandas
numpy
matplotlib
```

---

# Streamlit Cloud 배포 방법

## 1단계

GitHub 저장소 생성

## 2단계

아래 파일 업로드

* app.py
* requirements.txt
* population.csv

## 3단계

Streamlit Cloud 접속

[https://streamlit.io/cloud](https://streamlit.io/cloud)

## 4단계

GitHub 저장소 연결 후 Deploy 클릭

---

# 기능

✅ 행정구 선택

✅ 연령별 꺾은선 그래프

✅ 무지개 색상 적용

✅ 10살 단위 가로축 구분선

✅ Streamlit Cloud 한글 깨짐 방지

✅ 연령별 데이터 테이블 제공
