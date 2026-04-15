import sys
import streamlit as st
import pandas as pd
import plotly.express as px

import folium
from folium import DivIcon
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울특별시 전기자동차 현황",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

:root {
    --bg: #f8fafc;
    --surface: #ffffff;
    --surface2: #f1f5f9;
    --accent: #2563eb;
    --accent-hover: #1d4ed8;
    --green: #10b981;
    --yellow: #f59e0b;
    --text: #1e293b;
    --muted: #64748b;
    --border: #e2e8f0;
    --shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}
.stApp { background: var(--bg); }

/* [수정 3] 최대 폭 제한으로 가로 피로감 완화 */
.block-container {
    padding: 0 !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}
            

.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
}
.kpi-label { font-size: 11px; font-weight: 600; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-value { font-size: 26px; font-weight: 800; font-family: 'Space Grotesk'; color: var(--accent); }
.kpi-sub   { font-size: 12px; color: var(--muted); margin-top: 4px; font-weight: 500; }

.section-title {
    font-size: 14px; font-weight: 700; color: var(--text);
    margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
}

/* [수정 3] 패딩 축소 */
.page-content { padding: 24px 28px; }

.stButton button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    font-weight: 600; border-radius: 8px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.stButton button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
.stButton button p { margin: 0; }

[data-baseweb="tab-list"] { background: var(--surface2) !important; border-radius: 10px !important; gap: 4px; padding: 4px; }
[data-baseweb="tab"] { background: transparent !important; border-radius: 8px !important; color: var(--muted) !important; font-weight: 600; }
[aria-selected="true"] { background: var(--surface) !important; color: var(--accent) !important; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }

.faq-tag { display: inline-block; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; margin-right: 6px; margin-top: 12px; }
.tag-ev     { background: #ecfdf5; color: var(--green); border: 1px solid #a7f3d0; }
.tag-charge { background: #fffbeb; color: var(--yellow); border: 1px solid #fde68a; }
/* 멀티셀렉트 선택된 태그(칩) 모던하게 변경 */
[data-baseweb="tag"] {
    background-color: #eff6ff !important; /* 연한 블루 배경 */
    border: 1px solid #bfdbfe !important; /* 부드러운 테두리 */
    border-radius: 20px !important; /* 알약 모양으로 완전 둥글게 */
    padding: 2px 8px !important;
    margin-right: 4px !important;
}

/* 태그 안쪽 텍스트 스타일 */    /* 윤태선 수정 */
[data-baseweb="tag"] span {
    color: #1d4ed8 !important; /* 진하고 신뢰감 있는 블루 텍스트 */
    font-weight: 600 !important;
    font-size: 16px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 태그 지우기 'X' 버튼 스타일 */
[data-baseweb="tag"] svg {
    color: #60a5fa !important; /* 아이콘 기본 색상 */
    transition: color 0.2s;
}

/* 'X' 버튼에 마우스 올렸을 때 */
[data-baseweb="tag"] svg:hover {
    color: #1e3a8a !important; /* 더 진한 파란색으로 변경 */
}
</style>
""", unsafe_allow_html=True)



if "page" not in st.session_state:
    st.session_state.page = "🏠 EV Seoul 소개 (INFO)"

with st.sidebar:
    # 사이드바 상단 로고 및 타이틀
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 900; background: linear-gradient(90deg, #10b981 0%, #00e5ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            EV Seoul
        </div>
        <div style="color: #64748b; font-size: 12px; margin-top: 4px;">Navigation Menu</div>
    </div>
    """, unsafe_allow_html=True)
    
    pages = ["🏠 EV Seoul 소개 (INFO)", "📊 현황 대시보드", "📍 충전소 맵", "💬 FAQ"]
    
    # 2. key="page"를 넣으면 st.session_state.page 와 자동으로 동기화됩니다.
    # 복잡한 if문이나 st.rerun()이 전혀 필요 없습니다!
    selected_page = st.selectbox(
        "이동할 페이지를 선택하세요",
        options=pages,
        key="page"
    )

st.markdown("---")

import sys

from data.seoul_ev_data import (
    get_ev_data, get_charging_station_data, get_load_faq_data, 
    get_ev_trend_data, get_ev_fuel_data, top_rate  # 추가됨
)

@st.cache_data
def load_data():
    return get_ev_data()

@st.cache_data
def load_charging():
    return get_charging_station_data()
@st.cache_data
def load_faq_data():
    return get_load_faq_data()

df        = load_data()
df_charge = load_charging()
district_df = pd.read_csv("data/data_set_seoul_districts.csv")
# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 : INFO (메인 소개 화면)
# ─────────────────────────────────────────────────────────────────────────────
if selected_page == "🏠 EV Seoul 소개 (INFO)":
    
   # 1. INFO 페이지 전용 추가 CSS
    st.markdown("""
    <style>
    .hero-container { text-align: center; padding: 60px 20px 40px 20px; }
    .hero-badge { display: inline-block; padding: 6px 16px; background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 100px; color: #00e5ff; font-size: 13px; font-weight: 700; margin-bottom: 24px; letter-spacing: 1px; }
    .hero-title { font-family: 'Space Grotesk', sans-serif; font-size: 3.5rem; font-weight: 900; margin-bottom: 20px; line-height: 1.2; color: var(--text); }
    .hero-title span { background: linear-gradient(90deg, #10b981 0%, #00e5ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    /* 서브타이틀 가독성 & 중앙정렬 완벽 개선 */
    .hero-subtitle { 
        font-size: 1.15rem; 
        color: #475569; /* 기존보다 약간 더 또렷한 색상 */
        font-weight: 500; 
        max-width: 650px; 
        margin: 0 auto; 
        line-height: 1.7; 
        text-align: center; /* 확실한 중앙 정렬 */
        word-break: keep-all; /* 단어가 중간에 잘리지 않고 깔끔하게 줄바꿈됨 */
    }
    
    /* 퀵 스탯 배너 */
    .quick-stats-container { display: flex; justify-content: center; gap: 40px; margin-bottom: 60px; }
    .quick-stat-item { text-align: center; }
    .quick-stat-num { font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; font-weight: 900; color: #2563eb; }
    .quick-stat-label { font-size: 14px; font-weight: 600; color: var(--muted); }

    /* 기능 카드 */
    .feature-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 32px 24px; text-align: center; transition: all 0.3s ease; height: 100%; display: flex; flex-direction: column; align-items: center; box-shadow: var(--shadow); margin-bottom: 15px; }
    .feature-card:hover { transform: translateY(-5px); border-color: #3b82f6; box-shadow: 0 10px 20px rgba(37, 99, 235, 0.1); }
    .feature-icon { font-size: 40px; margin-bottom: 16px; background: #f1f5f9; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
    .feature-title { font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 12px; }
    .feature-desc { font-size: 14px; color: var(--muted); line-height: 1.6; word-break: keep-all; flex-grow: 1; }
    
    /* 기능 이동 버튼 커스텀 */
    div.stButton > button.nav-btn { background: #eff6ff !important; color: #2563eb !important; border: 1px solid #bfdbfe !important; width: 100%; height: 45px; border-radius: 12px !important; font-size: 15px; transition: all 0.2s; }
    div.stButton > button.nav-btn:hover { background: #2563eb !important; color: #ffffff !important; border-color: #2563eb !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    
    # 2. 히어로 섹션
    # 2. 히어로 섹션 (타이틀과 서브타이틀 완벽 분리 및 중앙 고정)
    
    # 2-1. 뱃지 및 메인 타이틀
    st.markdown("""
    <div style="width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 60px; padding-bottom: 15px;">
        <div style="padding: 6px 16px; background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 100px; color: #00e5ff; font-size: 13px; font-weight: 700; margin-bottom: 24px; letter-spacing: 1px;">
            SMART MOBILITY CITY
        </div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 3.5rem; font-weight: 900; margin: 0; line-height: 1.2; color: var(--text); text-align: center;">
            <span style="background: linear-gradient(90deg, #10b981 0%, #00e5ff 100%); -webkit-background-clip: text;
                 -webkit-text-fill-color: transparent;">미래를 향한 푸른 발걸음<br>
                EV Seoul과 함께</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # 2-2. 서브타이틀 (분리하여 강제 중앙 정렬 적용)
    st.markdown("""
    <div style="width: 100%; display: flex; justify-content: center; margin-bottom: 40px;">
        <div style="text-align: center; font-size: 1.15rem; color: #475569; font-weight: 500; line-height: 1.7; word-break: keep-all;">
            서울특별시의 전기차 보급 현황과 충전소 인프라를 한눈에 파악하세요.<br>
            시민들을 위한 편리하고 스마트한 데이터 통합 플랫폼입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. [신규] 라이브 퀵 스탯 (데이터에서 실시간 추출)
    # 가장 최신 년도의 전기차 등록 대수 합계 구하기
    latest_year = sorted(df["기준년도"].unique())[-1]
    total_evs = int(df[df["기준년도"] == latest_year]["등록대수"].sum())
    total_stations = len(df_charge)

    st.markdown(f"""
    <div class="quick-stats-container">
        <div class="quick-stat-item">
            <div class="quick-stat-num">{total_evs:,}<span style="font-size:1.2rem;color:#94a3b8;">대</span></div>
            <div class="quick-stat-label">서울시 누적 전기차 ({latest_year} 기준)</div>
        </div>
        <div style="width: 1px; background-color: var(--border); height: 60px; margin-top: 10px;"></div>
        <div class="quick-stat-item">
            <div class="quick-stat-num">{total_stations:,}<span style="font-size:1.2rem;color:#94a3b8;">개소</span></div>
            <div class="quick-stat-label">서울시 전체 전기차 충전소</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # [추가] 페이지 이동을 위한 콜백 함수 정의
    def change_page(page_name):
        st.session_state.page = page_name

    # 4. 기능 카드 섹션 (HTML 레이아웃 + 콜백이 적용된 Streamlit 버튼)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">현황 대시보드</div>
            <div class="feature-desc">
                서울시 25개 자치구별 전기자동차 등록 현황 및 연도별 추이를 직관적인 데이터 시각화로 분석합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        # on_click과 args를 사용하여 위젯 렌더링 전에 상태를 변경합니다 (에러 해결 핵심!)
        st.button("현황 분석하기 ➔", key="nav_dash", type="primary", use_container_width=True, on_click=change_page, args=("📊 현황 대시보드",))

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📍</div>
            <div class="feature-title">스마트 충전소 맵</div>
            <div class="feature-desc">
                현재 위치 주변이나 원하는 자치구의 충전소를 빠르게 찾고, 급속/완속 여부 등 상세 정보를 확인하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("충전소 찾기 ➔", key="nav_map", type="primary", use_container_width=True, on_click=change_page, args=("📍 충전소 맵",))

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">자주 묻는 질문 (FAQ)</div>
            <div class="feature-desc">
                전기차 보조금, 혜택, 충전기 이용 방법 등 시민들이 가장 궁금해하는 핵심 정보들을 키워드로 검색해 보세요.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("FAQ 바로가기 ➔", key="nav_faq", type="primary", use_container_width=True, on_click=change_page, args=("💬 FAQ",))

    # 5. [신규] 안내 섹션 (Why EV Seoul?)
    st.markdown("""
    <div style="margin-top: 80px; padding: 40px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 20px;">
        <h3 style="font-family: 'Space Grotesk', sans-serif; color: #1e293b; margin-bottom: 20px; text-align: center;">💡 Why EV Seoul?</h3>
        <div style="display: flex; gap: 30px; justify-content: space-around; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 10px;">📈</div>
                <h4 style="font-size: 16px; color: #334155;">데이터 기반의 인사이트</h4>
                <p style="font-size: 13px; color: #64748b; line-height: 1.6;">국토교통부와 환경부의 검증된 공공데이터를 기반으로 정확한 서울시 모빌리티 현황을 파악합니다.</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 10px;">⚡</div>
                <h4 style="font-size: 16px; color: #334155;">충전 사각지대 해소</h4>
                <p style="font-size: 13px; color: #64748b; line-height: 1.6;">누구나 쉽게 거주지 주변의 충전 인프라를 확인하여 전기차 진입 장벽을 낮춥니다.</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 10px;">🌱</div>
                <h4 style="font-size: 16px; color: #334155;">친환경 도시 실현</h4>
                <p style="font-size: 13px; color: #64748b; line-height: 1.6;">지속 가능한 미래를 위해 내연기관차에서 친환경차로의 전환을 독려하고 정보를 제공합니다.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 : 현황
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 : 현황 대시보드
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "📊 현황 대시보드":
    import folium
    from folium import DivIcon
    from streamlit_folium import st_folium

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1e293b;font-weight:800;margin-bottom:20px;'>📊 EV Seoul 전기차 등록 현황</h3>", unsafe_allow_html=True)


    # [수정됨] 필터 최상단: 다중선택이 아닌 단일 '년도' 선택으로 변경
    with st.expander("🔍 상세 필터 설정", expanded=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        with f1:
            all_districts = ["전체"] + sorted(df["시군구명"].unique().tolist())
            selected_district = st.selectbox("시군구 선택", all_districts, key="dist_filter")
        with f2:
            # 년도 내림차순 정렬 (가장 최신 년도가 기본값)
            year_options = sorted(df["기준년도"].unique().tolist(), reverse=True)
            selected_year = st.selectbox("기준년도 선택", year_options, index=0, key="year_filter")
        with f3:
            # 선택된 년도의 서울시 전체 등록대수 미리보기
            year_total = df[df["기준년도"] == selected_year]["등록대수"].sum()
            st.metric(f"{selected_year} 전기차 총 등록대수", f"{int(year_total):,}대")

    # 필터 적용 (선택된 하나의 '년도' 데이터만 남김)
    filtered = df[df["기준년도"] == selected_year].copy()
    if selected_district != "전체":
        filtered = filtered[filtered["시군구명"] == selected_district]

    st.markdown("<br>", unsafe_allow_html=True)

    # 지도 + 표
    map_col, table_col = st.columns([5, 4], gap="large")

    with map_col:
        st.markdown(f'<div class="section-title">📍 {selected_year} 지역별 등록 현황 지도</div>', unsafe_allow_html=True)

        m = folium.Map(location=[37.5665, 126.9780], zoom_start=11, tiles="CartoDB Positron")

        district_totals = filtered.groupby(["시군구명", "위도", "경도"])["등록대수"].sum().reset_index()
        max_count = district_totals["등록대수"].max() if len(district_totals) > 0 else 1

        for _, row in district_totals.iterrows():
            count   = row["등록대수"]
            ratio   = count / max_count
            radius  = 12 + ratio * 30
            is_sel  = (selected_district != "전체" and row["시군구명"] == selected_district)
            fill_c  = "#2563eb" if is_sel else "#60a5fa"
            bdr_c   = "#1d4ed8" if is_sel else "#3b82f6"
            opacity = 0.9 if is_sel else 0.65

            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=radius, color=bdr_c, weight=2 if is_sel else 1,
                fill=True, fill_color=fill_c, fill_opacity=opacity,
                popup=folium.Popup(
                    f"<div style='font-family:Noto Sans KR;'><b>{row['시군구명']}</b><br>등록대수: {int(count):,}대</div>",
                    max_width=200
                ),
                tooltip=f"{row['시군구명']}: {int(count):,}대",
            ).add_to(m)

            label_html = (
                f"<div style='"
                f"background:rgba(255,255,255,0.92);"
                f"border:1px solid {'#1d4ed8' if is_sel else '#bfdbfe'};"
                f"border-radius:6px;padding:2px 6px;"
                f"font-size:{'12px' if is_sel else '10px'};"
                f"font-weight:{'800' if is_sel else '600'};"
                f"color:{'#1e3a8a' if is_sel else '#1e40af'};"
                f"white-space:nowrap;pointer-events:none;"
                f"box-shadow:0 2px 4px rgba(0,0,0,0.10);line-height:1.4;'>"
                f"{row['시군구명']}<br>"
                f"<span style='font-size:{'11px' if is_sel else '9px'};color:{'#1d4ed8' if is_sel else '#3b82f6'};'>"
                f"{int(count):,}대</span></div>"
            )
            folium.Marker(
                location=[row["위도"] + 0.012, row["경도"]],
                icon=DivIcon(html=label_html, icon_size=(80, 36), icon_anchor=(40, 36)),
            ).add_to(m)

        st_folium(m, width=None, height=500, use_container_width=True)

    with table_col:
        st.markdown(f'<div class="section-title">📊 자치구별 현황 (막대 그래프)</div>', unsafe_allow_html=True)

        chart_data = filtered.groupby("시군구명")["등록대수"].sum().sort_values(ascending=False).reset_index()
        st.bar_chart(chart_data, x="시군구명", y="등록대수", color="#2563eb", use_container_width=True, height=550)

        # [수정됨] 연료별 피벗 테이블 추가
        #st.markdown('<div class="section-title" style="margin-top:20px;">📋 친환경 연료별 상세 표</div>', unsafe_allow_html=True)
       # if not filtered.empty:
           # pivot = filtered.groupby(["시군구명", "연료명"])["등록대수"].sum().unstack(fill_value=0)
          # pivot["합계"] = pivot.sum(axis=1)
           # pivot = pivot.sort_values("합계", ascending=False)
            #pivot.index.name = "시군구명"

           # styled = pivot.style.format("{:,.0f}").background_gradient(subset=["합계"], cmap="Blues").set_properties(**{'font-size': '13px'})
           # st.dataframe(styled, use_container_width=True, height=200)

    # KPI 카드
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📈 {selected_year} 주요 지표</div>', unsafe_allow_html=True)

    # 'filtered' 데이터프레임에는 이미 선택된 년도 데이터만 존재함!
    total        = filtered["등록대수"].sum()
    top_district = filtered.groupby("시군구명")["등록대수"].sum().idxmax() if not filtered.empty else "-"
    top_count    = filtered.groupby("시군구명")["등록대수"].sum().max() if not filtered.empty else 0
    avg          = int(filtered.groupby("시군구명")["등록대수"].sum().mean()) if not filtered.empty else 0
    
    # 전기차 비중 계산 (연료명에 '전기'가 포함된 경우)
    ev_total     = filtered[filtered["연료명"].str.contains("전기", na=False)]["등록대수"].sum()
    ratio        = int((ev_total / total) * 100) if total > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">전체 등록대수</div><div class="kpi-value">{total:,}</div><div class="kpi-sub">선택 년도 누적기준</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">최다 등록 자치구</div><div class="kpi-value">{top_district}</div><div class="kpi-sub">{top_count:,}대</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">자치구 평균</div><div class="kpi-value">{avg:,}</div><div class="kpi-sub">25개 자치구 기준</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">순수 전기차(EV) 비중</div><div class="kpi-value">{ratio}%</div><div class="kpi-sub">친환경차 중 전기차 비율</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── [추가] 년도별 추이 및 연료별 비중 섹션 ──────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    trend_col, donut_col = st.columns([5, 4], gap="large")

    with trend_col:
        st.markdown('<div class="section-title">📈 년도별 전기차 증가 추이</div>', unsafe_allow_html=True)
        
        yearly_trend = get_ev_trend_data() # 함수 연동 (파일 직접 읽기 x)
        
        st.line_chart(
            yearly_trend,
            x="기준년도", y="등록대수", color="#07f303", 
            use_container_width=True, height=350
        )

    with donut_col:
        st.markdown('<div class="section-title">🍩 연료별 자동차 등록 비중</div>', unsafe_allow_html=True)
        
        import plotly.express as px
        
        fuel_data = get_ev_fuel_data() # 함수 연동 (파일 직접 읽기 x)

        fig = px.pie(
            fuel_data, 
            values="수량", names="연료", hole=0.1,
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=True, height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 : 충전소 맵
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "📍 충전소 맵":

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1e293b;font-weight:800;margin-bottom:20px;'>📍 EV Seoul 충전소 인프라 현황</h3>", unsafe_allow_html=True)
    
    # district_code -> 지역명 매핑
    df_charge_map = df_charge.merge(
        district_df[["district_code", "district_name"]],
        on="district_code",
        how="left"
    )

    f1, f2, f3 = st.columns([3, 3, 2])
    with f1:
        all_districts = ["전체"] + sorted(df_charge_map["district_name"].dropna().unique().tolist())
        sel_dist = st.selectbox("자치구 선택", all_districts, key="charge_dist")
    with f2:
        charge_types = ["전체", "급속", "완속"]
        sel_type = st.selectbox("충전기 종류", charge_types, key="charge_type")
    with f3:
        filtered_c = df_charge_map.copy()
        if sel_dist != "전체":
            filtered_c = filtered_c[filtered_c["district_name"] == sel_dist]
        if sel_type == "급속":
            filtered_c = filtered_c[filtered_c["fast_charger"] > 0]
        elif sel_type == "완속":
            filtered_c = filtered_c[filtered_c["slow_charger"] > 0]
        filtered_c = filtered_c.dropna(subset=["lat", "lon"])
        st.metric("조회된 충전소", f"{len(filtered_c):,}개")
        
        
    st.markdown("<br>", unsafe_allow_html=True)
    map_col2, info_col = st.columns([6, 3], gap="large")

    with map_col2:
        center_lat, center_lon, zoom = 37.5665, 126.9780, 11
        if sel_dist != "전체" and len(filtered_c) > 0:
            center_lat = filtered_c["lat"].mean()
            center_lon = filtered_c["lon"].mean()
            zoom = 13

        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB Positron")
        cluster = MarkerCluster(options={"maxClusterRadius": 50, "spiderfyOnMaxZoom": True}).add_to(m2)

        for _, row in filtered_c.iterrows():
            if sel_type == "급속":
                color = "#3b82f6"
            elif sel_type == "완속":
                color = "#10b981"
            else:
                if row["fast_charger"] > 0 and row["slow_charger"] > 0:
                    color = "#8b5cf6"
                elif row["fast_charger"] > 0:
                    color = "#3b82f6"
                elif row["slow_charger"] > 0:
                    color = "#10b981"
                else:
                    color = "#94a3b8"

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=6, color=color, weight=1,
                fill=True, fill_color=color, fill_opacity=0.9,
                tooltip=row["station_name"],
                popup=folium.Popup(
                    f"<div style='font-family:Noto Sans KR;'><b>{row['station_name']}</b><br>"
                    f"<span style='color:#64748b;font-size:12px;'>{row['address']}</span><br><br>"
                    f"<b>자치구:</b> {row['district_name']}<br>"
                    f"<b>급속:</b> {int(row['fast_charger'])}대<br>"
                    f"<b>완속:</b> {int(row['slow_charger'])}대</div>",
                    max_width=250
                )
            ).add_to(cluster)

        legend_html = """
        <div style="position:absolute;bottom:30px;right:30px;z-index:9999;
                    background:rgba(255,255,255,0.95);border:1px solid #e2e8f0;
                    box-shadow:0 4px 6px rgba(0,0,0,0.05);border-radius:12px;
                    padding:14px 18px;font-size:13px;color:#1e293b;">
          <b style="font-size:14px;display:block;margin-bottom:8px;">충전기 유형</b>
          <span style="color:#3b82f6;font-size:16px;">●</span> 급속 보유 &nbsp;&nbsp;
          <span style="color:#10b981;font-size:16px;">●</span> 완속 보유 &nbsp;&nbsp;
          <span style="color:#8b5cf6;font-size:16px;">●</span> 급속+완속
        </div>
        """
        m2.get_root().html.add_child(folium.Element(legend_html))
        st_folium(m2, width=None, height=560, use_container_width=True)

    with info_col:
        st.markdown('<div class="section-title">📋 해당 충전소의 종류별 충전기 수</div>', unsafe_allow_html=True)
        if len(filtered_c) > 0:
            summary_data = [
                ("급속", int(filtered_c["fast_charger"].sum()), "#3b82f6", "#eff6ff", "#bfdbfe"),
                ("완속", int(filtered_c["slow_charger"].sum()), "#10b981", "#ecfdf5", "#a7f3d0"),
            ]

            for t, cnt, color, bg_c, bdr_c in summary_data:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:12px 18px;background:{bg_c};border:1px solid {bdr_c};
                            border-radius:12px;margin-bottom:10px;">
                    <span style="color:{color};font-weight:700;font-size:15px;">{t}</span>
                    <span style="color:#1e293b;font-weight:800;font-size:20px;">{cnt:,}
                        <span style="font-size:13px;font-weight:500;color:#64748b;">대</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">상세 리스트</div>', unsafe_allow_html=True)
        display_df = filtered_c[["station_name", "district_name", "fast_charger", "slow_charger"]].reset_index(drop=True)
        display_df.index = display_df.index + 1
        display_df.columns = ["장소명", "자치구", "급속", "완속"]
        st.dataframe(display_df.head(50), use_container_width=True, height=300)
        if len(filtered_c) > 50:
            st.caption(f"*상위 50개소 표시 (검색결과: 총 {len(filtered_c):,}개소)")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 : FAQ
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "💬 FAQ":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1e293b;font-weight:800;margin-bottom:20px;'>💬 EV Seoul 자주 묻는 질문(FAQ)</h3>", unsafe_allow_html=True)
    
    search_col, cat_col = st.columns([4, 2])
    with search_col:
        search_query = st.text_input(
            "검색",
            placeholder="🔍  궁금한 키워드를 입력하세요  (예: 보조금, 충전 요금, 배터리)",
            label_visibility="collapsed"
        )
    with cat_col:
        category = st.radio("카테고리", ["전체", "전기차", "충전소"], horizontal=True, label_visibility="collapsed")

    popular_keywords = top_rate(5)
    st.markdown("<div style='font-size:13px;color:#64748b;margin-bottom:8px;font-weight:600;'>🔥 인기 검색어</div>", unsafe_allow_html=True)
    kw_cols = st.columns(len(popular_keywords))
    for i, kw in enumerate(popular_keywords):
        with kw_cols[i]:
            if st.button(kw, key=f"kw_{i}", use_container_width=True):
                search_query = kw

    st.markdown("<br><hr style='border-color:#e2e8f0;'><br>", unsafe_allow_html=True)
    
    faqs = load_faq_data()
    if category != "전체":
        faqs = [f for f in faqs if f["category"] == category]
    if search_query:
        sq = search_query.lower()
        faqs = [f for f in faqs if (
            sq in f["question"].lower() or
            sq in f["answer"].lower() or
            any(sq in t.lower() for t in f.get("tags", []))
        )]

    st.markdown(f'<div class="section-title" style="color:#3b82f6;">검색 결과 {len(faqs)}건</div>', unsafe_allow_html=True)

    if not faqs:
        st.info("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
    else:
        for faq in faqs:
            tag_class = "tag-ev" if faq["category"] == "전기차" else "tag-charge"
            tags_html = "".join([f'<span class="faq-tag {tag_class}">{t}</span>' for t in faq["tags"]])
            with st.expander(f"{'🚗' if faq['category']=='전기차' else '⚡'}  {faq['question']}"):
                st.markdown(f"""
                <div style="font-size:15px;line-height:1.7;color:#334155;padding:12px 4px">{faq['answer']}</div>
                <div>{tags_html}</div>
                """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%);
                border:1px solid #bae6fd;border-radius:16px;padding:36px 32px;text-align:center;">
        <div style="font-size:21px;font-weight:800;color:#0369a1;margin-bottom:8px;">원하는 답변을 찾지 못하셨나요?</div>
        <div style="color:#0284c7;margin-bottom:20px;font-size:14px;">서울시 전기차 상담센터에 직접 문의해 보세요.</div>
        <div style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;">
            <div style="background:#fff;border:1px solid #7dd3fc;border-radius:12px;padding:14px 28px;color:#0369a1;font-size:17px;">
                📞 <b style="font-size:19px;">120</b> (다산콜센터)
            </div>
            <div style="background:#fff;border:1px solid #7dd3fc;border-radius:12px;padding:14px 28px;color:#0369a1;font-size:17px;">
                🌐 <b>ev.seoul.go.kr</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
