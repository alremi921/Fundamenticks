import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os

# -------------------------
# 1. DESIGN "TERMINAL V7" (STABLE & GREEN)
# -------------------------
st.set_page_config(page_title="Fundamenticks", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        /* 1. ZÁKLADNÍ MATRIX STYL */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* 2. SCHOVÁNÍ VĚCÍ OD STREAMLITU */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        footer {display: none !important;}
        .stAppDeployButton {display: none !important;}
        
        /* 3. LEPÍCÍ LIŠTA (Sticky Header) - BEZPEČNÁ METODA */
        /* Toto zaručí, že horní tlačítka zůstanou nahoře, ale nepřekryjí obsah */
        div[data-testid="stVerticalBlock"] > div:first-child {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: #000000;
            padding-top: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }

        /* 4. TEXTY */
        h1, h2, h3, h4, p, div, span, li, ul {
            font-family: 'Courier New', Courier, monospace !important;
            color: #E0E0E0 !important;
        }

        /* 5. TLAČÍTKA - HLAVNÍ DESIGN (ZELENÝ RÁMEČEK) */
        /* Platí pro Login, Get Started i Logo */
        .stButton > button {
            background-color: #000000 !important;
            color: #00FF00 !important;
            border: 1px solid #00FF00 !important;  /* ZELENÝ RÁMEČEK */
            border-radius: 0px !important;
            font-family: 'Courier New', Courier, monospace !important;
            text-transform: uppercase;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        /* EFEKT PŘI NAJETÍ MYŠÍ (VÝPLŇ) */
        .stButton > button:hover {
            background-color: #00FF00 !important;
            color: #000000 !important;
            box-shadow: 0 0 10px #00FF00;
        }
        
        /* 6. SPECIÁLNÍ ÚPRAVA PRO LOGO (Aby vypadalo víc jako text vlevo) */
        /* Cílíme na první tlačítko na stránce (Logo) */
        div[data-testid="column"]:nth-of-type(1) .stButton > button {
            border: none !important; 
            text-align: left;
            font-size: 20px;
            background-color: transparent !important;
            padding-left: 0;
        }
        div[data-testid="column"]:nth-of-type(1) .stButton > button:hover {
            background-color: transparent !important;
            color: #FFFFFF !important;
            box-shadow: none !important;
        }

        /* 7. KARTY (BOXÍKY) */
        .paid-box {
            border: 1px solid #00FF00 !important; /* Zelený box pro PAID */
            padding: 20px;
            margin-bottom: 10px;
            background-color: #0a0a0a;
            box-shadow: 0 0 5px rgba(0, 255, 0, 0.1);
            height: 100%;
        }
        
        .feature-box {
            border: 1px solid #333;
            padding: 20px;
            margin-bottom: 10px;
            background-color: #0a0a0a;
            height: 100%;
        }

        /* 8. VSTUPNÍ POLE (INPUTY) */
        input {
            background-color: #111 !important;
            color: white !important;
            border: 1px solid #333 !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 2. NAČÍTÁNÍ DAT
# -------------------------
FILES = {
    "lines": "dxy_linechart_history_2.csv.txt",
    "heatmap": "dxy_seasonality_heatmap_history_2.csv.txt"
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
# 3. PŘIHLAŠOVÁNÍ (AUTHENTICATOR)
# -------------------------
# Inicializace session state, aby aplikace nepadala
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

names = ['SYSTEM ADMIN', 'GUEST USER']
usernames = ['admin', 'guest']
hashed_passwords = [
    '$2b$12$R.S4lQd8I/Iq3ZlA5tQ9uOxFp/H32mXJjK/iM0V1n4hR', # password123
    '$2b$12$t3n1S7pC2pP7tKjO9XbH9OqT3yGgY7Xw8tW1wG7p8r'  # guest123
]

# Změna názvu cookie na 'v9' (Resetuje problémy s přihlášením)
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'fundamenticks_cookie_v9', 'random_key_v9', cookie_expiry_days=1
)

# Navigace
if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'watchlist'

# -------------------------
# 4. VYKRESLOVACÍ FUNKCE
# -------------------------

def render_navbar():
    """Horní lišta (Sticky Header)"""
    # Vytvoříme sloupce přímo pro tlačítka
    c1, c2, c3 = st.columns([3, 5, 2])
    
    with c1:
        # Logo Tlačítko (Funguje jako Domů)
        if st.button("> FUNDAMENTICKS_", key="nav_logo"):
            st.session_state['page'] = 'landing'
            st.rerun()
            
    with c3:
        # Login / Logout tlačítko
        if st.session_state.get('authentication_status'):
             if st.button("LOGOUT"):
                 authenticator.logout('LOGOUT', 'main')
        else:
            if st.button("LOGIN / START SYSTEM", key="nav_login"):
                st.session_state['page'] = 'login'
                st.rerun()

def render_landing():
    st.write("")
    col_head_1, col_head_2 = st.columns([3,1])
    with col_head_1:
        st.markdown("<h1>SYSTEM STATUS: <span style='color:#00FF00'>ONLINE</span></h1>", unsafe_allow_html=True)

    st.markdown("---")
    
    # VLASTNOSTI (FEATURES)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="feature-box">
            <h4>[ MACRO_DATA ]</h4>
            <p>Analyze historical seasonality of key currencies (USD, EUR) over the last 15 years. 
            Identify months with the highest probability of growth or decline.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="feature-box">
            <h4>[ AI_SCORING ]</h4>
            <p>Our algorithm evaluates fundamental news (NFP, CPI, FED) in real-time. 
            Instantly translates complex macroeconomic data into a simple score: Bullish or Bearish.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="feature-box">
            <h4>[ WATCHLIST ]</h4>
            <p>Create a personalized list of assets to track. Monitor price action 
            and seasonal trends for specific indices and currency pairs in one dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3><center>ACCESS LEVELS</center></h3>", unsafe_allow_html=True)

    # Sekce Access Levels s tlačítky pod sebou
    col_free, col_paid = st.columns(2)
    
    with col_free:
        # Box
        st.markdown("""
        <div class="feature-box" style="text-align:center">
            <h3 style="color:white">TIER: FREE</h3>
            <ul style="list-style-type:none; padding:0; text-align:left;">
                <li>[x] Only one asset in watchlist (SPX500)</li>
                <li>[ ] No Currency Overview</li>
                <li>[ ] Limited History Data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        # Tlačítko pod boxem (Zelený rámeček díky CSS)
        if st.button("GET STARTED (FREE)", key="btn_free"):
            st.session_state['page'] = 'login'
            st.rerun()
        
    with col_paid:
        # Box (Zelený rámeček)
        st.markdown("""
        <div class="paid-box" style="text-align:center">
            <h3 style="color:#00FF00">TIER: PAID (ADMIN)</h3>
            <ul style="list-style-type:none; padding:0; text-align:left;">
                <li>[x] Unlimited assets in watchlist</li>
                <li>[x] Seasonality Analysis (Full)</li>
                <li>[x] News Sentiment AI</li>
                <li>[x] Currency Overview Hub</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        # Tlačítko pod boxem (Zelený rámeček díky CSS)
        if st.button("GET STARTED (PAID)", key="btn_paid"):
            st.session_state['page'] = 'login'
            st.rerun()

def render_login_page():
    st.write("")
    st.write("")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div class='feature-box'><h3>> AUTHENTICATION REQUIRED</h3></div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])
        
        with tab1:
            try:
                name, status, user = authenticator.login('Login', 'main')
            except Exception:
                status = False

            if status:
                st.session_state['authentication_status'] = True
                st.session_state['name'] = name
                st.session_state['username'] = user
                st.session_state['page'] = 'dashboard'
                st.rerun()
            elif status is False:
                st.error("ACCESS DENIED: INVALID CREDENTIALS")
                
        with tab2:
            st.warning("REGISTRATION PROTOCOL: DISABLED")
            st.markdown("For DEMO access:")
            st.code("User: admin\nPass: password123")
            
        st.markdown("---")
        if st.button("< RETURN TO BASE"): 
            st.session_state['page'] = 'landing'
            st.rerun()

def render_dashboard():
    user_status = 'PAID' if st.session_state["username"] == 'admin' else 'FREE'
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"### USER: {st.session_state['username'].upper()}")
        st.markdown(f"### TIER: <span style='color:{'#00FF00' if user_status=='PAID' else 'white'}'>{user_status}</span>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("> WATCHLIST"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("> CURRENCY HUB"): st.session_state['active_tab'] = 'currency'; st.rerun()
        st.markdown("---")
        # Logout handled by library logic
        authenticator.logout('LOGOUT', 'main')

    # MAIN CONTENT
    st.markdown(f"<h2>MODULE: {st.session_state['active_tab'].upper()}</h2>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state['active_tab'] == 'watchlist':
        assets = ["SPX500"]
        if user_status == 'PAID':
            assets.extend(["EURUSD", "XAUUSD", "BTCUSD"])
            
        choice = st.selectbox("SELECT TARGET:", assets)
        
        if user_status == 'FREE' and choice != "SPX500":
             st.error("ACCESS DENIED. UPGRADE TO PAID TIER.")
        else:
            st.success(f"DATA LINK ESTABLISHED: {choice}")
            df = get_data("lines")
            if not df.empty:
                st.markdown("### SEASONALITY FORECAST")
                df_m = df.melt(id_vars=['Month'], value_vars=['Return_15Y', 'Return_10Y', 'Return_5Y'])
                fig = px.line(df_m, x='Month', y='value', color='variable', markers=True)
                fig.update_layout(
                    plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0',
                    xaxis=dict(showgrid=False, gridcolor='#333'),
                    yaxis=dict(showgrid=True, gridcolor='#333'),
                    legend=dict(orientation="h", y=1.1)
                )
                st.plotly_chart(fig, use_container_width=True)

    elif st.session_state['active_tab'] == 'currency':
        if user_status == 'FREE':
            st.error("SECURITY ALERT: MODULE LOCKED")
            st.markdown("""
                <div style="border: 1px dashed red; padding: 20px; text-align: center;">
                    <h3 style="color:red">RESTRICTED AREA</h3>
                    <p>Currency Overview is available for PAID users only.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("ACCESS GRANTED: FULL MARKET OVERVIEW")
            df = get_data("heatmap")
            if not df.empty:
                st.markdown("### > MONTHLY RETURN HEATMAP (USD)")
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                piv = df.pivot(index='Year', columns='Month', values='Return').reindex(columns=months)
                fig = go.Figure(data=go.Heatmap(
                    z=piv.values, x=piv.columns, y=piv.index, colorscale='Electric', text=piv.values, texttemplate="%{text:.1f}"
                ))
                fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0', height=600)
                st.plotly_chart(fig, use_container_width=True)

# -------------------------
# 5. HLAVNÍ KONTROLER
# -------------------------
# Vykreslit lištu na každé stránce
render_navbar()

if st.session_state.get('authentication_status'):
    render_dashboard()
else:
    if st.session_state['page'] == 'landing':
        render_landing()
    elif st.session_state['page'] == 'login':
        render_login_page()
    else:
        st.session_state['page'] = 'landing'
        st.rerun()
