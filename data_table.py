import streamlit as st
import pandas as pd


def render_page():
    # 페이지 제목
    st.title("Market Data")

    # 3개의 탭 생성
    tab1, tab2, tab3 = st.tabs(["환율", "유가", "주식"])

    # 첫 번째 탭
    with tab1:
        import exchange_dashboard as exchange_dashboard
        exchange_dashboard.render_page()

    # 두 번째 탭
    with tab2:
        import oil_dashboard
        oil_dashboard.render_page()

    # 세 번째 탭
    with tab3:
        import stock_dashboard as stock_dashboard
        stock_dashboard.render_page()

# render_page 호출
if __name__ == "__main__":
    render_page()

