"""
서울특별시 시군구별 전기자동차 및 충전소 실제 데이터 연동 모듈
"""
import pandas as pd
import numpy as np
import glob
import os

# 서울 25개 자치구 중심 좌표 (충전소 및 지도 마커 기준점 제공용)
DISTRICT_COORDS = {
    "종로구": (37.5730, 126.9794), "중구": (37.5640, 126.9975), "용산구": (37.5384, 126.9654),
    "성동구": (37.5635, 127.0369), "광진구": (37.5384, 127.0823), "동대문구": (37.5744, 127.0396),
    "중랑구": (37.6063, 127.0927), "성북구": (37.5894, 127.0167), "강북구": (37.6396, 127.0256),
    "도봉구": (37.6688, 127.0471), "노원구": (37.6542, 127.0568), "은평구": (37.6027, 126.9291),
    "서대문구": (37.5791, 126.9368), "마포구": (37.5663, 126.9014), "양천구": (37.5170, 126.8664),
    "강서구": (37.5509, 126.8495), "구로구": (37.4955, 126.8875), "금천구": (37.4600, 126.9001),
    "영등포구": (37.5264, 126.8963), "동작구": (37.5124, 126.9393), "관악구": (37.4784, 126.9516),
    "서초구": (37.4837, 127.0324), "강남구": (37.5172, 127.0473), "송파구": (37.5145, 127.1059),
    "강동구": (37.5301, 127.1238),
}

def get_data_path(filename):
    """실행 위치에 상관없이 data 폴더의 파일을 찾기 위한 헬퍼 함수"""
    return os.path.join("data", filename)

def get_ev_data():
    """1. 등록 현황 데이터 병합 및 가공"""
    df_year = pd.read_csv(get_data_path("year_amount.csv"))
    df_dist = pd.read_csv(get_data_path("data_set_seoul_districts.csv"))
    df_fuel = pd.read_csv(get_data_path("data_set_fuel_types.csv"))

    # 테이블 병합 (JOIN)
    df = df_year.merge(df_dist, on="district_code", how="left")
    df = df.merge(df_fuel, on="fuel_id", how="left")

    # 전기차(친환경) 데이터만 필터링
    df_ev = df[df['fuel_name'].str.contains('전기', na=False)].copy()

    # 원본 데이터에 '차량종류(승용/화물)'가 없으므로 UI 필터 호환을 위해 등록년도(reg_year)를 차량종류 컬럼에 매핑 
    # (이렇게 하면 앱에서 승용/화물 대신 "2023년", "2024년" 등으로 필터링 가능해집니다)
    df_ev['차량종류'] = df_ev['reg_year'].astype(str) + "년 등록"

    # 구별, 년도별 합계 산출
    grouped = df_ev.groupby(['district_name', '차량종류'])['total_amount'].sum().reset_index()
    grouped.rename(columns={'district_name': '시군구명', 'total_amount': '등록대수'}, inplace=True)

    # 좌표 매핑
    grouped['위도'] = grouped['시군구명'].map(lambda x: DISTRICT_COORDS.get(x, (37.5665, 126.9780))[0])
    grouped['경도'] = grouped['시군구명'].map(lambda x: DISTRICT_COORDS.get(x, (37.5665, 126.9780))[1])

    return grouped

def get_charging_station_data():
    """2. 충전소 데이터 병합 및 가공"""
    df_stat = pd.read_csv(get_data_path("data_set_ev_charging_stations.csv"))
    df_dist = pd.read_csv(get_data_path("data_set_seoul_districts.csv"))

    # 테이블 병합
    df = df_stat.merge(df_dist, on="district_code", how="left")

    # 급속/완속 여부 결정 로직 (급속 충전기가 1개라도 있으면 '급속'으로 분류)
    df['충전기종류'] = df.apply(lambda row: "급속" if row['fast_charger'] > 0 else "완속", axis=1)

    # UI 컬럼명에 맞게 변경
    df.rename(columns={
        'district_name': '시군구명',
        'station_name': '설치장소명',
        'address': '주소'
    }, inplace=True)

    df['운영시간'] = "정보 없음" # CSV에 운영시간이 없으므로 기본값 처리

    # 충전소 데이터에 위도/경도가 없으므로, 자치구 중심 좌표를 기준으로 약간씩 분산(Scatter)시킴
    np.random.seed(42)
    lat_list, lon_list = [], []
    for dist in df['시군구명']:
        base_lat, base_lon = DISTRICT_COORDS.get(dist, (37.5665, 126.9780))
        lat_list.append(base_lat + np.random.uniform(-0.025, 0.025))
        lon_list.append(base_lon + np.random.uniform(-0.025, 0.025))
    
    df['위도'] = lat_list
    df['경도'] = lon_list

    return df

def get_load_faq_data():
    """3. FAQ 데이터 로드"""
    file_list = glob.glob(get_data_path("data_faq/*.csv"))
    df_list = []
    
    for file in file_list:
        # FAQ 관련 파일만 로드 (가정: 파일명에 faq가 포함되거나, 컬럼에 question이 있는 경우)
        if "faq" not in file.lower() and "질문" not in file:
            continue
            
        try:
            df = pd.read_csv(file)
            if "question" in df.columns:
                df["category"] = "충전소" if "charge" in file.lower() else "전기차"
                df_list.append(df)
        except Exception:
            pass

    if not df_list:
        return []

    df_faq = pd.concat(df_list, ignore_index=True).fillna("")
    faqs = []
    for _, row in df_faq.iterrows():
        faqs.append({
            "category": row.get("category", "전기차"),
            "question": row.get("question", ""),
            "answer": row.get("answer", ""),
            "tags": []
        })
    return faqs


# ── 하단의 차트를 위한 헬퍼 함수 ──────────────────────────────
def get_ev_trend_data():
    """년도별 전기차 추이 (app.py 라인차트용)"""
    df_year = pd.read_csv(get_data_path("year_amount.csv"))
    df_fuel = pd.read_csv(get_data_path("data_set_fuel_types.csv"))
    df = df_year.merge(df_fuel, on="fuel_id", how="left")
    
    df_ev = df[df['fuel_name'].str.contains('전기', na=False) | (df['is_eco'].isin([1, '1', True, 'True']))]
    trend = df_ev.groupby('reg_year')['total_amount'].sum().reset_index()
    trend.rename(columns={'reg_year': '기준년도', 'total_amount': '등록대수'}, inplace=True)
    return trend

def get_ev_fuel_data():
    """연료별 등록 비중 (app.py 도넛차트용)"""
    #df_year = pd.read_csv(get_data_path("year_amount.csv"))
    #df_fuel = pd.read_csv(get_data_path("data_set_fuel_types.csv"))
    #df = df_year.merge(df_fuel, on="fuel_id", how="left")
    
    #fuel = df.groupby('fuel_name')['total_amount'].sum().reset_index()
    #fuel.rename(columns={'fuel_name': '연료', 'total_amount': '수량'}, inplace=True)
    #return fuel
    fuel_data = pd.read_csv("data\year_amount.csv")

    df_2026 = fuel_data[fuel_data['reg_year'] == 2026]

    fuel_select = {1: "휘발유", 2: "경유", 3: "LPG", 4: "CNG",5: "하이브리드", 6: "전기", 7: "수소"}
    df_2026['연료'] = df_2026['fuel_id'].map(fuel_select)
    fuel_data = df_2026.groupby("연료")["total_amount"].sum().reset_index()

    fuel_data.columns = ["연료", "수량"]

    return fuel_data

