import streamlit as st

st.set_page_config(
    page_title="서울특별시 전기자동차 현황",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 공통 CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

:root {
    --bg: #0a0f1e;
    --surface: #111827;
    --surface2: #1a2235;
    --accent: #00e5ff;
    --accent2: #7c3aed;
    --green: #10b981;
    --yellow: #f59e0b;
    --text: #e2e8f0;
    --muted: #64748b;
    --border: rgba(255,255,255,0.08);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

.stApp { background: var(--bg); }

/* 상단 헤더 */
.app-header {
    background: linear-gradient(135deg, #0a0f1e 0%, #111827 50%, #0f172a 100%);
    border-bottom: 1px solid var(--border);
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.header-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.5px;
}
.header-logo span { color: #fff; }
.header-nav {
    display: flex;
    gap: 8px;
}
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
    color: #000;
    font-weight: 700;
}

/* 카드 */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: var(--accent); }
.kpi-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.kpi-value { font-size: 28px; font-weight: 900; font-family: 'Space Grotesk'; color: var(--accent); }
.kpi-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }

/* 섹션 타이틀 */
.section-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* 표 스타일 */
.dataframe { font-size: 13px !important; }

/* 숨기기 */
.block-container { padding: 0 !important; }

/* 지도 컨테이너 */
.map-wrapper {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

/* 필터 패널 */
.filter-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}

/* Streamlit 위젯 오버라이드 */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
.stMultiSelect > div > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    gap: 4px;
    padding: 4px;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 500;
}
[aria-selected="true"] {
    background: var(--accent2) !important;
    color: #fff !important;
}
.stButton button {
    background: var(--accent) !important;
    color: #000 !important;
    font-weight: 700;
    border: none !important;
    border-radius: 8px !important;
}

/* FAQ 카드 */
.faq-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s, background 0.2s;
    cursor: pointer;
}
.faq-card:hover { border-color: var(--accent); background: var(--surface2); }
.faq-q { font-weight: 600; font-size: 14px; color: var(--text); }
.faq-a { font-size: 13px; color: var(--muted); margin-top: 8px; line-height: 1.6; }
.faq-tag {
    display: inline-block;
    background: rgba(0,229,255,0.1);
    border: 1px solid rgba(0,229,255,0.2);
    color: var(--accent);
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 100px;
    margin-right: 4px;
    margin-top: 8px;
}
.tag-ev { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3); color: var(--green); }
.tag-charge { background: rgba(245,158,11,0.1); border-color: rgba(245,158,11,0.3); color: var(--yellow); }

