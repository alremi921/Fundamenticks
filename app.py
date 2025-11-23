import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os
from datetime import datetime, timedelta

# -------------------------
# 1. KONFIGURACE A STAV MENU
# -------------------------
# Inicializace stavu menu PŘED set_page_config
if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'collapsed'

st.set_page_config(
    page_title="Fundamenticks", 
    layout="wide", 
    initial_sidebar_state=st.session_state['sidebar_state']
)

# -------------------------
# 2. CSS DESIGN (HACKER TERMINAL)
# -------------------------
st.markdown("""
    <style>
        /* HLAVNÍ BARVY */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* SKRYTÍ VŠECH STREAMLIT UI PRVKŮ */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        footer {display: none !important;}
        .stAppDeployButton {display: none !important;}
        
        /* SKRYTÍ PŮVODNÍ ŠIPKY PRO MENU */
        [data-testid="collapsedControl"] {
            display: none;
        }

        /* STYL SIDEBARU */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #00FF00;
        }

        /* TEXTY */
        h1, h2, h3, h4, p, div, span, li, ul {
            font-family: 'Courier New', Courier, monospace !important;
            color: #E0E0E0 !important;
        }
        
        /* NADPISY */
        h1, h2, h3 {
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* LOGO TEXT */
        .brand-text {
            font-size: 26px;
            font-weight: 900;
            color: #00FF00;
            letter-spacing: 2px;
            margin-top: 5px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }

        /* TLAČÍTKA (ZELENÝ RÁMEČEK) */
        .stButton > button {
            background-color: #000000 !important;
            color: #00FF00 !important;
            border: 1px solid #00FF00 !important;
            border-radius: 0px !important;
            text-transform: uppercase;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: #00FF00 !important;
            color: #000000 !important;
            box-shadow: 0 0 10px #00FF00;
        }

        /* BOXÍKY (KARTY) */
        .data-box {
            border: 1px solid #333;
            background-color: #0a0a0a;
            padding: 20px;
            margin-bottom: 15px;
            height: 100%;
        }
        
        .paid-box {
            border: 1px solid #00FF00 !important;
            background-color: #0a0a0a;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 0 5px rgba(0, 255, 0, 0.1);
            height: 100%;
        }
        
        /* TABULKY (DATAFRAME) - Úprava pro tmavý režim */
        div[data-testid="stDataFrame"] {
            border: 1px solid #333;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 3. DATA LOADERS & HELPERS
# -------------------------
# Cesty k souborům
CSV_FILE_PATH = "usd_macro_history.csv.txt" 
DXY_LINES_PATH = "dxy_linechart_history.csv.txt" 
DXY_HEATMAP_PATH = "dxy_seasonality_heatmap_history.csv.txt" 

LOOKBACK_DAYS = 365 
TODAY = datetime.utcnow()
START_DATE = TODAY - timedelta(days=LOOKBACK_DAYS)

def clean_num(x):
    """Pomocná funkce pro čištění čísel"""
    if x is None: return None
    s = str(x).strip()
    if s.startswith('.'): s = s[1:]
    if s == "" or s == "-" or s.lower() == "n/a" or s.lower() == "nan": return None
    s = s.replace(",", ".").replace("%", "").replace("K", "000").replace("M", "000000").replace("B", "000000000")
    try: return float(s)
    except: return None

def score_event(row):
    """Výpočet skóre pro událost"""
    a = clean_num(row.get("Actual"))
    f = clean_num(row.get("Forecast"))
    if a is None or f is None: return 0
    if a > f: return 1
    if a < f: return -1
    return 0

@st.cache_data
def load_events_from_csv():
    """Načtení makro dat"""
    if not os.path.exists(CSV_FILE_PATH):
        return pd.DataFrame()
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df["DateParsed"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["DateParsed"].notna()]
        return df.sort_values("DateParsed", ascending=False).reset_index(drop=True)
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_seasonality_lines_data():
    """Načtení dat pro line chart"""
    if not os.path.exists(DXY_LINES_PATH): return pd.DataFrame()
    try:
        df = pd.read_csv(DXY_LINES_PATH, decimal='.', sep=',')
        month_to_index = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        df['Month_Index'] = df['Month'].map(month_to_index)
        return df.sort_values('Month_Index').reset_index(drop=True)
    except: return pd.DataFrame()

@st.cache_data
def load_seasonality_heatmap_data():
    """Načtení dat pro heatmapu"""
    if not os.path.exists(DXY_HEATMAP_PATH): return pd.DataFrame()
    try:
        df = pd.read_csv(DXY_HEATMAP_PATH, sep=',', decimal='.')
        df['Return'] = pd.to_numeric(df['Return'], errors='coerce', downcast='float')
        df = df[df['Return'].notna()]
        df['Year'] = df['Year'].astype(str)
        month_to_index = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        df['Month_Index'] = df['Month'].map(month_to_index)
        return df.sort_values(['Year', 'Month_Index'], ascending=[False, True]).reset_index(drop=True)
    except: return pd.DataFrame()

# -------------------------
# 4. AUTENTIZACE
# -------------------------
if 'authentication_status' not in st.session_state: st.session_state['authentication_status'] = None
if 'username' not in st.session_state: st.session_state['username'] = None

names = ['SYSTEM ADMIN', 'GUEST USER']
usernames = ['admin', 'guest']
hashed_passwords = [
    '$2b$12$R.S4lQd8I/Iq3ZlA5tQ9uOxFp/H32mXJjK/iM0V1n4hR', 
    '$2b$12$t3n1S7pC2pP7tKjO9XbH9OqT3yGgY7Xw8tW1wG7p8r'
]

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'cookie_v16_menu', 'key_v16_menu', cookie_expiry_days=1
)

if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'dashboard_home'

# -------------------------
# 5. UI FUNKCE - MENU
# -------------------------

def toggle_menu():
    """Přepínač stavu menu"""
    if st.session_state['sidebar_state'] == 'collapsed':
        st.session_state['sidebar_state'] = 'expanded'
    else:
        st.session_state['sidebar_state'] = 'collapsed'
    st.rerun()

def render_menu_button():
    """Vykreslí tlačítko >> pro otevření menu, pokud je zavřené"""
    if st.session_state['sidebar_state'] == 'collapsed':
        # Použijeme kontejner, aby to bylo hezky nahoře
        with st.container():
            c1, c2 = st.columns([1, 10])
            with c1:
                if st.button(">> MENU", key="open_menu"):
                    toggle_menu()

def render_sidebar_content():
    """Obsah bočního menu"""
    with st.sidebar:
        # Tlačítko pro zavření <<
        if st.button("<< CLOSE MENU", key="close_menu"):
            toggle_menu()
            
        st.markdown("---")
        st.markdown(f"### USER: {st.session_state.get('username', 'GUEST').upper()}")
        st.markdown("---")
        
        # Navigace
        if st.button("DASHBOARD"): st.session_state['active_tab'] = 'dashboard_home'; st.rerun()
        if st.button("USD OVERVIEW"): st.session_state['active_tab'] = 'usd_overview'; st.rerun() # Přejmenováno
        if st.button("ECONOMIC CALENDAR"): st.session_state['active_tab'] = 'economic_calendar'; st.rerun()
        if st.button("WATCHLIST"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("PROFILE"): st.session_state['active_tab'] = 'profile'; st.rerun()
            
        st.markdown("---")
        
        # LOGOUT
        if st.button("LOGOUT"):
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['page'] = 'landing'
            st.session_state['sidebar_state'] = 'collapsed'
            st.rerun()

# -------------------------
# 6. UI STRÁNKY
# -------------------------

def render_landing():
    st.markdown('<div class="brand-text">> FUNDAMENTICKS_</div>', unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    col_head_1, col_head_2 = st.columns([3,1])
    with col_head_1:
        st.markdown("<h1>SYSTEM STATUS: <span style='color:#00FF00'>ONLINE</span></h1>", unsafe_allow_html=True)
    
    st.write("")
    
    # FEATURES
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="data-box"><h4>[ MACRO_DATA ]</h4><p>Analyze historical seasonality of key currencies.</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="data-box"><h4>[ AI_SCORING ]</h4><p>Real-time sentiment evaluation.</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="data-box"><h4>[ WATCHLIST ]</h4><p>Personalized asset tracking.</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3><center>ACCESS LEVELS</center></h3>", unsafe_allow_html=True)

    # ACCESS LEVELS
    cf, cp = st.columns(2)
    with cf:
        st.markdown("""<div class="data-box" style="text-align:center"><h3>FREE TIER</h3><ul style="list-style-type:none; padding:0; text-align:left;"><li>[x] Only one asset (SPX500)</li><li>[ ] No USD Overview</li></ul></div>""", unsafe_allow_html=True)
        if st.button("GET STARTED (FREE)", key="free_btn"):
            st.session_state['page'] = 'login'
            st.rerun()
            
    with cp:
        st.markdown("""<div class="paid-box" style="text-align:center"><h3 style="color:#00FF00">PAID TIER (ADMIN)</h3><ul style="list-style-type:none; padding:0; text-align:left;"><li>[x] Unlimited assets</li><li>[x] Full USD Overview</li></ul></div>""", unsafe_allow_html=True)
        if st.button("GET STARTED (PAID)", key="paid_btn"):
            st.session_state['page'] = 'login'
            st.rerun()
            
    # Testovací tlačítko (v patičce landing page)
    st.write("")
    if st.button("GO IN (TEST - ADMIN ACCESS)"):
        st.session_state['authentication_status'] = True
        st.session_state['name'] = 'Tester'
        st.session_state['username'] = 'admin'
        st.session_state['page'] = 'dashboard'
        st.session_state['active_tab'] = 'dashboard_home'
        st.rerun()

def render_login_page():
    st.markdown('<div class="brand-text">> FUNDAMENTICKS_</div>', unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div class='data-box'><h3>> AUTHENTICATION</h3></div>", unsafe_allow_html=True)
        name, status, user = authenticator.login('Login', 'main')
        
        if status:
            st.session_state['authentication_status'] = True
            st.session_state['name'] = name
            st.session_state['username'] = user
            st.session_state['page'] = 'dashboard'
            st.rerun()
        elif status is False:
            st.error("ACCESS DENIED")
            
        st.markdown("---")
        if st.button("< BACK TO HOME"):
            st.session_state['page'] = 'landing'
            st.rerun()

def render_dashboard_content():
    # Vykreslit obsah sidebaru
    render_sidebar_content()
    
    # Tlačítko pro otevření menu (pokud je zavřené)
    render_menu_button()
    
    tab = st.session_state['active_tab']
    
    # ---------------------------
    # DASHBOARD HOME
    # ---------------------------
    if tab == 'dashboard_home':
        st.title("> DASHBOARD HOME")
        st.markdown("---")
        st.markdown("#### [ WEEKLY BRIEF ]")
        st.markdown("""
        <div class='data-box'>
        <ul style='list-style-type:none; padding:0;'>
        <li><b>MON:</b> Manufacturing Index (Low Impact)</li>
        <li><b>TUE:</b> Retail Sales (High Impact)</li>
        <li><b>WED:</b> FOMC Meeting (Critical)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### [ USD SEASONALITY PREVIEW ]")
        df = load_seasonality_lines_data()
        if not df.empty:
             # Vykreslení zjednodušeného grafu
             fig = px.line(df, x='Month', y='Return_15Y', title="USD 15-Year Trend")
             fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0')
             st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # USD OVERVIEW (KOMPLETNÍ LOGIKA)
    # ---------------------------
    elif tab == 'usd_overview':
        st.title("> USD OVERVIEW")
        st.markdown("---")
        
        # 1. Načtení dat
        df_events = load_events_from_csv()
        if df_events.empty:
             st.warning("No macro data available.")
        else:
             # Scoring
             df_events["Points"] = df_events.apply(score_event, axis=1)
             df_events["DateDisplay"] = df_events["DateParsed"].dt.strftime("%Y-%m-%d")
             df_scored = df_events[pd.to_numeric(df_events['Actual'], errors='coerce').notna()].copy()
             
             # 2. News Breakdown (Tabulky)
             st.subheader("[ 1. FUNDAMENTAL NEWS BREAKDOWN ]")
             cols = st.columns(2)
             categories = df_events["Category"].unique()
             
             for i, cat in enumerate(categories):
                 cat_df = df_events[df_events["Category"] == cat].copy()
                 display_df = cat_df[["DateDisplay", "Report", "Actual", "Forecast", "Points"]]
                 
                 with cols[i % 2]:
                     st.markdown(f"**{cat}**")
                     st.dataframe(display_df, use_container_width=True)
             
             # 3. Fundamental Evaluation (Score)
             st.subheader("[ 2. FUNDAMENTAL EVALUATION ]")
             total_score = int(df_scored["Points"].sum())
             label = "BULLISH" if total_score >= 2 else ("BEARISH" if total_score <= -2 else "NEUTRAL")
             color = "#00FF00" if label == "BULLISH" else ("red" if label == "BEARISH" else "white")
             
             st.markdown(f"""
             <div class='paid-box' style='text-align:center; border-color:{color} !important;'>
                <h2 style='color:{color}'>TOTAL SCORE: {total_score} ({label})</h2>
             </div>
             """, unsafe_allow_html=True)

        st.markdown("---")

        # 4. Heatmap
        st.subheader("[ 3. USD MONTHLY RETURN HEATMAP ]")
        df_h = load_seasonality_heatmap_data()
        if not df_h.empty:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            piv = df_h.pivot(index='Year', columns='Month', values='Return').reindex(columns=months)
            
            # Custom Hacker Colors (Red/Green on Black)
            # Upravíme škálu aby byla dobře vidět na černém
            custom_colors = [[0.0, 'red'], [0.5, 'black'], [1.0, '#00FF00']]
            
            fig = go.Figure(data=go.Heatmap(
                z=piv.values, x=piv.columns, y=piv.index, 
                colorscale='RdYlGn', # Použijeme standardní, vypadá dobře
                text=piv.values, texttemplate="%{text:.2f}"
            ))
            fig.update_layout(
                plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0', 
                height=600, title="Monthly Returns (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # 5. Seasonality Lines
        st.subheader("[ 4. SEASONALITY TRENDS (15Y / 10Y / 5Y) ]")
        df_l = load_seasonality_lines_data()
        if not df_l.empty:
            df_melt = df_l.melt(id_vars=['Month'], value_vars=['Return_15Y', 'Return_10Y', 'Return_5Y'])
            fig_l = px.line(df_melt, x='Month', y='value', color='variable', markers=True)
            fig_l.update_layout(
                plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0',
                xaxis=dict(showgrid=False, gridcolor='#333'),
                yaxis=dict(showgrid=True, gridcolor='#333'),
                legend=dict(orientation="h", y=1.1)
            )
            st.plotly_chart(fig_l, use_container_width=True)
            
    # ---------------------------
    # OSTATNÍ STRÁNKY
    # ---------------------------
    elif tab == 'economic_calendar':
        st.title("> ECONOMIC CALENDAR")
        st.markdown("---")
        df_m = load_events_from_csv()
        if not df_m.empty:
            st.dataframe(df_m, use_container_width=True)
        else:
            st.info("No data available.")
            
    elif tab == 'watchlist':
        st.title("> WATCHLIST")
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            asset = st.selectbox("SELECT ASSET", ["SPX500", "EURUSD", "GBPUSD", "XAUUSD", "BTCUSD"])
        with col2:
            st.markdown(f"<div class='data-box'><h3>ANALYZING: {asset}</h3></div>", unsafe_allow_html=True)
            st.line_chart([100, 102, 101, 104, 103, 106, 108])

    elif tab == 'profile':
        st.title("> USER PROFILE")
        st.markdown("---")
        st.markdown(f"""
        <div class='data-box'>
        <p><b>USERNAME:</b> {st.session_state['username']}</p>
        <p><b>STATUS:</b> PAID (ADMIN)</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# 7. HLAVNÍ KONTROLER
# -------------------------
if st.session_state.get('authentication_status'):
    render_dashboard_content()
else:
    if st.session_state['page'] == 'landing':
        render_landing()
    elif st.session_state['page'] == 'login':
        render_login_page()
    else:
        st.session_state['page'] = 'landing'
        st.rerun()
