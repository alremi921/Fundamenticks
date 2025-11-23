import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os

# -------------------------
# 1. DESIGN "HACKER TERMINAL" (Fixed Layout)
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
        
        /* 2. SCHOVÁNÍ PRVKŮ STREAMLITU */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        footer {display: none !important;}
        .stAppDeployButton {display: none !important;}
        
        /* 3. OPRAVA LIŠTY (FIXNÍ POZICE) */
        /* Tímto cílíme na první řádek s logem a tlačítkem */
        div[data-testid="stHorizontalBlock"]:nth-of-type(1) {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #000000;
            z-index: 999999; /* Aby byla vždy nahoře */
            padding: 15px 30px;
            border-bottom: 1px solid #333;
            height: 80px; /* Pevná výška lišty */
            display: flex;
            align-items: center;
        }
        
        /* 4. ODSTRČENÍ OBSAHU (ABY NEBYL POD LIŠTOU) */
        /* Toto je to nejdůležitější - posune vše dolů */
        .block-container {
            padding-top: 120px !important; 
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* 5. STYLOVÁNÍ TEXTŮ */
        h1, h2, h3, h4, p, div, span, li, ul {
            font-family: 'Courier New', Courier, monospace !important;
            color: #E0E0E0 !important;
        }

        /* 6. LOGO (TEXTOVÉ) */
        .brand-text {
            font-size: 26px;
            font-weight: 900;
            color: #E0E0E0;
            letter-spacing: 2px;
            margin: 0;
            padding: 0;
            line-height: 1.5;
        }

        /* 7. TLAČÍTKA (ZELENÝ RÁMEČEK) */
        .stButton > button {
            background-color: #000000 !important;
            color: #00FF00 !important;
            border: 1px solid #00FF00 !important;
            border-radius: 0px !important;
            font-family: 'Courier New', Courier, monospace !important;
            text-transform: uppercase;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: #00FF00 !important;
            color: #000000 !important;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.8);
        }

        /* 8. KARTY (BOXÍKY) */
        .paid-box {
            border: 1px solid #00FF00 !important;
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

        /* 9. INPUTY */
        input {
            background-color: #111 !important;
            color: white !important;
            border: 1px solid #333 !important;
        }
        
        /* Zarovnání tlačítka v liště doprava */
        div[data-testid="column"]:nth-of-type(2) {
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 2. DATA
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

# Cookie v11 (Nový reset)
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'fundamenticks_cookie_v11', 'random_key_v11', cookie_expiry_days=1
)

if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'watchlist'

# -------------------------
# 4. UI FUNKCE
# -------------------------

def render_navbar():
    """
    Vykreslí horní lištu.
    Díky CSS (nth-of-type(1)) bude tento první 'st.columns' blok přilepený nahoře.
    """
    # Rozložení: Logo vlevo (velký sloupec), Tlačítko vpravo (malý sloupec)
    c1, c2 = st.columns([7, 2])
    
    with c1:
        # Prostý text, ne tlačítko
        st.markdown('<p class="brand-text">> FUNDAMENTICKS_</p>', unsafe_allow_html=True)
        
    with c2:
        # Tlačítko Login/Logout
        if st.session_state.get('authentication_status'):
             if st.button("LOGOUT", key="nav_logout"):
                 authenticator.logout('LOGOUT', 'main')
        else:
            if st.button("LOGIN / START SYSTEM", key="nav_login"):
                st.session_state['page'] = 'login'
                st.rerun()

def render_landing():
    # Díky paddingu v CSS už nepotřebujeme 'st.write("")' pro odskok
    
    col_head_1, col_head_2 = st.columns([3,1])
    with col_head_1:
        st.markdown("<h1>SYSTEM STATUS: <span style='color:#00FF00'>ONLINE</span></h1>", unsafe_allow_html=True)

    # Žádná čára zde

    st.write("")
    
    # FEATURES
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

    col_free, col_paid = st.columns(2)
    
    with col_free:
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
        # Tlačítko pod boxem
        if st.button("GET STARTED (FREE)", key="btn_free"):
            st.session_state['page'] = 'login'
            st.rerun()
        
    with col_paid:
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
        # Tlačítko pod boxem
        if st.button("GET STARTED (PAID)", key="btn_paid"):
            st.session_state['page'] = 'login'
            st.rerun()

def render_login_page():
    # Odskok kvůli liště řeší CSS, ale pro jistotu malá mezera pro vizuál
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
    
    with st.sidebar:
        st.markdown(f"### USER: {st.session_state['username'].upper()}")
        st.markdown(f"### TIER: <span style='color:{'#00FF00' if user_status=='PAID' else 'white'}'>{user_status}</span>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("> WATCHLIST"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("> CURRENCY HUB"): st.session_state['active_tab'] = 'currency'; st.rerun()
        st.markdown("---")
        # Logout v sidebaru
        authenticator.logout('LOGOUT', 'main')

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
# Vykreslíme lištu jako první věc. 
# Díky CSS se 'přilepí' nahoru.
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