/* 페이지 콘텐츠 패딩 */
.page-content { padding: 24px 32px; }
</style>
""", unsafe_allow_html=True)

# ── 페이지 상태 ───────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "현황"

# ── 상단 헤더 ─────────────────────────────────────────────────────────────────

# ── 사이드바 네비게이션 ───────────────────────────────────────────────
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
import sys, os
# sys.path.insert(0, "/home/claude/ev_app")
# 실제 데이터 연결 시 data/seoul_ev_data.py의 get_ev_data() 
# 함수를 공공데이터포털 API(국토교통부 자동차 등록 현황) 호출로 교체하면 됩니다. 충전소 데이터는 환경부 전기차 충전소 API로 대체하세요.
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
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">승용 비율</div><div class="kpi-value">{ratio}%</div><div class="kpi-sub">{승용_total:,}대</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 필터 패널
    with st.expander("🔍 필터 설정", expanded=True):
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

    # 지도 + 표
    map_col, table_col = st.columns([5, 4], gap="medium")

    with map_col:
        st.markdown('<div class="section-title">📍 지역별 등록 현황 지도</div>', unsafe_allow_html=True)

        # Folium 지도
        m = folium.Map(
            location=[37.5665, 126.9780],
            zoom_start=11,
            tiles="CartoDB Positron",
        )
        folium.TileLayer(
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="CartoDB Dark Matter",
            name="Dark",
            max_zoom=19,
        ).add_to(m)

        # 구별 합계
        district_totals = filtered.groupby(["시군구명", "위도", "경도"])["등록대수"].sum().reset_index()
        max_count = district_totals["등록대수"].max() if len(district_totals) > 0 else 1

        for _, row in district_totals.iterrows():
            count = row["등록대수"]
            ratio = count / max_count
            radius = 10 + ratio * 35
            color_intensity = int(ratio * 200)
            color = f"#{255 - color_intensity:02x}{color_intensity:02x}ff"

            # 선택된 구는 강조
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
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>{row['시군구명']}</b><br>등록대수: {int(count):,}대",
                    max_width=200
                ),
                tooltip=f"{row['시군구명']}: {int(count):,}대",
            ).add_to(m)

        st_folium(m, width=None, height=480, use_container_width=True)

    with table_col:
        st.markdown('<div class="section-title">📊 등록 현황 표</div>', unsafe_allow_html=True)

        # 피벗 테이블
        pivot = filtered.groupby(["시군구명", "차량종류"])["등록대수"].sum().unstack(fill_value=0)
        pivot["합계"] = pivot.sum(axis=1)
        pivot = pivot.sort_values("합계", ascending=False)

        # 컬럼 순서 정리
        col_order = [c for c in ["승용", "승합", "화물", "특수"] if c in pivot.columns] + ["합계"]
        pivot = pivot[col_order]
        pivot.index.name = "시군구명"

        # 숫자 포맷
        styled = pivot.style.format("{:,.0f}").background_gradient(
            subset=["합계"], cmap="Blues"
        ).set_properties(**{
            'font-size': '13px',
        })

        st.dataframe(styled, use_container_width=True, height=480)

        # 하단 요약
        st.markdown(f"""
        <div style="margin-top:12px; padding:12px 16px; background:var(--surface2); border-radius:8px; font-size:13px;">
            <span style="color:var(--muted)">표시 구역:</span> <b>{len(pivot)}개</b>
            &nbsp;|&nbsp;
            <span style="color:var(--muted)">총 등록대수:</span> <b style="color:var(--accent)">{int(pivot['합계'].sum()):,}대</b>
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
    st.markdown("### ⚡ 서울시 전기차 충전소 현황")

    # 필터
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
        st.metric("충전소 수", f"{len(filtered_c):,}개소")

    map_col2, info_col = st.columns([6, 3], gap="medium")

    with map_col2:
        center_lat = 37.5665
        center_lon = 126.9780
        zoom = 11
        if sel_dist != "전체" and len(filtered_c) > 0:
            center_lat = filtered_c["위도"].mean()
            center_lon = filtered_c["경도"].mean()
            zoom = 13

        m2 = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB Positron")
        folium.TileLayer(
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="CartoDB", name="Dark", max_zoom=19,
        ).add_to(m2)

        cluster = MarkerCluster(
            options={"maxClusterRadius": 50, "spiderfyOnMaxZoom": True}
        ).add_to(m2)

        color_map = {"급속": "#00e5ff", "완속": "#10b981", "초급속": "#f59e0b"}
        icon_map = {"급속": "bolt", "완속": "plug", "초급속": "star"}

        for _, row in filtered_c.iterrows():
            color = color_map.get(row["충전기종류"], "#888")
            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                tooltip=row["설치장소명"],
                popup=folium.Popup(
                    f"<b>{row['설치장소명']}</b><br>{row['주소']}<br>종류: {row['충전기종류']}<br>운영: {row['운영시간']}",
                    max_width=250
                )
            ).add_to(cluster)

        # 범례
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
        st.markdown('<div class="section-title">📋 충전소 목록</div>', unsafe_allow_html=True)

        # 통계
        if len(filtered_c) > 0:
            type_counts = filtered_c["충전기종류"].value_counts()
            for t, cnt in type_counts.items():
                color = {"급속": "#00e5ff", "완속": "#10b981", "초급속": "#f59e0b"}.get(t, "#888")
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:10px 14px;background:var(--surface);border:1px solid var(--border);
                            border-radius:8px;margin-bottom:8px;">
                    <span style="color:{color};font-weight:600">{t}</span>
                    <span style="color:var(--accent);font-weight:700;font-size:18px">{cnt:,}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">목록 상세</div>', unsafe_allow_html=True)

        display_df = filtered_c[["설치장소명", "충전기종류", "운영시간"]].reset_index(drop=True)
        display_df.columns = ["장소명", "종류", "운영시간"]
        st.dataframe(display_df.head(50), use_container_width=True, height=350)

        if len(filtered_c) > 50:
            st.caption(f"*상위 50개 표시 (전체 {len(filtered_c)}개)")

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 : FAQ
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "FAQ":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown("### 💬 자주 묻는 질문")

    # 검색 + 카테고리
    search_col, cat_col = st.columns([4, 2])
    with search_col:
        search_query = st.text_input(
            "검색",
            placeholder="🔍  궁금한 키워드를 입력하세요  (예: 보조금, 충전 요금, 배터리)",
            label_visibility="collapsed"
        )
    with cat_col:
        category = st.radio(
            "카테고리",
            ["전체", "전기차", "충전소"],
            horizontal=True,
            label_visibility="collapsed"
        )

    # 인기 검색어
    popular_keywords = ["보조금", "충전 요금", "배터리 수명", "급속충전", "세금 혜택", "아파트 충전기"]
    st.markdown("**인기 검색어:**", )
    kw_cols = st.columns(len(popular_keywords))
    for i, kw in enumerate(popular_keywords):
        with kw_cols[i]:
            if st.button(kw, key=f"kw_{i}", use_container_width=True):
                search_query = kw
                st.session_state[f"search_q"] = kw

    st.markdown("<br>", unsafe_allow_html=True)

    # 필터
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

    # 결과
    st.markdown(f'<div class="section-title">검색 결과 {len(faqs)}건</div>', unsafe_allow_html=True)

    if not faqs:
        st.info("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
    else:
        for faq in faqs:
            tag_class = "tag-ev" if faq["category"] == "전기차" else "tag-charge"
            tags_html = "".join([f'<span class="faq-tag {tag_class}">{t}</span>' for t in faq["tags"]])

            with st.expander(f"{'🚗' if faq['category']=='전기차' else '⚡'} {faq['question']}"):
                st.markdown(f"""
                <div style="font-size:15px;line-height:1.7;color:#334155;padding:12px 4px">
                    {faq['answer']}
                </div>
                <div>{tags_html}</div>
                """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 문의 CTA
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
