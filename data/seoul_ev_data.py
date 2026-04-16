"""
서울특별시 시군구별 전기자동차 및 충전소 실제 데이터 연동 모듈
"""
import streamlit as st
import pandas as pd
import numpy as np
import glob
import os
from collections import Counter
from kiwipiepy import Kiwi

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

    # 친환경 데이터만 필터링
    df_ev = df[df['fuel_name'].str.contains('전기', na=False)].copy()

    # [핵심 수정] 구별, 년도별, 연료명별로 합계 산출
    grouped = df_ev.groupby(['district_name', 'reg_year', 'fuel_name'])['total_amount'].sum().reset_index()
    grouped.rename(columns={'district_name': '시군구명', 'reg_year': '기준년도', 'fuel_name': '연료명', 'total_amount': '등록대수'}, inplace=True)

    # 년도 뒤에 '년' 글자 붙이기
    grouped['기준년도'] = grouped['기준년도'].astype(str) + "년"

    # 좌표 매핑
    grouped['위도'] = grouped['시군구명'].map(lambda x: DISTRICT_COORDS.get(x, (37.5665, 126.9780))[0])
    grouped['경도'] = grouped['시군구명'].map(lambda x: DISTRICT_COORDS.get(x, (37.5665, 126.9780))[1])

    return grouped


def get_charging_station_data(csv_path="data/data_set_ev_charging_stations_new.csv"):
    df = pd.read_csv(csv_path)

    df = df[
        [
            "station_id",
            "station_name",
            "address",
            "lat",
            "lon",
            "fast_charger",
            "slow_charger",
            "district_code",
        ]
    ]

    return df

def get_load_faq_data():
    """FAQ 데이터 로드 - data_set_faq.csv 단일 파일"""
    try:
        df = pd.read_csv(get_data_path("data_set_faq.csv"))
    except Exception as e:
        st.warning(f"FAQ 데이터를 불러오지 못했습니다: {e}")
        return []

    faqs = []
    for _, row in df.iterrows():
        faqs.append({
            "faq_id": row.get("faq_id", ""),
            "question": row.get("questions", ""),
            "answer": row.get("answers", ""),
        })
    return faqs
    
# faq keywords 뽑기 위한 함수

@st.cache_data
def top_rate(csv_path):
    '''
    csv 파일을 받아 questions 컬럼에 있는 값들 중 단어를 추출해 빈도를 묶어 반환해주는 함수입니다.
    '''
    df = pd.read_csv(csv_path)

    questions = df['questions'].dropna()

    kiwi = Kiwi()
    words = []

    for q in questions:
        tokens = kiwi.tokenize(q)

        # 명사만 추출 (NNG: 일반명사, NNP: 고유명사)
        nouns = [t.form for t in tokens if t.tag in ['NNG', 'NNP']]

        words.extend(nouns)

    stopwords = {'경우', '관련', '문의', '확인', '사용', '방법', '서울시', '가능', '얼마나', '이후', '하나요'}

    # 한 글자 제거 + stopwords 제거
    words = [w for w in words if len(w) > 1 and w not in stopwords]

    count_words = Counter(words)
    return count_words

# ── 하단의 차트를 위한 헬퍼 함수 ──────────────────────────────
def get_ev_trend_data():
    """년도별 전기차 추이 (라인차트용)"""
    df_year = pd.read_csv(get_data_path("year_amount.csv"))
    df_fuel = pd.read_csv(get_data_path("data_set_fuel_types.csv"))
    df = df_year.merge(df_fuel, on="fuel_id", how="left")
    
    df_ev = df[df['fuel_name'].str.contains('전기', na=False)]
    trend = df_ev.groupby('reg_year')['total_amount'].sum().reset_index()
    trend.rename(columns={'reg_year': '기준년도', 'total_amount': '등록대수'}, inplace=True)
    return trend

def get_ev_fuel_data():
    """연료별 등록 비중 (도넛차트용)"""
    #df_year = pd.read_csv(get_data_path("year_amount.csv"))
    #df_fuel = pd.read_csv(get_data_path("data_set_fuel_types.csv"))
    #df = df_year.merge(df_fuel, on="fuel_id", how="left")
    
    #fuel = df.groupby('fuel_name')['total_amount'].sum().reset_index()
    #fuel.rename(columns={'fuel_name': '연료', 'total_amount': '수량'}, inplace=True)
    #return fuel
    fuel_data = pd.read_csv(get_data_path("year_amount.csv"))

    df_2026 = fuel_data[fuel_data['reg_year'] == 2026]

    fuel_select = {1: "휘발유", 2: "경유", 3: "LPG", 4: "CNG",5: "하이브리드", 6: "전기", 7: "수소"}
    df_2026['연료'] = df_2026['fuel_id'].map(fuel_select)
    fuel_data = df_2026.groupby("연료")["total_amount"].sum().reset_index()

    fuel_data.columns = ["연료", "수량"]

    return fuel_data

