import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import os

# -------------------------
# 1. DESIGN "TERMINAL V4" (Fixed Borders & Login)
# -------------------------
st.set_page_config(page_title="Fundamenticks", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        /* BASIC TERMINAL STYLE */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* HIDE STREAMLIT UI */
        header {visibility: hidden !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        footer {display: none !important;}
        .stAppDeployButton {display: none !important;}
        
        /* FIXED NAVBAR */
        .header-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #000000;
            border-bottom: 1px solid #333;
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
        }
        
        /* CONTENT PADDING */
        .block-container {
            padding-top: 90px !important; 
        }

        /* TEXT STYLING */
        h1, h2, h3, h4, p, div, span, li, ul {
            font-family: 'Courier New', Courier, monospace !important;
            color: #E0E0E0 !important;
        }
        
        /* BUTTONS - GREEN HOVER EFFECT (KEPT) */
        .stButton>button {
            background-color: #000000;
            color: #00FF00;
            border: 1px solid #00FF00;
            border-radius: 0px;
            font-family: 'Courier New', Courier, monospace;
            text-transform: uppercase;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #00FF00;
            color: #000000;
            box-shadow: 0 0 10px #00FF00;
        }
        
        /* BOXES - NO HOVER EFFECT ANYMORE */
        .feature-box {
            border: 1px solid #333;
            padding: 20px;
            margin-bottom: 10px;
            background-color: #0a0a0a;
            height: 100%;
        }
        
        /* SPECIAL CLASS FOR PAID TIER (ALWAYS GREEN) */
        .paid-box {
            border: 1px solid #00FF00 !important;
            padding: 20px;
            margin-bottom: 10px;
            background-color: #0a0a0a;
            box-shadow: 0 0 5px rgba(0, 255, 0, 0.1);
        }
        
        /* NAVBAR LOGO */
        .nav-logo {
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF !important;
            letter-spacing: 2px;
        }

        /* INPUT FIELDS */
        input {
            background-color: #111 !important;
            color: white !important;
            border: 1px solid #333 !important;
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
# 3. AUTHENTICATION & SESSION
# -------------------------
# Fixing the login memory issue by checking session state explicitly

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

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'fundamenticks_cookie_v5', 'random_key_v5', cookie_expiry_days=0
)

# Navigation State
if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'active_tab' not in st.session_state: st.session_state['active_tab'] = 'watchlist'

# -------------------------
# 4. RENDER FUNCTIONS
# -------------------------

def render_navbar():
    """Fixed Top Bar"""
    st.markdown("""
        <div class="header-container">
            <div class="nav-logo">> FUNDAMENTICKS_</div>
            <div></div>
        </div>
    """, unsafe_allow_html=True)

def render_landing():
    # Header Status
    st.write("")
    col_head_1, col_head_2 = st.columns([3,1])
    with col_head_1:
        st.markdown("<h1>SYSTEM STATUS: <span style='color:#00FF00'>ONLINE</span></h1>", unsafe_allow_html=True)
    with col_head_2:
        if st.button("LOGIN / START SYSTEM"):
            st.session_state['page'] = 'login'
            st.rerun()

    st.markdown("---")
    
    # PRODUCT FEATURES (English)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="feature-box">
            <h4>[ MACRO_DATA ]</h4>
            <p>Analyze historical seasonality of key currencies (USD, EUR) over the last 15 years. 
            Identify months with the highest probability of growth or decline and gain a statistical edge.</p>
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
        
    with col_paid:
        # This one gets the special .paid-box class with the GREEN BORDER
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

    # GET STARTED BUTTON (Centers the flow)
    st.write("")
    c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
    with c_btn2:
        if st.button("GET STARTED >>", use_container_width=True):
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
            # Login widget
            name, status, user = authenticator.login('Login', 'main')
            
            # Logic to handle login success immediately
            if status:
                st.session_state['authentication_status'] = True
                st.session_state['name'] = name
                st.session_state['username'] = user
                st.session_state['page'] = 'dashboard'
                st.rerun()
            elif status is False:
                st.error("ACCESS DENIED: INVALID CREDENTIALS")
                
        with tab2:
            st.warning("REGISTRATION PROTOCOL: DISABLED (DB_OFFLINE)")
            st.markdown("For DEMO access, use credentials below:")
            st.code("User: admin\nPass: password123")
            st.code("User: guest\nPass: guest123")
        
        st.markdown("---")
        if st.button("< RETURN TO BASE"): 
            st.session_state['page'] = 'landing'
            st.rerun()

def render_dashboard():
    # Determine Status
    user_status = 'PAID' if st.session_state["username"] == 'admin' else 'FREE'
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"### USER: {st.session_state['username'].upper()}")
        st.markdown(f"### TIER: <span style='color:{'#00FF00' if user_status=='PAID' else 'white'}'>{user_status}</span>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("> WATCHLIST"): st.session_state['active_tab'] = 'watchlist'; st.rerun()
        if st.button("> CURRENCY HUB"): st.session_state['active_tab'] = 'currency'; st.rerun()
        st.markdown("---")
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
                fig.update_traces(line=dict(width=2))
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
                    z=piv.values, x=piv.columns, y=piv.index, 
                    colorscale='Electric',
                    text=piv.values, texttemplate="%{text:.1f}"
                ))
                fig.update_layout(
                    plot_bgcolor='black', paper_bgcolor='black', font_color='#E0E0E0', height=600
                )
                st.plotly_chart(fig, use_container_width=True)

# -------------------------
# 5. MAIN APP CONTROLLER
# -------------------------
render_navbar()

# If user is logged in via cookie/session, go straight to dashboard
if st.session_state.get('authentication_status'):
    render_dashboard()
else:
    # Router for non-logged users
    if st.session_state['page'] == 'landing':
        render_landing()
    elif st.session_state['page'] == 'login':
        render_login_page()
    else:
        render_landing()
