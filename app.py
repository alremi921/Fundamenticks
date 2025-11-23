import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os

# -------------------------
# 1. KONFIGURACE A DESIGN
# -------------------------
st.set_page_config(page_title="Fundamenticks", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        /* HLAVNÍ STYL (Černá a Zelená) */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* SCHOVÁNÍ PRVKŮ STREAMLITU */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        footer {display: none !important;}
        
        /* OPRAVA ROZLOŽENÍ */
        .block-container {
            padding-top: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* STYL BOČNÍ LIŠTY (SIDEBAR) */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #333;
        }
        
        /* TEXTY */
        h1, h2, h3, h4, p, div, span, li, ul {
            font-family: 'Courier New', Courier, monospace !important;
            color: #E0E0E0 !important;
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

        /* AKTIVNÍ TLAČÍTKO V MENU (Simulace) */
        /* Toto je složitější v CSS, řešíme to logikou Pythonu */

        /* BOXÍKY DATA */
        .data-box {
            border: 1px solid #333;
            background-color: #0a0a0a;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .green-border {
            border: 1px solid #00FF00 !important;
        }

        /* TABULKY */
        div[data-testid="stDataFrame"] {
            border: 1px solid #333;
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
    'cookie_v12', 'key_v12', cookie_expiry_days=1
)

# Inicializace Session State
if 'page' not in st.session_state: st.session_state['page'] = 'landing'
# Zde sledujeme, na které podstránce v dashboardu jsme (defaultně Dashboard)
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'dashboard_home'

# -------------------------
# 4. STRÁNKY A KOMPONENTY
# -------------------------

def render_navbar_landing():
    """Lišta pouze pro Landing Page"""
    with st.container():
        c1, c2, c3, c4 = st.columns([4, 2, 1.5, 1.5])
        with c1:
            st.markdown('<h3 style="margin:0; padding-top:5px;">> FUNDAMENTICKS_</h3>', unsafe_allow_html=True)
        with c3:
            # GO IN BUTTON (Test)
            if st.button("GO IN (TEST)"):
                st.session_state['authentication_status'] = True
                st.session_state['name'] = 'Tester'
                st.session_state['username'] = 'admin'
                st.session_state['page'] = 'dashboard'
                st.session_state['active_tab'] = 'dashboard_home' # Reset na home
                st.rerun()
        with c4:
            if st.button("LOGIN / SIGN IN"):
                st.session_state['page'] = 'login'
                st.rerun()
        st.markdown("---")

def render_landing():
    render_navbar_landing()
    st.write("")
    
    c_status, c_empty = st.columns([1, 3])
    with c_status:
        st.markdown("SYSTEM STATUS: <span style='color:#00FF00'>ONLINE</span>", unsafe_allow_html=True)
    
    st.write("")
    
    # FEATURES
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="data-box"><h4>[ MACRO_DATA ]</h4><p>Seasonality Analysis.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="data-box"><h4>[ AI_SCORING ]</h4><p>Real-time sentiment.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="data-box"><h4>[ WATCHLIST ]</h4><p>Asset tracking.</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3><center>ACCESS LEVELS</center></h3>", unsafe_allow_html=True)

    cf, cp = st.columns(2)
    with cf:
        st.markdown('<div class="data-box" style="text-align:center"><h3>FREE TIER</h3><p>Limited Access</p></div>', unsafe_allow_html=True)
        if st.button("GET STARTED (FREE)"):
            st.session_state['page'] = 'login'
            st.rerun()
    with cp:
        st.markdown('<div class="data-box green-border" style="text-align:center"><h3 style="color:#00FF00">PAID TIER</h3><p>Full Access</p></div>', unsafe_allow_html=True)
        if st.button("GET STARTED (PAID)"):
            st.session_state['page'] = 'login'
            st.rerun()

def render_login_page():
    st.write("")
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
            st.session_state['active_tab'] = 'dashboard_home'
            st.rerun()
        elif status is False:
            st.error("ACCESS DENIED")
            
        st.markdown("---")
        if st.button("< BACK TO HOME"):
            st.session_state['page'] = 'landing'
            st.rerun()

# -------------------------
# 5. HLAVNÍ DASHBOARD (PLACENÁ SEKCE)
# -------------------------

def render_sidebar_menu():
    """Boční navigace pro přihlášené uživatele"""
    with st.sidebar:
        st.markdown(f"## USER: {st.session_state['username'].upper()}")
        st.markdown("---")
        
        # NAVIGACE - Tlačítka mění 'active_tab'
        if st.button("DASHBOARD"): 
            st.session_state['active_tab'] = 'dashboard_home'
            st.rerun()
            
        if st.button("CURRENCY OVERVIEW"): 
            st.session_state['active_tab'] = 'currency_overview'
            st.rerun()
            
        if st.button("ECONOMIC CALENDAR"): 
            st.session_state['active_tab'] = 'economic_calendar'
            st.rerun()
            
        if st.button("WATCHLIST"): 
            st.session_state['active_tab'] = 'watchlist'
            st.rerun()
            
        if st.button("PROFILE"): 
            st.session_state['active_tab'] = 'profile'
            st.rerun()
            
        st.markdown("---")
        
        # LOGOUT LOGIKA
        # Authenticator logout sám o sobě jen vymaže cookie, my musíme přesměrovat
        authenticator.logout('LOGOUT', 'sidebar')
        if st.session_state['authentication_status'] == False:
            st.session_state['page'] = 'landing'
            st.rerun()

def render_dashboard_content():
    # 1. Zobrazit Menu
    render_sidebar_menu()
    
    # 2. Zobrazit Obsah podle toho, na co klikl
    tab = st.session_state['active_tab']
    
    if tab == 'dashboard_home':
        st.markdown("## > DASHBOARD HOME")
        st.markdown("---")
        
        # A) Sezónnost Dolaru (Zjednodušená)
        st.markdown("#### [ USD SEASONALITY PREVIEW ]")
        df = get_data("lines")
        if not df.empty:
             fig = px.line(df, x='Month', y='Return_15Y', title="USD 15-Year Seasonality Trend")
             fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0')
             st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data loading...")

        # B) Zprávy tento týden (Preview)
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
        
        # 1. Fundamental News Breakdown
        st.markdown("#### 1. FUNDAMENTAL NEWS BREAKDOWN")
        st.table(pd.DataFrame({
            "Category": ["Inflation", "Labor Market", "Central Bank", "Growth"],
            "Sentiment": ["Bearish", "Bullish", "Neutral", "Bullish"],
            "Last Data": ["CPI 3.1%", "NFP 210k", "Hold 5.5%", "GDP 2.9%"]
        }))
        
        # 2. Fundamental Evaluation
        st.markdown("#### 2. FUNDAMENTAL EVALUATION")
        st.markdown("<div class='data-box green-border' style='text-align:center'><h3>OVERALL SCORE: BULLISH (65/100)</h3></div>", unsafe_allow_html=True)
        
        # 3. Heatmap
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
        
        # Načteme makro data
        df_m = get_data("macro")
        if not df_m.empty:
            st.dataframe(df_m, use_container_width=True)
        else:
            st.info("Calendar data synchronization pending...")
            
    elif tab == 'watchlist':
        st.markdown("## > WATCHLIST")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            asset = st.selectbox("SELECT ASSET", ["SPX500", "EURUSD", "GBPUSD", "XAUUSD", "BTCUSD"])
        
        with col2:
            st.markdown(f"<div class='data-box'><h3>ANALYZING: {asset}</h3></div>", unsafe_allow_html=True)
            # Zde by byl graf aktiva
            st.line_chart([1, 2, 3, 2, 4, 5, 4, 6, 7])

    elif tab == 'profile':
        st.markdown("## > USER PROFILE")
        st.markdown("---")
        st.markdown(f"""
        <div class='data-box'>
        <p><b>USERNAME:</b> {st.session_state['username']}</p>
        <p><b>STATUS:</b> PAID (ADMIN)</p>
        <p><b>MEMBER SINCE:</b> NOV 2025</p>
        <p><b>API KEY:</b> ******************</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# 6. KONTROLER APLIKACE
# -------------------------

if st.session_state['page'] == 'landing':
    render_landing()

elif st.session_state['page'] == 'login':
    render_login_page()

elif st.session_state['page'] == 'dashboard':
    if st.session_state.get('authentication_status'):
        render_dashboard_content()
    else:
        # Pokud není přihlášen, vyhodit na landing
        st.session_state['page'] = 'landing'
        st.rerun()
