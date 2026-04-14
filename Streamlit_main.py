import streamlit as st

st.set_page_config(
    page_title="서울특별시 전기자동차 현황",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded", # 사이드바 표시
)

# ── 공통 CSS (모던 라이트 테마) ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');


:root {
    --bg: #f8fafc;           /* 아주 밝은 회색 배경 */
    --surface: #ffffff;      /* 흰색 카드 배경 */
    --surface2: #f1f5f9;     /* 옅은 회색 (호버/보조) */
    --accent: #2563eb;       /* 신뢰감 있는 블루 */
    --accent-hover: #1d4ed8; 
    --accent2: #0ea5e9;      /* 스카이 블루 */
    --green: #10b981;        /* 에메랄드 그린 */
    --yellow: #f59e0b;       /* 앰버(주황/노랑) */
    --text: #1e293b;         /* 진한 슬레이트 (기본 텍스트) */
    --muted: #64748b;        /* 중간 슬레이트 (보조 텍스트) */
    --border: #e2e8f0;       /* 부드러운 경계선 */
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

.stApp { background: var(--bg); }

/* 상단 헤더 */
.app-header {
    background: #ffffff;
    border-bottom: 1px solid var(--border);
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.header-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.5px;
}
.header-logo span { color: #0f172a; }

/* 네비게이션 버튼 */
.nav-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 6px 16px;
    border-radius: 6px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Noto Sans KR', sans-serif;
}
.nav-btn.active {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
    font-weight: 700;
}

/* 카드 */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { 
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
}
.kpi-label { font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 8px; }
.kpi-value { font-size: 32px; font-weight: 800; font-family: 'Space Grotesk'; color: var(--accent); }
.kpi-sub { font-size: 13px; color: var(--muted); margin-top: 6px; font-weight: 500; }

/* 섹션 타이틀 */
.section-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 숨기기 */
.block-container { padding: 0 !important; }

/* 필터 패널 */
.filter-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: var(--shadow);
}

/* Streamlit 위젯 오버라이드 */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
.stMultiSelect > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
}
[data-baseweb="tab-list"] {
    background: var(--surface2) !important;
    border-radius: 10px !important;
    gap: 4px;
    padding: 4px;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 600;
}
[aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--accent) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stButton button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    font-weight: 600;
    border-radius: 8px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.stButton button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* 활성화된 네비게이션 버튼 흉내 (Streamlit 버튼으로 구현됨) */
.stButton button p { margin: 0; }

