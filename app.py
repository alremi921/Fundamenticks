import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os

# -------------------------
# 1. NASTAVENÍ STRÁNKY A DESIGNU (Vzhled Fundamenticks)
# -------------------------
st.set_page_config(page_title="Fundamenticks", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        /* --- SCHOVÁNÍ PRVKŮ STREAMLITU (Aby to vypadalo profi) --- */
        header[data-testid="stHeader"] { display: none; }
        [data-testid="stToolbar"] { display: none; }
        footer { display: none; }
        .stAppDeployButton { display: none; }

        /* --- DESIGN FUNDAMENTICKS --- */
        
        /* Fixní hlavička nahoře */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #0E1117;
            z-index: 9999;
            padding: 1rem 2rem;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        
        /* Odsazení obsahu od hlavičky */
        .block-container {
            padding-top: 100px !important; 
        }

        /* Hlavní nápisy */
        .brand-title {
            font-size: 4rem;
            font-weight: 900;
            text-align: center;
            letter-spacing: -2px;
            background: -webkit-linear-gradient(90deg, #00C9FF, #92FE9D); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: #888;
            margin-bottom: 3rem;
            font-family: monospace;
        }

        /* Karty funkcí */
        .feature-card {
            background-color: #161b22;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #30363d;
            height: 100%;
            text-align: center;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            border-color: #00C9FF;
            transform: translateY(-5px);
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# 2. NAČÍTÁNÍ DAT (Připojení tvých souborů)
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
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# -------------------------
# 3. PŘIHLÁŠENÍ (Login System)
# -------------------------

names = ['Admin User', 'Free Trader']
usernames = ['admin', 'freetrader']
hashed_passwords = ['$2b$12$R.S4lQd8I/Iq3ZlA5tQ9uOxFp/H32mXJjK/iM0V1n4hR', 
                    '$2b$12$t3n1S7pC2pP7tKjO9XbH9OqT3yGgY7Xw8tW1wG7p8r']

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'fundamenticks_cookie', 'signature_key_fx', cookie_expiry_days=30
)

if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'watchlist'

# -------------------------
# 4. GRAFICKÉ ROZHRANÍ (Co vidíš na obrazovce)
# -------------------------

def render_navbar():
    """Horní menu, které je vždy vidět."""
    c1, c2, c3 = st.columns([2, 5, 1])
    with c1:
        st.markdown("### 📈 Fundamenticks")
    with c3:
        if st.session_state.get('authentication_status'):
            authenticator.logout('Odhlásit', 'main')
        else:
            if st.session_state['page'] == 'landing':
                if st.button("Log In"):
                    st.session_state['page'] = 'login'
                    st.rerun()

def render_landing_page():
    """Úvodní stránka pro návštěvníky."""
    st.markdown("<div class='brand-title'>FUNDAMENTICKS</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'> > DECODE THE MARKET_ </div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-card'><h3>📊 Macro Data</h3>Analýza sezónnosti USD a EUR.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><h3>🧠 AI Scoring</h3>Okamžité vyhodnocení zpráv.</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'><h3>⚡ Live Signals</h3>Automatické obchodní signály.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Vyberte si svůj plán")
    
    cf, cp = st.columns(2)
    with cf:
        st.info("**FREE Verze**")
        st.write("✅ Watchlist: SPX")
        st.write("❌ Currency Dashboard")
        if st.button("Začít ZDARMA"):
            st.session_state['page'] = 'login'
            st.rerun()
    with cp:
        st.error("**PRO Verze**")
        st.write("✅ Všechny měnové páry")
        st.write("✅ Full Dashboard")
        if st.button("Získat PRO"):
            st.session_state['page'] = 'login'
            st.rerun()

def render_dashboard():
    """Hlavní aplikace."""
    tier = 'PAID' if st.session_state["username"] == 'admin' else 'FREE'
    
    with st.sidebar:
        st.title("Fundamenticks")
        st.write(f"User: **{st.session_state['name']}**")
        st.info(f"Tier: **{tier}**")
        st.markdown("---")
        if st.button("Watchlist"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("Currency Hub"): st.session_state['active_tab'] = 'currency'; st.rerun()

    st.title(f"{st.session_state['active_tab'].capitalize()} View")
    
    if st.session_state['active_tab'] == 'watchlist':
        opts = ["SPX"] + (["EURUSD", "XAUUSD"] if tier == 'PAID' else [])
        sel = st.selectbox("Vyber aktivum:", opts)
        
        if tier == 'FREE' and sel != "SPX":
            st.error("Upgrade to PRO required.")
        else:
            df = get_data("lines")
            if not df.empty:
                st.subheader(f"Sezónnost: {sel}")
                df_m = df.melt(id_vars=['Month'], value_vars=['Return_15Y', 'Return_10Y', 'Return_5Y'])
                fig = px.line(df_m, x='Month', y='value', color='variable', markers=True)
                st.plotly_chart(fig, use_container_width=True)

    elif st.session_state['active_tab'] == 'currency':
        if tier == 'FREE':
            st.warning("🔒 Currency Hub je dostupný pouze ve verzi PRO.")
        else:
            st.subheader("USD Heatmap Analysis")
            df_h = get_data("heatmap")
            if not df_h.empty:
                 # Seřazení měsíců
                month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                piv = df_h.pivot(index='Year', columns='Month', values='Return').reindex(columns=month_order)
                
                fig = go.Figure(data=go.Heatmap(
                    z=piv.values, x=piv.columns, y=piv.index, colorscale='RdYlGn', text=piv.values, texttemplate="%{text:.2f}"
                ))
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

# -------------------------
# 5. START APLIKACE
# -------------------------
render_navbar()

if st.session_state['page'] == 'landing':
    render_landing_page()
elif st.session_state['page'] == 'login':
    st.write(""); st.write("")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.subheader("Login to Fundamenticks")
        name, status, user = authenticator.login('Login', 'main')
        if status:
            st.session_state['authentication_status'] = True
            st.session_state['name'] = name
            st.session_state['username'] = user
            st.session_state['page'] = 'dashboard'
            st.rerun()
        elif status is False: st.error('Chyba přihlášení')
        if st.button("Zpět"): st.session_state['page'] = 'landing'; st.rerun()
elif st.session_state['page'] == 'dashboard':
    if st.session_state.get('authentication_status'): render_dashboard()
    else: st.session_state['page'] = 'login'; st.rerun()