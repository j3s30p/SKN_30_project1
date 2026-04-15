import streamlit as st

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
sys.path.insert(0, "Users\playdata2\SK_AI_Camp_TeamProject1")
from data.seoul_ev_data import get_ev_data, get_charging_station_data, get_load_faq_data

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
# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 : INFO
# ─────────────────────────────────────────────────────────────────────────────

if selected_page == "🏠 EV Seoul 소개 (INFO)":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    
    # 히어로 섹션
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px 80px 20px;">
        <div style="display: inline-block; padding: 6px 16px; background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 100px; color: #00e5ff; font-size: 13px; font-weight: 700; margin-bottom: 24px; letter-spacing: 1px;">
            SMART MOBILITY CITY
        </div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 4rem; font-weight: 900; margin-bottom: 20px; line-height: 1.2;">
            미래를 향한 푸른 발걸음<br>
            <span style="background: linear-gradient(90deg, #10b981 0%, #00e5ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EV Seoul</span>과 함께
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; font-weight: 400; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            서울특별시의 전기차 보급 현황과 충전소 인프라를 한눈에 파악하세요.<br>
            시민들을 위한 편리하고 스마트한 데이터 통합 플랫폼입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 기능 카드 섹션 (3열)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">현황 대시보드</div>
            <div class="feature-desc">
                서울시 25개 자치구별 전기자동차 등록 대수 및 차종별 분포를 
                다양한 필터와 지도 시각화를 통해 직관적으로 분석합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📍</div>
            <div class="feature-title">스마트 충전소 맵</div>
            <div class="feature-desc">
                현재 위치 주변이나 원하는 자치구의 충전소를 빠르게 찾을 수 있습니다.
                급속, 완속 등 충전기 타입과 운영시간을 확인하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">자주 묻는 질문 (FAQ)</div>
            <div class="feature-desc">
                전기차 보조금, 혜택, 충전기 이용 방법 등 
                시민들이 가장 궁금해하는 핵심 정보들을 키워드로 쉽게 검색해 보세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 하단 안내
    st.markdown("""
    <div style="text-align: center; margin-top: 80px; padding-top: 40px; border-top: 1px solid var(--border);">
        <p style="color: #64748b; font-size: 14px;">
            👈 왼쪽 <b>사이드바 메뉴</b>에서 원하시는 기능을 선택하여 시작하세요!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    
# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 : 현황
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "📊 현황 대시보드":
    import folium
    from folium import DivIcon
    from streamlit_folium import st_folium

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("### 📊 EV Seoul 전기차 등록 현황")

    # 필터 (최상단)
    with st.expander("🔍 상세 필터 설정", expanded=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        with f1:
            all_districts = ["전체"] + sorted(df["시군구명"].unique().tolist())
            selected_district = st.selectbox("시군구 선택", all_districts, key="dist_filter")
        with f2:
            vehicle_options = df["차량종류"].unique().tolist()
            selected_vehicles = st.multiselect("차량 종류", vehicle_options, default=vehicle_options, key="vtype_filter")
        with f3:
            st.metric("선택된 차량종류", f"{len(selected_vehicles)}종")

    filtered = df.copy()
    if selected_district != "전체":
        filtered = filtered[filtered["시군구명"] == selected_district]
    if selected_vehicles:
        filtered = filtered[filtered["차량종류"].isin(selected_vehicles)]

    st.markdown("<br>", unsafe_allow_html=True)

    # [수정 2] 지도 + 표 먼저
    map_col, table_col = st.columns([5, 4], gap="large")

    with map_col:
        st.markdown('<div class="section-title">📍 지역별 등록 현황 지도</div>', unsafe_allow_html=True)

        m = folium.Map(location=[37.5665, 126.9780], zoom_start=11, tiles="CartoDB Positron")

        district_totals = (
            filtered.groupby(["시군구명", "위도", "경도"])["등록대수"]
            .sum().reset_index()
        )
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

            # [수정 1] 항상 보이는 지역명 + 등록대수 라벨
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

    ######    

    with table_col:
        st.markdown('<div class="section-title">📊 자치구별 등록 현황 (막대 그래프)</div>', unsafe_allow_html=True)

        # 1. 데이터 가공: 시군구별 합계만 추출하여 내림차순 정렬
        chart_data = filtered.groupby("시군구명")["등록대수"].sum().sort_values(ascending=False).reset_index()

        # 2. 막대 그래프 출력 (지역명 & 합계만 표시)
        st.bar_chart(
            chart_data, 
            x="시군구명", 
            y="등록대수", 
            color="#2563eb", 
            use_container_width=True,
            height=480
        )

        # 3. 하단 요약 정보
        st.markdown(f"""
        <div style="margin-top:12px;padding:14px 18px;background:#f8fafc;
                    border:1px solid #e2e8f0;border-radius:12px;font-size:13px;text-align:center;">
            <span style="color:#64748b">표시 구역:</span> <b>{len(chart_data)}개</b>
            <span style="margin:0 10px;color:#cbd5e1;">|</span>
            <span style="color:#64748b">총 등록대수:</span>
            <b style="color:#2563eb; font-size:15px;">{int(chart_data['등록대수'].sum()):,}대</b>
        </div>
        """, unsafe_allow_html=True)

    # [수정 2] KPI 카드 — 지도·표 아래
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 주요 지표</div>', unsafe_allow_html=True)

    total        = df["등록대수"].sum()
    top_district = df.groupby("시군구명")["등록대수"].sum().idxmax()
    top_count    = df.groupby("시군구명")["등록대수"].sum().max()
    avg          = int(df.groupby("시군구명")["등록대수"].sum().mean())
    승용_total   = df[df["차량종류"] == "승용"]["등록대수"].sum()
    ratio        = int(승용_total / total * 100)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">전체 전기차 등록</div><div class="kpi-value">{total:,}</div><div class="kpi-sub">서울특별시 전체</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">최다 등록 자치구</div><div class="kpi-value">{top_district}</div><div class="kpi-sub">{top_count:,}대</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">자치구 평균</div><div class="kpi-value">{avg:,}</div><div class="kpi-sub">25개 자치구 기준</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">승용차 비율</div><div class="kpi-value">{ratio}%</div><div class="kpi-sub">{승용_total:,}대</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)



    # ── [추가] 년도별 추이 및 연료별 비중 섹션 ──────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    trend_col, donut_col = st.columns([5, 4], gap="large")

    with trend_col:
        st.markdown('<div class="section-title">📈 년도별 전기차 증가 추이</div>', unsafe_allow_html=True)
        
        yearly_trend = pd.read_csv("data/ev_trend.csv")
        
       
        st.line_chart(
            yearly_trend,
            x="기준년도",
            y="등록대수",
            color="#07f303", 
            use_container_width=True,
            height=350
        )

    with donut_col:
        st.markdown('<div class="section-title">🍩 연료별 자동차 등록 비중</div>', unsafe_allow_html=True)
        
        
        import plotly.express as px

        
        fuel_data = pd.read_csv("data/ev_fuel.csv") ###실제데이터 삽입

        fig = px.pie(
            fuel_data, 
            values="수량", 
            names="연료", 
            hole=0.1,
            color_discrete_sequence=px.colors.sequential.Greens # 색상 테마
        )
        
        # 그래프 레이아웃 깔끔하게 조정
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            height=350,
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 : 충전소 맵
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "📍 충전소 맵":
    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1e293b;font-weight:800;margin-bottom:20px;'>📍 EV Seoul 충전소 인프라 현황</h3>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns([3, 3, 2])
    with f1:
        all_districts = ["전체"] + sorted(df_charge["시군구명"].unique().tolist())
        sel_dist = st.selectbox("자치구 선택", all_districts, key="charge_dist")
    with f2:
        charge_types = ["전체"] + sorted(df_charge["충전기종류"].unique().tolist())
        sel_type = st.selectbox("충전기 종류", charge_types, key="charge_type")
    with f3:
        filtered_c = df_charge.copy()
        if sel_dist != "전체":
            filtered_c = filtered_c[filtered_c["시군구명"] == sel_dist]
        if sel_type != "전체":
            filtered_c = filtered_c[filtered_c["충전기종류"] == sel_type]
        st.metric("조회된 충전소", f"{len(filtered_c):,}개")

    st.markdown("<br>", unsafe_allow_html=True)
    map_col2, info_col = st.columns([6, 3], gap="large")

    with map_col2:
        center_lat, center_lon, zoom = 37.5665, 126.9780, 11
        if sel_dist != "전체" and len(filtered_c) > 0:
            center_lat = filtered_c["위도"].mean()
            center_lon = filtered_c["경도"].mean()
            zoom = 13

        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB Positron")
        cluster = MarkerCluster(options={"maxClusterRadius": 50, "spiderfyOnMaxZoom": True}).add_to(m2)

        color_map = {"급속": "#3b82f6", "완속": "#10b981", "초급속": "#f59e0b"}
        for _, row in filtered_c.iterrows():
            color = color_map.get(row["충전기종류"], "#fb0473")
            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=6, color=color, weight=1,
                fill=True, fill_color=color, fill_opacity=0.9,
                tooltip=row["설치장소명"],
                popup=folium.Popup(
                    f"<div style='font-family:Noto Sans KR;'><b>{row['설치장소명']}</b><br>"
                    f"<span style='color:#64748b;font-size:12px;'>{row['주소']}</span><br><br>"
                    f"<b>종류:</b> {row['충전기종류']}<br><b>운영:</b> {row['운영시간']}</div>",
                    max_width=250
                )
            ).add_to(cluster)

        legend_html = """
        <div style="position:absolute;bottom:30px;right:30px;z-index:9999;
                    background:rgba(255,255,255,0.95);border:1px solid #e2e8f0;
                    box-shadow:0 4px 6px rgba(0,0,0,0.05);border-radius:12px;
                    padding:14px 18px;font-size:13px;color:#1e293b;">
          <b style="font-size:14px;display:block;margin-bottom:8px;">충전기 종류</b>
          <span style="color:#3b82f6;font-size:16px;">●</span> 급속 &nbsp;&nbsp;
          <span style="color:#10b981;font-size:16px;">●</span> 완속 &nbsp;&nbsp;
          <span style="color:#f59e0b;font-size:16px;">●</span> 초급속
        </div>
        """
        m2.get_root().html.add_child(folium.Element(legend_html))
        st_folium(m2, width=None, height=560, use_container_width=True)

    with info_col:
        st.markdown('<div class="section-title">📋 시설 요약</div>', unsafe_allow_html=True)
        if len(filtered_c) > 0:
            for t, cnt in filtered_c["충전기종류"].value_counts().items():
                color    = {"급속": "#3b82f6", "완속": "#10b981", "초급속": "#f59e0b"}.get(t, "#94a3b8")
                bg_c     = {"급속": "#eff6ff",  "완속": "#ecfdf5",  "초급속": "#fffbeb"}.get(t, "#f8fafc")
                bdr_c    = {"급속": "#bfdbfe",  "완속": "#a7f3d0",  "초급속": "#fde68a"}.get(t, "#e2e8f0")
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
        display_df = filtered_c[["설치장소명", "충전기종류", "운영시간"]].reset_index(drop=True)
        display_df.columns = ["장소명", "종류", "운영시간"]
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

    popular_keywords = ["보조금", "충전 요금", "배터리 수명", "급속충전", "세금 혜택", "아파트 충전기"]
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
