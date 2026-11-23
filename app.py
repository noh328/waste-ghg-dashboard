import streamlit as st
st.title("🌱 쓰레기 처리의 비효율성과 온실가스 배출 분석")

st.write(
    "지역별 폐기물 발생량과 온실가스 배출량, "
    "처리 인프라 데이터를 비교하고 분석하는 대시보드입니다."
)

st.caption("분석 기준: 2022년 | 전국 17개 시·도")
st.divider()
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="폐기물 처리 분석 대시보드",
    page_icon="♻️",
    layout="wide"
)

# 제목
st.title("♻️ 폐기물 처리 및 온실가스 배출 분석")
st.caption("2022년 전국 17개 시·도 데이터를 활용한 폐기물 처리 현황 분석")

# 엑셀 데이터 불러오기
FILE = "역할1_2022_Baseline_실험결과.xlsx"

try:     
    waste = pd.read_excel(FILE, sheet_name="2022 지역별 발생량")
    treatment = pd.read_excel(FILE, sheet_name="연도별 처리방식")
    gas = pd.read_excel(FILE, sheet_name="온실가스 배출량")
    infra = pd.read_excel(FILE, sheet_name="인프라")

    # 지역명 공백 제거
    for df in [waste, gas, infra]:
        df["지역"] = df["지역"].astype(str).str.strip()

    # 전국 합계 행 제외
    waste = waste[
        ~waste["지역"].str.contains("전국|합계", na=False)
    ]

    # 지역별 데이터 통합
    data = pd.merge(waste, gas, on="지역", how="inner")
    data = pd.merge(data, infra, on="지역", how="inner")

        # 지역 선택
    st.divider()
    st.subheader("📍 지역별 데이터 분석")

    regions = data["지역"].dropna().unique().tolist()

    selected_region = st.selectbox(
        "분석할 지역을 선택하세요.",
        options=regions,
        key="region_select"
    )

    selected_data = data[data["지역"] == selected_region].iloc[0]

    st.write(f"### {selected_region} 상세 정보")

    col1, col2, col3 = st.columns(3)

    with col1:
     st.metric(
        "폐기물 발생량 (만 톤/년)",
        f"{selected_data['2022년 폐기물 발생량 (만 톤/년)']:,.1f}"
    )

    with col2:
     st.metric(
        "온실가스 배출량 (천 tonCO₂-eq)",
        f"{selected_data['온실가스 배출량 (천 tonCO₂-eq)']:,.0f}"
    )

    with col3:
     st.metric(
        "인프라 수치",
        f"{selected_data['인프라 수치 (수거함·수거차량)']:,.1f}"
    )

    st.subheader("📋 선택 지역 데이터")

    st.dataframe(
        selected_data.to_frame().T,
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("🏆 지역별 폐기물 발생량 순위")

    rank_data = data.sort_values(
        by="2022년 폐기물 발생량 (만 톤/년)",
        ascending=False
    )

    fig = px.bar(
        rank_data,
        x="지역",
        y="2022년 폐기물 발생량 (만 톤/년)",
        title="2022년 지역별 폐기물 발생량",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    selected_region = st.selectbox(
        "분석할 지역을 선택하세요.",
        sorted(data["지역"].unique())
    )

    selected = data[data["지역"] == selected_region].iloc[0]

    # 주요 지표
    st.subheader(f"📊 {selected_region} 주요 현황")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "폐기물 발생량",
        f'{selected["2022년 폐기물 발생량 (만 톤/년)"]:,.0f}만 톤'
    )

    col2.metric(
        "온실가스 배출량",
        f'{selected["온실가스 배출량 (천 tonCO₂-eq)"]:,.0f}천 톤'
    )

    col3.metric(
        "인프라 수치",
        f'{selected["인프라 수치 (수거함·수거차량)"]:,.0f}'
    )

    # 지역별 폐기물 발생량
    st.divider()
    st.subheader("📈 지역별 폐기물 발생량 비교")

    fig1 = px.bar(
        data.sort_values(
            "2022년 폐기물 발생량 (만 톤/년)",
            ascending=False
        ),
        x="지역",
        y="2022년 폐기물 발생량 (만 톤/년)",
        title="2022년 지역별 폐기물 발생량",
        labels={
            "지역": "지역",
            "2022년 폐기물 발생량 (만 톤/년)": "발생량 (만 톤)"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 온실가스 배출량
    st.divider()
    st.subheader("🌍 지역별 온실가스 배출량 비교")

    fig2 = px.bar(
        data.sort_values(
            "온실가스 배출량 (천 tonCO₂-eq)",
            ascending=False
        ),
        x="지역",
        y="온실가스 배출량 (천 tonCO₂-eq)",
        title="2022년 지역별 온실가스 배출량",
        labels={
            "지역": "지역",
            "온실가스 배출량 (천 tonCO₂-eq)": "배출량 (천 tonCO₂-eq)"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 인프라 비교
    st.divider()
    st.subheader("🚛 지역별 처리 인프라 비교")

    fig3 = px.bar(
        data.sort_values(
            "인프라 수치 (수거함·수거차량)",
            ascending=False
        ),
        x="지역",
        y="인프라 수치 (수거함·수거차량)",
        title="지역별 처리 인프라 수치",
        labels={
            "지역": "지역",
            "인프라 수치 (수거함·수거차량)": "인프라 수치"
        }
    )

    st.plotly_chart(fig3, use_container_width=True)

    # 전국 연도별 처리 방식
    st.divider()
    st.subheader("♻️ 전국 폐기물 처리 방식 변화")

    fig4 = px.line(
        treatment,
        x="연도",
        y=["매립 비율 (%)", "소각 비율 (%)", "재활용 비율 (%)"],
        markers=True,
        title="2019~2022년 전국 폐기물 처리 방식 비율 변화",
        labels={
            "value": "처리 비율 (%)",
            "variable": "처리 방식",
            "연도": "연도"
        }
    )

    st.plotly_chart(fig4, use_container_width=True)
    st.divider()
    st.subheader("📊 분석 결과 및 해석")

    st.markdown("""
    ### 1. 폐기물 발생량과 온실가스 배출량

    - 상관계수는 **0.709**로 나타났습니다.
    - 두 변수 사이에 양의 상관관계가 확인되었습니다.
    - 폐기물 발생량이 많은 지역일수록 전체 온실가스 배출량도 높은 경향을 보였습니다.

    ### 2. 분석을 통해 알 수 있는 점

    폐기물 발생량뿐만 아니라 지역별 처리 방식과 처리 인프라 등
    다양한 요인이 온실가스 배출과 관련될 수 있습니다.

    ### 3. 분석 시 주의할 점

    이번 결과는 17개 시·도 자료를 바탕으로 확인한 상관관계이며,
    직접적인 인과관계를 의미하지는 않습니다.
    """)

    st.warning("추가적인 데이터 검증과 분석이 필요합니다.")
    
    # 데이터 표
    st.divider()
    st.subheader("📋 지역별 통합 데이터")

        # 폐기물 발생량과 온실가스 배출량의 관계
    st.divider()
    st.subheader("🔎 폐기물 발생량과 온실가스 배출량의 관계")

    fig5 = px.scatter(
        data,
        x="2022년 폐기물 발생량 (만 톤/년)",
        y="온실가스 배출량 (천 tonCO₂-eq)",
        text="지역",
        hover_name="지역",
        title="지역별 폐기물 발생량과 온실가스 배출량"
    )

    st.plotly_chart(fig5, width="stretch")

    # 상관계수 계산
    corr = data["2022년 폐기물 발생량 (만 톤/년)"].corr(
        data["온실가스 배출량 (천 tonCO₂-eq)"]
    )

    st.metric("상관계수 (Pearson)", f"{corr:.3f}")

    st.caption(
        "상관계수는 두 변수 사이의 선형적인 관계를 나타내며, "
        "인과관계를 의미하지는 않습니다."
    )

        # 분석 결과 및 해석
    st.divider()
    st.subheader("📊 분석 결과 및 해석")

    st.markdown("""
    ### 1. 폐기물 발생량과 온실가스 배출량

    ### 1. 폐기물 발생량과 온실가스 배출량

    - 상관계수는 **0.709**로 나타났습니다.
    - 두 변수 사이에 양의 상관관계가 확인되었습니다.
    - 폐기물 발생량이 많은 지역일수록 전체 온실가스 배출량도 높은 경향을 보였습니다.

    ### 2. 분석을 통해 알 수 있는 점

    폐기물 발생량뿐만 아니라 지역별 처리 방식과 처리 인프라 등
    다양한 요인이 온실가스 배출과 관련될 수 있습니다.
    따라서 폐기물 처리 과정 전반을 함께 살펴볼 필요가 있습니다.

    ### 3. 분석 시 주의할 점

    이번 결과는 17개 시·도 자료를 바탕으로 확인한 상관관계이며,
    폐기물 발생량이 온실가스 배출량의 직접적인 원인이라는 의미는 아닙니다.
    또한 데이터의 단위와 출처를 확인하는 과정이 필요합니다.
    """)

    st.warning(
        "본 분석은 지역별 데이터의 관계를 탐색한 결과이며, "
        "추가적인 데이터 검증과 분석이 필요합니다."
    )

    st.dataframe(data, use_container_width=True)

    st.success("실제 엑셀 데이터를 이용한 분석이 완료되었습니다!")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")