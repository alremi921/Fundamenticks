import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os
import time

# -------------------------
# 1. CSS DESIGN (HACKER TERMINAL)
# -------------------------
st.set_page_config(page_title="Fundamenticks", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        /* HLAVNÍ BARVY - ČERNÁ A ZELENÁ */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* SCHOVÁNÍ PRVKŮ STREAMLITU */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        footer {display: none !important;}
        
        /* --- FIXNÍ LIŠTA NAHOŘE --- */
        /* Cílíme na první blok stránky a přibijeme ho nahoru */
        div[data-testid="stVerticalBlock"] > div:first-child {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 999999;
            background-color: #000000;
            border-bottom: 1px solid #333;
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* --- ODSTRČENÍ OBSAHU DOLŮ --- */
        /* Toto je ta oprava - posuneme obsah, aby nezačínal pod lištou */
        .block-container {
            padding-top: 130px !important; /* Dost místa pro lištu */
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* SIDEBAR (LEVÁ LIŠTA PRO MENU) */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #333;
            top: 80px !important; /* Aby nezasahovala do horní lišty */
            height: calc(100vh - 80px) !important;
        }

        /* TEXTY */
        h1, h2, h3, h4, p, div, span, li, ul {
            font-family: 'Courier New', Courier, monospace !important;
            color: #E0E0E0 !important;
        }

        /* LOGO TEXT V LIŠTĚ */
        .brand-text {
            font-size: 24px;
            font-weight: 900;
            color: #E0E0E0;
            letter-spacing: 2px;
            margin-top: 5px;
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

        /* KARTY (BOXÍKY) */
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
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 2. DATA
# -------------------------
FILES = {
    "lines": "dxy_linechart_history_2.csv.txt",
    "heatmap": "dxy_seasonality_heatmap_history_2.csv.txt",
    "macro": "usd_macro_history_2.csv.txt"
}

@st.cache_data
def get_data(file_key):
    path = FILES.get(file_key)
    if path and os.path.exists(path):
        try:
            return pd.read_csv(path, sep=',', decimal='.')
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# -------------------------
# 3. AUTENTIZACE
# -------------------------
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

names = ['SYSTEM ADMIN', 'GUEST USER']
usernames = ['admin', 'guest']
hashed_passwords = [
    '$2b$12$R.S4lQd8I/Iq3ZlA5tQ9uOxFp/H32mXJjK/iM0V1n4hR', 
    '$2b$12$t3n1S7pC2pP7tKjO9XbH9OqT3yGgY7Xw8tW1wG7p8r'
]

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'cookie_v14_final', 'key_v14_final', cookie_expiry_days=1
)

if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'dashboard_home'

# -------------------------
# 4. HORNÍ LIŠTA (NAVBAR)
# -------------------------
def render_navbar():
    """
    Toto je obsah fixní lišty. 
    Díky CSS je tento kontejner přibitý nahoře.
    """
    with st.container():
        c1, c2, c3, c4 = st.columns([4, 2, 1.5, 1.5])
        
        with c1:
            st.markdown('<div class="brand-text">> FUNDAMENTICKS_</div>', unsafe_allow_html=True)
            
        with c3:
            # Tlačítko GO IN (Pro rychlý test) - jen když není přihlášen
            if not st.session_state.get('authentication_status'):
                if st.button("GO IN (TEST)"):
                    st.session_state['authentication_status'] = True
                    st.session_state['name'] = 'Tester'
                    st.session_state['username'] = 'admin'
                    st.session_state['page'] = 'dashboard'
                    st.session_state['active_tab'] = 'dashboard_home'
                    st.rerun()
                    
        with c4:
            # Login / Sign In Tlačítko
            if not st.session_state.get('authentication_status'):
                if st.button("LOGIN / SIGN IN"):
                    st.session_state['page'] = 'login'
                    st.rerun()
            # Pokud je přihlášen, tlačítko tu není, logout je v menu vlevo

# -------------------------
# 5. STRÁNKY
# -------------------------

def render_landing():
    # Obsah už nemusíme posouvat ručně, dělá to CSS (.block-container padding)
    
    col_head_1, col_head_2 = st.columns([3,1])
    with col_head_1:
        st.markdown("<h1>SYSTEM STATUS: <span style='color:#00FF00'>ONLINE</span></h1>", unsafe_allow_html=True)
    
    st.write("")
    
    # FEATURES (S TEXTEM)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="data-box">
            <h4>[ MACRO_DATA ]</h4>
            <p>Analyze historical seasonality of key currencies (USD, EUR) over the last 15 years. 
            Identify months with the highest probability of growth or decline.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="data-box">
            <h4>[ AI_SCORING ]</h4>
            <p>Our algorithm evaluates fundamental news (NFP, CPI, FED) in real-time. 
            Instantly translates complex macroeconomic data into a simple score: Bullish or Bearish.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="data-box">
            <h4>[ WATCHLIST ]</h4>
            <p>Create a personalized list of assets to track. Monitor price action 
            and seasonal trends for specific indices and currency pairs in one dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3><center>ACCESS LEVELS</center></h3>", unsafe_allow_html=True)

    # ACCESS LEVELS
    cf, cp = st.columns(2)
    with cf:
        st.markdown("""
        <div class="data-box" style="text-align:center">
            <h3>FREE TIER</h3>
            <ul style="list-style-type:none; padding:0; text-align:left;">
                <li>[x] Only one asset in watchlist (SPX500)</li>
                <li>[ ] No Currency Overview</li>
                <li>[ ] Limited History Data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("GET STARTED (FREE)", key="free_btn"):
            st.session_state['page'] = 'login'
            st.rerun()
            
    with cp:
        st.markdown("""
        <div class="paid-box" style="text-align:center">
            <h3 style="color:#00FF00">PAID TIER (ADMIN)</h3>
            <ul style="list-style-type:none; padding:0; text-align:left;">
                <li>[x] Unlimited assets in watchlist</li>
                <li>[x] Seasonality Analysis (Full)</li>
                <li>[x] News Sentiment AI</li>
                <li>[x] Currency Overview Hub</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("GET STARTED (PAID)", key="paid_btn"):
            st.session_state['page'] = 'login'
            st.rerun()

def render_login_page():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div class='data-box'><h3>> AUTHENTICATION</h3></div>", unsafe_allow_html=True)
        name, status, user = authenticator.login('Login', 'main')
        
        if status:
            st.session_state['authentication_status'] = True
            st.session_state['name'] = name
            st.session_state['username'] = user
            st.session_state['page'] = 'dashboard'
            st.session_state['active_tab'] = 'dashboard_home'
            st.rerun()
        elif status is False:
            st.error("ACCESS DENIED")
            
        st.markdown("---")
        if st.button("< BACK TO HOME"):
            st.session_state['page'] = 'landing'
            st.rerun()

def render_dashboard_content():
    # BOČNÍ MENU (SIDEBAR)
    with st.sidebar:
        st.markdown(f"## USER: {st.session_state['username'].upper()}")
        st.markdown("---")
        
        # Navigace
        if st.button("DASHBOARD"): st.session_state['active_tab'] = 'dashboard_home'; st.rerun()
        if st.button("CURRENCY OVERVIEW"): st.session_state['active_tab'] = 'currency_overview'; st.rerun()
        if st.button("ECONOMIC CALENDAR"): st.session_state['active_tab'] = 'economic_calendar'; st.rerun()
        if st.button("WATCHLIST"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("PROFILE"): st.session_state['active_tab'] = 'profile'; st.rerun()
            
        st.markdown("---")
        
        # LOGOUT (Natvrdo vymazat session a přesměrovat)
        if st.button("LOGOUT"):
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['page'] = 'landing'
            st.rerun()

    # HLAVNÍ OBSAH DASHBOARDU
    tab = st.session_state['active_tab']
    
    if tab == 'dashboard_home':
        st.markdown("## > DASHBOARD HOME")
        st.markdown("---")
        st.markdown("#### [ USD SEASONALITY PREVIEW ]")
        df = get_data("lines")
        if not df.empty:
             fig = px.line(df, x='Month', y='Return_15Y', title="USD 15-Year Seasonality Trend")
             fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0')
             st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### [ WEEKLY NEWS BRIEF ]")
        st.markdown("""
        <div class='data-box'>
        <ul style='list-style-type:none; padding:0;'>
        <li><b>MON:</b> USD Empire State Manufacturing Index (Low Impact)</li>
        <li><b>TUE:</b> USD Retail Sales m/m (High Impact)</li>
        <li><b>WED:</b> USD FOMC Meeting Minutes (Critical)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    elif tab == 'currency_overview':
        st.markdown("## > CURRENCY OVERVIEW: USD")
        st.markdown("---")
        st.markdown("#### 1. FUNDAMENTAL NEWS BREAKDOWN")
        st.table(pd.DataFrame({
            "Category": ["Inflation", "Labor Market", "Central Bank", "Growth"],
            "Sentiment": ["Bearish", "Bullish", "Neutral", "Bullish"],
            "Last Data": ["CPI 3.1%", "NFP 210k", "Hold 5.5%", "GDP 2.9%"]
        }))
        
        st.markdown("#### 2. FUNDAMENTAL EVALUATION")
        st.markdown("<div class='paid-box' style='text-align:center'><h3>OVERALL SCORE: BULLISH (65/100)</h3></div>", unsafe_allow_html=True)
        
        st.markdown("#### 3. USD MONTHLY RETURN HEATMAP")
        df_h = get_data("heatmap")
        if not df_h.empty:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            piv = df_h.pivot(index='Year', columns='Month', values='Return').reindex(columns=months)
            fig = go.Figure(data=go.Heatmap(
                z=piv.values, x=piv.columns, y=piv.index, colorscale='Electric', text=piv.values, texttemplate="%{text:.1f}"
            ))
            fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0', height=500)
            st.plotly_chart(fig, use_container_width=True)
            
    elif tab == 'economic_calendar':
        st.markdown("## > ECONOMIC CALENDAR")
        st.markdown("---")
        df_m = get_data("macro")
        if not df_m.empty:
            st.dataframe(df_m, use_container_width=True)
        else:
            st.info("Data synchronization pending...")
            
    elif tab == 'watchlist':
        st.markdown("## > WATCHLIST")
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            asset = st.selectbox("SELECT ASSET", ["SPX500", "EURUSD", "GBPUSD", "XAUUSD", "BTCUSD"])
        with col2:
            st.markdown(f"<div class='data-box'><h3>ANALYZING: {asset}</h3></div>", unsafe_allow_html=True)
            # Simulace grafu
            chart_data = pd.DataFrame(
                {'Price': [100, 102, 101, 105, 104, 108, 107]},
                index=pd.date_range(start='2024-01-01', periods=7)
            )
            st.line_chart(chart_data)

    elif tab == 'profile':
        st.markdown("## > USER PROFILE")
        st.markdown("---")
        st.markdown(f"""
        <div class='data-box'>
        <p><b>USERNAME:</b> {st.session_state['username']}</p>
        <p><b>STATUS:</b> PAID (ADMIN)</p>
        <p><b>API KEY:</b> 8f92-x921-8821-xxxx</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# 6. HLAVNÍ KONTROLER
# -------------------------
# Vykreslit lištu (bude nahoře díky CSS)
render_navbar()

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
