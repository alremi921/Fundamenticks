import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os

# -------------------------
# 1. DESIGN "TERMINÁL" (CSS)
# -------------------------
st.set_page_config(page_title="Fundamenticks", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        /* Vynucení tmavého režimu a strojového písma všude */
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* SCHOVÁNÍ PRVKŮ STREAMLITU (Agresivní metoda pro mobil) */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        footer {display: none !important;}
        .stAppDeployButton {display: none !important;}
        .viewerBadge_container__1QSob {display: none !important;}
        
        /* FIXNÍ MENU NAHOŘE */
        .header-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #000000;
            border-bottom: 1px solid #FFFFFF;
            padding: 15px 0;
            z-index: 99999;
            text-align: center;
        }
        
        /* Aby obsah nebyl schovaný pod menu */
        .block-container {
            padding-top: 100px !important;
        }

        /* STYLOVÁNÍ TEXTŮ - Vše na střed, bílé, strohé */
        h1, h2, h3, h4, p, div {
            text-align: center !important;
            font-family: 'Courier New', Courier, monospace !important;
            color: #FFFFFF !important;
        }
        
        /* Tlačítka jako v příkazové řádce */
        .stButton>button {
            background-color: #000000;
            color: #FFFFFF;
            border: 1px solid #FFFFFF;
            border-radius: 0px; /* Žádné kulaté rohy */
            font-family: 'Courier New', Courier, monospace;
            text-transform: uppercase;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #FFFFFF;
            color: #000000;
        }
        
        /* Karty bez stínů, jen rámeček */
        .feature-box {
            border: 1px solid #FFFFFF;
            padding: 20px;
            margin: 10px 0;
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
# 3. LOGIN SYSTÉM (Admin má vše zdarma)
# -------------------------

names = ['SYSTEM ADMIN', 'GUEST USER']
usernames = ['admin', 'guest']
# Hesla: 
# admin -> 'password123' (Toto je tvůj master účet)
# guest -> 'guest123'
hashed_passwords = ['$2b$12$R.S4lQd8I/Iq3ZlA5tQ9uOxFp/H32mXJjK/iM0V1n4hR', 
                    '$2b$12$t3n1S7pC2pP7tKjO9XbH9OqT3yGgY7Xw8tW1wG7p8r']

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'cookie_fundamenticks_v2', 'key_signature_xx', cookie_expiry_days=30
)

# Inicializace paměti
if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'watchlist'

# -------------------------
# 4. PRVKY ROZHRANÍ
# -------------------------

def render_header():
    """Horní lišta - napevno přibitá"""
    # Používáme HTML přímo, aby to bylo přesně podle tvého designu
    st.markdown("""
        <div class="header-container">
            <span style="font-size: 24px; font-weight: bold;">> FUNDAMENTICKS_</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Tlačítka pro odhlášení/přihlášení pod lištou (aby fungovala logika Streamlitu)
    # Musíme je trochu nastylovat, aby byly vidět
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.session_state.get('authentication_status'):
            authenticator.logout('LOGOUT', 'main')
        else:
            if st.session_state['page'] == 'landing':
                if st.button("LOGIN / START"):
                    st.session_state['page'] = 'login'
                    st.rerun()

def render_landing():
    st.write("") # Mezera
    st.write("") 
    st.markdown("<h1>SYSTEM: ONLINE</h1>", unsafe_allow_html=True)
    st.markdown("<p>DECODING MARKET DATA...</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-box"><h4>[ MACRO_DATA ]</h4>SEASONALITY ANALYSIS<br>USD / EUR / GBP</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-box"><h4>[ AI_CORE ]</h4>NEWS SENTIMENT<br>REAL-TIME SCORING</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-box"><h4>[ SIGNALS ]</h4>ALGORITHMIC OUTPUT<br>HIGH PROBABILITY</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("<h3>SELECT ACCESS LEVEL</h3>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="feature-box">ACCESS: FREE<br>TARGET: SPX500</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="feature-box">ACCESS: PRO<br>TARGET: ALL ASSETS</div>', unsafe_allow_html=True)

def render_app():
    # Tady je ten trik: Pokud jsi 'admin', jsi automaticky 'PAID'
    user_status = 'PAID' if st.session_state["username"] == 'admin' else 'FREE'
    
    # Boční menu (Sidebar)
    with st.sidebar:
        st.write(f"USER: {st.session_state['username'].upper()}")
        st.write(f"STATUS: {user_status}")
        st.markdown("---")
        if st.button("> WATCHLIST"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("> CURRENCY HUB"): st.session_state['active_tab'] = 'currency'; st.rerun()

    # Hlavní obsah
    st.markdown(f"<h2>MODULE: {st.session_state['active_tab'].upper()}</h2>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state['active_tab'] == 'watchlist':
        assets = ["SPX500"]
        if user_status == 'PAID':
            assets.extend(["EURUSD", "XAUUSD", "BTCUSD"])
            
        choice = st.selectbox("SELECT TARGET:", assets)
        
        # Ochrana pro FREE uživatele (pokud by se pokusili hacknout výběr)
        if user_status == 'FREE' and choice != "SPX500":
             st.error("ACCESS DENIED. UPGRADE REQUIRED.")
        else:
            st.write(f"LOADING DATA FOR: {choice}...")
            df = get_data("lines")
            if not df.empty:
                df_m = df.melt(id_vars=['Month'], value_vars=['Return_15Y', 'Return_10Y', 'Return_5Y'])
                # Grafy přizpůsobené tmavému režimu
                fig = px.line(df_m, x='Month', y='value', color='variable')
                fig.update_layout(
                    plot_bgcolor='black', paper_bgcolor='black', font_color='white',
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#333')
                )
                st.plotly_chart(fig, use_container_width=True)

    elif st.session_state['active_tab'] == 'currency':
        if user_status == 'FREE':
            st.error("ERROR: MODULE LOCKED. PERMISSION DENIED.")
            st.markdown("<div style='border:1px solid red; padding:10px; color:red;'>UNLOCK WITH PRO KEY</div>", unsafe_allow_html=True)
        else:
            st.write("INITIATING HEATMAP SEQUENCE...")
            df = get_data("heatmap")
            if not df.empty:
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                piv = df.pivot(index='Year', columns='Month', values='Return').reindex(columns=months)
                
                fig = go.Figure(data=go.Heatmap(
                    z=piv.values, x=piv.columns, y=piv.index, colorscale='gray', # Černo-bílá škála (nebo jiná)
                    text=piv.values, texttemplate="%{text:.1f}"
                ))
                fig.update_layout(
                    plot_bgcolor='black', paper_bgcolor='black', font_color='white', height=600
                )
                st.plotly_chart(fig, use_container_width=True)

# -------------------------
# 5. START SYSTEM
# -------------------------
render_header()

if st.session_state['page'] == 'landing':
    render_landing()
elif st.session_state['page'] == 'login':
    st.write(""); st.write("")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h3>> AUTHENTICATION</h3>", unsafe_allow_html=True)
        name, status, user = authenticator.login('Login', 'main')
        if status:
            st.session_state['authentication_status'] = True
            st.session_state['name'] = name
            st.session_state['username'] = user
            st.session_state['page'] = 'dashboard'
            st.rerun()
        elif status is False: st.error("ACCESS DENIED")
        
        st.markdown("---")
        if st.button("< BACK"): st.session_state['page'] = 'landing'; st.rerun()

elif st.session_state['page'] == 'dashboard':
    if st.session_state.get('authentication_status'): render_app()
    else: st.session_state['page'] = 'login'; st.rerun()
