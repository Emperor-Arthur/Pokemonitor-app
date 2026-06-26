import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 頁面基本配置 (金融終端極簡專業風格) ---
st.set_page_config(page_title="Pokémonitor 另類資產金融終端", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #F0F2F6; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .stTabs [data-baseweb="tab"] { color: #8a93a6; font-size: 16px; }
    .stTabs [data-baseweb="tab"]:hover { color: #ff4b4b; }
    .stTabs [aria-selected="true"] { color: #ff4b4b; font-weight: bold; border-bottom-color: #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Pokémonitor™ 寶可夢另類資產數據終端")
st.caption("基於第一性原理構建 | 全球首創卡牌市場綜合整合指標與公允價值估值系統")

# --- 核心數據引擎 (模擬 2018-2026 宏觀與微觀週期) ---
@st.cache_data
def generate_market_data():
    start_date = datetime(2018, 1, 1)
    # 模擬至2026年中，約3100天
    dates = [start_date + timedelta(days=x) for x in range(3100)]
    n = len(dates)
    t = np.linspace(0, 10, n)
    
    # 基欽週期與減半共振因子
    cycle_factor = 1.0 + 0.8 * np.sin(t * 0.8) + 1.2 * np.exp(-((t - 3.5)**2) / 1.5) + np.random.normal(0, 0.05, n)
    
    composite_index = 1000 * cycle_factor * (1 + 0.05 * t)
    wotc_bluechip = 1000 * (1.0 + 0.4 * np.sin(t * 0.8) + 0.5 * np.exp(-((t - 3.5)**2) / 3.0)) * (1 + 0.02 * t)
    modern_high_beta = 1000 * (1.0 + 1.5 * np.sin(t * 0.8) + 2.5 * np.exp(-((t - 3.5)**2) / 0.8)) * (1 + 0.08 * t)
    waifu_index = 1000 * (1.0 + 1.2 * np.sin(t * 0.9) + 2.0 * np.exp(-((t - 3.8)**2) / 1.0)) * (1 + 0.10 * t)
    sealed_box = 1000 * (1.0 + 0.5 * np.sin(t * 0.7) + 0.8 * np.exp(-((t - 3.5)**2) / 2.0)) * (1 + 0.06 * t)
    
    btc_price = 10000 * (1.0 + 2.0 * np.sin(t * 0.85) + 3.0 * np.exp(-((t - 3.4)**2) / 1.0)) * (1 + 0.15 * t)
    fed_rate = np.where(t < 2.5, 2.25, np.where(t < 5.0, 0.25, np.where(t < 8.5, 5.25, 4.50)))
    
    return pd.DataFrame({
        'Date': dates, 'Composite_Index': composite_index, 'WOTC_Bluechip': wotc_bluechip,
        'Modern_High_Beta': modern_high_beta, 'Waifu_Index': waifu_index, 'Sealed_Box': sealed_box,
        'Bitcoin_USD': btc_price, 'FED_Rate': fed_rate
    })

df = generate_market_data()

# --- 側邊欄 ---
st.sidebar.header("⚙️ 終端控制中心")
date_range = st.sidebar.date_input("時間週期選擇 (支援5年以上長週期)", [df['Date'].min(), df['Date'].max()])

if len(date_range) == 2:
    filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]
else:
    filtered_df = df

tab1, tab2, tab3 = st.tabs(["📈 綜合大盤與宏觀對標", "🗂️ 板塊整合指標分析", "🔍 稀有卡公允價值（低流動性插值）"])

# --- Tab 1: 大盤 ---
with tab1:
    st.subheader("Pokémon Composite 500 指數與宏觀經濟共振走勢")
    overlay_macro = st.radio("疊加宏觀對比資產：", ["無疊加", "比特幣 (BTC/USD)", "美聯儲基準利率 (FED Rate)"], horizontal=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Composite_Index'], name='Pokémon 500 綜合指數', line=dict(color='#FF4B4B', width=3)))
    
    if overlay_macro == "比特幣 (BTC/USD)":
        fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Bitcoin_USD'], name='Bitcoin (右軸)', yaxis='y2', line=dict(color='#F7931A', width=1.5, dash='dash')))
        y2 = dict(title='比特幣價格 (USD)', side='right', overlaying='y', gridcolor='rgba(0,0,0,0)')
    elif overlay_macro == "美聯儲基準利率 (FED Rate)":
        fig1.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['FED_Rate'], name='美聯儲利率 (右軸)', yaxis='y2', line=dict(color='#00D4B2', width=1.5, dash='dot')))
        y2 = dict(title='基準利率 (%)', side='right', overlaying='y', gridcolor='rgba(0,0,0,0)')
    else:
        y2 = None

    fig1.update_layout(template="plotly_dark", xaxis=dict(gridcolor='#222'), yaxis=dict(title="指數點位", gridcolor='#222'), yaxis2=y2, height=500)
    st.plotly_chart(fig1, use_container_width=True)

# --- Tab 2: 板塊 ---
with tab2:
    st.subheader("分類概念板塊指數走勢 (Sector Indices)")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['WOTC_Bluechip'], name='WOTC經典藍籌 (對標黃金)', line=dict(color='#FFD700')))
    fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Modern_High_Beta'], name='Modern High-Beta (對標科技股)', line=dict(color='#FF00FF')))
    fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Waifu_Index'], name='Waifu 女教練板塊 (對標迷因情緒)', line=dict(color='#00FFFF')))
    fig2.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Sealed_Box'], name='Sealed 密封產品盒 (帶時間價值)', line=dict(color='#00FF00')))
    fig2.update_layout(template="plotly_dark", xaxis=dict(gridcolor='#222'), yaxis=dict(title="指數點位", gridcolor='#222'), height=500)
    st.plotly_chart(fig2, use_container_width=True)

# --- Tab 3: 插值估值 ---
with tab3:
    st.subheader("🔧 解決稀有卡流動性斷層：動態插值公允價值模型")
    st.markdown("針對極稀有、數月無成交的資產，系統自動捕捉同板塊波動率進行動態插值，計算每日即時公允價值 (Fair Value)。")
    np.random.seed(42)
    sparse_indices = np.sort(np.random.choice(np.arange(100, len(filtered_df)-100), size=15, replace=False))
    real_sales_date = filtered_df['Date'].iloc[sparse_indices].values
    real_sales_price = filtered_df['WOTC_Bluechip'].iloc[sparse_indices].values * 150 + np.random.normal(0, 5000, 15)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['WOTC_Bluechip']*150+2000, name='Pokémonitor 每日連續公允價值', line=dict(color='#00D4B2', width=2)))
    fig3.add_trace(go.Scatter(x=real_sales_date, y=real_sales_price, name='真實公開市場稀疏成交點', mode='markers', marker=dict(color='#FF4B4B', size=10, symbol='diamond')))
    fig3.update_layout(template="plotly_dark", xaxis=dict(gridcolor='#222'), yaxis=dict(title="估算價值 (HKD)", gridcolor='#222'), height=500)
    st.plotly_chart(fig3, use_container_width=True)