/* FAQ 카드 */
.faq-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: var(--shadow);
}
.faq-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 100px;
    margin-right: 6px;
    margin-top: 12px;
}
.tag-ev { background: #ecfdf5; color: var(--green); border: 1px solid #a7f3d0; }
.tag-charge { background: #fffbeb; color: var(--yellow); border: 1px solid #fde68a; }

/* 페이지 콘텐츠 패딩 */
.page-content { padding: 32px 40px; }
</style>
""", unsafe_allow_html=True)

# ── 페이지 상태 ───────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "현황"

# ── 상단 헤더 ─────────────────────────────────────────────────────────────────
# ── 사이드바 네비게이션 ───────────────────────────────────────────────
#    사이드바로 수정 
st.sidebar.markdown("## ⚡ 서울 EV 현황 시스템 메뉴")

pages = ["현황", "충전소 맵", "FAQ"]

selected_page = st.sidebar.selectbox(
    "페이지 선택",
    pages,
    index=pages.index(st.session_state.page)
)

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()
st.markdown("---")
# ── 데이터 로드 ───────────────────────────────────────────────────────────────
# 실제 데이터 연동 모듈 (기존 코드 유지)
from data.seoul_ev_data import get_ev_data, get_charging_station_data, FAQ_DATA

@st.cache_data
def load_data():
    return get_ev_data()

@st.cache_data
def load_charging():
    return get_charging_station_data()

df = load_data()
df_charge = load_charging()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 : 현황
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "현황":
    import pandas as pd
    import folium
    from streamlit_folium import st_folium

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("### ⚡ 서울특별시 전기차 등록 현황")

    # KPI 행
    total = df["등록대수"].sum()
    top_district = df.groupby("시군구명")["등록대수"].sum().idxmax()
    top_count = df.groupby("시군구명")["등록대수"].sum().max()
    avg = int(df.groupby("시군구명")["등록대수"].sum().mean())

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">전체 전기차 등록</div><div class="kpi-value">{total:,}</div><div class="kpi-sub">서울특별시 전체</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">최다 등록 자치구</div><div class="kpi-value">{top_district}</div><div class="kpi-sub">{top_count:,}대</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">자치구 평균</div><div class="kpi-value">{avg:,}</div><div class="kpi-sub">25개 자치구 기준</div></div>', unsafe_allow_html=True)
    with k4:
        승용_total = df[df["차량종류"]=="승용"]["등록대수"].sum()
        ratio = int(승용_total/total*100)
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">승용차 비율</div><div class="kpi-value">{ratio}%</div><div class="kpi-sub">{승용_total:,}대</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 필터 패널
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

    # 필터 적용
    filtered = df.copy()
    if selected_district != "전체":
        filtered = filtered[filtered["시군구명"] == selected_district]
    if selected_vehicles:
        filtered = filtered[filtered["차량종류"].isin(selected_vehicles)]

    st.markdown("<br>", unsafe_allow_html=True)

    # 지도 + 표
    map_col, table_col = st.columns([5, 4], gap="large")

    with map_col:
        st.markdown('<div class="section-title">📍 지역별 등록 현황 지도</div>', unsafe_allow_html=True)

        # 밝은 Folium 지도----수정 
        m = folium.Map(
            location=[37.5665, 126.9780],
            zoom_start=11,
            tiles="CartoDB Positron", 
        )

        # 구별 합계
        district_totals = filtered.groupby(["시군구명", "위도", "경도"])["등록대수"].sum().reset_index()
        max_count = district_totals["등록대수"].max() if len(district_totals) > 0 else 1

        for _, row in district_totals.iterrows():
            count = row["등록대수"]
            ratio = count / max_count
            radius = 12 + ratio * 30
            
            # 선택된 구는 눈에 띄는 블루, 나머지는 부드러운 스카이블루
            is_selected = (selected_district != "전체" and row["시군구명"] == selected_district)
            fill_color = "#2563eb" if is_selected else "#60a5fa"
            border_color = "#1d4ed8" if is_selected else "#3b82f6"
            opacity = 0.9 if is_selected else 0.6

            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=radius,
                color=border_color,
                weight=2 if is_selected else 1,
                fill=True,
                fill_color=fill_color,
                fill_opacity=opacity,
                popup=folium.Popup(
                    f"<div style='font-family: Noto Sans KR;'><b>{row['시군구명']}</b><br>등록대수: {int(count):,}대</div>",
                    max_width=200
                ),
                tooltip=f"{row['시군구명']}: {int(count):,}대",
            ).add_to(m)

        st_folium(m, width=None, height=480, use_container_width=True)

    with table_col:
        st.markdown('<div class="section-title">📊 자치구별 세부 현황</div>', unsafe_allow_html=True)

        pivot = filtered.groupby(["시군구명", "차량종류"])["등록대수"].sum().unstack(fill_value=0)
        pivot["합계"] = pivot.sum(axis=1)
        pivot = pivot.sort_values("합계", ascending=False)

        col_order = [c for c in ["승용", "승합", "화물", "특수"] if c in pivot.columns] + ["합계"]
        pivot = pivot[col_order]
        pivot.index.name = "시군구명"

        styled = pivot.style.format("{:,.0f}").background_gradient(
            subset=["합계"], cmap="Blues"
        ).set_properties(**{
            'font-size': '13px',
            'background-color': '#ffffff',
        })

        st.dataframe(styled, use_container_width=True, height=480)

        st.markdown(f"""
        <div style="margin-top:16px; padding:16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; font-size:14px; text-align:center;">
            <span style="color:#64748b">표시 구역:</span> <b>{len(pivot)}개</b>
            <span style="margin: 0 12px; color:#cbd5e1;">|</span>
            <span style="color:#64748b">총 등록대수:</span> <b style="color:#2563eb; font-size:16px;">{int(pivot['합계'].sum()):,}대</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 : 충전소 맵
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "충전소 맵":
    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1e293b; font-weight:800; margin-bottom:24px;'>⚡ 서울시 전기차 충전소 인프라 현황</h3>", unsafe_allow_html=True)

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
        st.metric("조회된 충전소", f"{len(filtered_c):,}개소")

    st.markdown("<br>", unsafe_allow_html=True)
    map_col2, info_col = st.columns([6, 3], gap="large")

    with map_col2:
        center_lat = 37.5665
        center_lon = 126.9780
        zoom = 11
        if sel_dist != "전체" and len(filtered_c) > 0:
            center_lat = filtered_c["위도"].mean()
            center_lon = filtered_c["경도"].mean()
            zoom = 13

        # 밝은 지도(수정부분)
        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB Positron")

        cluster = MarkerCluster(
            options={"maxClusterRadius": 50, "spiderfyOnMaxZoom": True}
        ).add_to(m2)

        color_map = {"급속": "#3b82f6", "완속": "#10b981", "초급속": "#f50b0b"}

        for _, row in filtered_c.iterrows():
            color = color_map.get(row["충전기종류"], "#fb0473")  
            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=6,
                color=color,
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                tooltip=row["설치장소명"],
                popup=folium.Popup(
                    f"<div style='font-family:Noto Sans KR;'><b>{row['설치장소명']}</b><br><span style='color:#64748b;font-size:12px;'>{row['주소']}</span><br><br><b>종류:</b> {row['충전기종류']}<br><b>운영:</b> {row['운영시간']}</div>",
                    max_width=250
                )
            ).add_to(cluster)

        # 수정 부분
        legend_html = """
        <div style="position:absolute;bottom:30px;right:30px;z-index:9999;background:rgba(255,255,255,0.95); 
                    border:1px solid #e2e8f0;box-shadow:0 4px 6px rgba(0,0,0,0.05);border-radius:12px;padding:16px;font-size:13px;color:#1e293b;">
        <b style="font-size:14px; display:block; margin-bottom:8px;">충전기 종류</b>
        <span style="color:#3b82f6; font-size:16px;">●</span> 급속 &nbsp;&nbsp;
        <span style="color:#10b981; font-size:16px;">●</span> 완속 &nbsp;&nbsp;
        <span style="color:#f59e0b; font-size:16px;">●</span> 초급속
        </div>
        """
        m2.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m2, width=None, height=560, use_container_width=True)

    with info_col:
        st.markdown('<div class="section-title">📋 시설 요약</div>', unsafe_allow_html=True)

        if len(filtered_c) > 0:
            type_counts = filtered_c["충전기종류"].value_counts()
            for t, cnt in type_counts.items():
                color = {"급속": "#3b82f6", "완속": "#10b981", "초급속": "#f59e0b"}.get(t, "#94a3b8")
                bg_color = {"급속": "#eff6ff", "완속": "#ecfdf5", "초급속": "#fffbeb"}.get(t, "#f8fafc")
                border_color = {"급속": "#bfdbfe", "완속": "#a7f3d0", "초급속": "#fde68a"}.get(t, "#e2e8f0")
                
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:14px 20px;background:{bg_color};border:1px solid {border_color};
                            border-radius:12px;margin-bottom:12px;">
                    <span style="color:{color};font-weight:700;font-size:15px;">{t}</span>
                    <span style="color:#1e293b;font-weight:800;font-size:20px">{cnt:,} <span style="font-size:13px; font-weight:500; color:#64748b;">대</span></span>
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

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 : FAQ
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "FAQ":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1e293b; font-weight:800; margin-bottom:24px;'>💬 무엇을 도와드릴까요?</h3>", unsafe_allow_html=True)

    search_col, cat_col = st.columns([4, 2])
    with search_col:
        search_query = st.text_input(
            "검색",
            placeholder="🔍  궁금한 키워드를 입력하세요  (예: 보조금, 충전 요금, 배터리)",
            label_visibility="collapsed"
        )
    with cat_col:
        category = st.radio(
            "카테고리",
            ["전체", "전기차", "충전소"],
            horizontal=True,
            label_visibility="collapsed"
        )

    popular_keywords = ["보조금", "충전 요금", "배터리 수명", "급속충전", "세금 혜택", "아파트 충전기"]
    st.markdown("<div style='font-size:13px; color:#64748b; margin-bottom:8px; font-weight:600;'>🔥 인기 검색어</div>", unsafe_allow_html=True)
    
    kw_cols = st.columns(len(popular_keywords))
    for i, kw in enumerate(popular_keywords):
        with kw_cols[i]:
            if st.button(kw, key=f"kw_{i}", use_container_width=True):
                search_query = kw
                st.session_state[f"search_q"] = kw

    st.markdown("<br><hr style='border-color:#e2e8f0;'><br>", unsafe_allow_html=True)

    faqs = FAQ_DATA
    if category != "전체":
        faqs = [f for f in faqs if f["category"] == category]
    if search_query:
        sq = search_query.lower()
        faqs = [f for f in faqs if (
            sq in f["question"].lower() or
            sq in f["answer"].lower() or
            any(sq in t for t in f["tags"])
        )]

    st.markdown(f'<div class="section-title" style="color:#3b82f6;">검색 결과 {len(faqs)}건</div>', unsafe_allow_html=True)

    if not faqs:
        st.info("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
    else:
        for faq in faqs:
            tag_class = "tag-ev" if faq["category"] == "전기차" else "tag-charge"
            tags_html = "".join([f'<span class="faq-tag {tag_class}">{t}</span>' for t in faq["tags"]])

            # 수정부분
            with st.expander(f"{'🚗' if faq['category']=='전기차' else '⚡'}  {faq['question']}"):
                st.markdown(f"""
                <div style="font-size:15px;line-height:1.7;color:#334155;padding:12px 4px">
                    {faq['answer']}
                </div>
                <div>{tags_html}</div>
                """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 수정 부분
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                border: 1px solid #bae6fd; border-radius: 16px; padding: 40px 32px; text-align: center; box-shadow: var(--shadow);">
        <div style="font-size:22px; font-weight:800; color:#0369a1; margin-bottom:8px;">원하는 답변을 찾지 못하셨나요?</div>
        <div style="color:#0284c7; margin-bottom:24px; font-size:15px;">서울시 전기차 상담센터에 직접 문의해 보세요. 친절하게 안내해 드립니다.</div>
        <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
            <div style="background:#ffffff; border:1px solid #7dd3fc; border-radius:12px; padding:16px 32px; color:#0369a1; font-size:18px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                📞 <b style="font-size:20px;">120</b> (다산콜센터)
            </div>
            <div style="background:#ffffff; border:1px solid #7dd3fc; border-radius:12px; padding:16px 32px; color:#0369a1; font-size:18px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                🌐 <b>ev.seoul.go.kr</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)





    #
