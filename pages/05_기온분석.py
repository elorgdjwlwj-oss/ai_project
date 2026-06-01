import os
import pandas as pd

# 1. 파일 경로 설정
# 현재 스크립트 위치(pages/)의 상위 폴더(..)에 있는 seoul.csv 지정
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "seoul.csv")

print(f"데이터 파일을 불러오는 중: {os.path.normpath(csv_path)}")

try:
    # 2. CSV 파일 읽기 (인코딩은 시스템 환경에 따라 cp949 또는 utf-8-sig 사용)
    df = pd.read_csv(csv_path, encoding="cp949")

    # 3. 데이터 정제 (공백 및 탭 문자 제거)
    # 열 이름의 공백 제거
    df.columns = df.columns.str.strip()

    # '날짜' 열 데이터 앞뒤의 탭(\t) 및 공백 제거
    if "날짜" in df.columns:
        df["날짜"] = df["날짜"].astype(str).str.strip()

    # 4. 데이터 기본 정보 출력
    print("\n=== 데이터 구조 요약 ===")
    print(df.info())

    print("\n=== 데이터 상위 5개 행 ===")
    print(df.head())

    # 5. 간단한 분석 예시 (역대 최고 기온과 최저 기온 찾기)
    print("\n=== 서울 기상 관측 역대 극값 ===")

    # 결측치 제거 후 계산
    df_clean = df.dropna(subset=["최고기온(℃)", "최저기온(℃)"])

    max_temp_row = df_clean.loc[df_clean["최고기온(℃)"].idxmax()]
    min_temp_row = df_clean.loc[df_clean["최저기온(℃)"].idxmin()]

    print(
        f"▶ 역대 최고 기온: {max_temp_row['최고기온(℃)']}℃ ({max_temp_row['날짜']})"
    )
    print(
        f"▶ 역대 최저 기온: {min_temp_row['최저기온(℃)']}℃ ({min_temp_row['날짜']})"
    )

except FileNotFoundError:
    print(
        f"\n[오류] 파일을 찾을 수 없습니다. 경로를 다시 확인해주세요.\n현재 예상 경로: {os.path.normpath(csv_path)}"
    )
except Exception as e:
    print(f"\n[오류] 데이터 처리 중 에러가 발생했습니다: {e}")
