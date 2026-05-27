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

# -----------------------------
# 한글 설정
# -----------------------------
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
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv('population.csv')


df = load_data()

# -----------------------------
# 첫 번째 컬럼 = 지역명
# -----------------------------
region_col = df.columns[0]

# -----------------------------
# 나이 컬럼 찾기
# -----------------------------
age_columns = []

for col in df.columns:
    col_str = str(col)

    if '세' in col_str:
        try:
            age_num = int(col_str.replace('세', '').strip())
            age_columns.append((age_num, col))
        except:
            pass

# 나이순 정렬
age_columns = sorted(age_columns, key=lambda x: x[0])

# -----------------------------
# 행정구 선택
# -----------------------------
regions = df[region_col].tolist()

selected_region = st.selectbox(
    '행정구를 선택하세요',
    regions
)

# -----------------------------
# 선택 지역 데이터
# -----------------------------
selected_row = df[df[region_col] == selected_region].iloc[0]

ages = []
populations = []

for age_num, col_name in age_columns:
    value = selected_row[col_name]

    try:
        value = int(str(value).replace(',', ''))
    except:
        value = 0

    ages.append(age_num)
    populations.append(value)

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(16, 7))

# 무지개 색상
colors = plt.cm.rainbow(np.linspace(0, 1, len(ages)))

# 구간별 색상 적용
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
    s=35
)

# 제목
ax.set_title(
    f'{selected_region} 연령별 인구수',
    fontsize=20,
    fontweight='bold'
)

# 축 라벨
ax.set_xlabel('나이', fontsize=14)
ax.set_ylabel('인구수', fontsize=14)

# -----------------------------
# 10살 단위 구분선
# -----------------------------
ax.set_xticks(range(0, max(ages) + 1, 10))
ax.grid(axis='x', linestyle='--', alpha=0.6)
ax.grid(axis='y', linestyle=':', alpha=0.3)

# 여백
plt.tight_layout()

# 출력
st.pyplot(fig)

# -----------------------------
# 데이터 테이블
# -----------------------------
st.subheader('연령별 데이터')

result_df = pd.DataFrame({
    '나이': ages,
    '인구수': populations
})

st.dataframe(result_df, use_container_width=True)
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
