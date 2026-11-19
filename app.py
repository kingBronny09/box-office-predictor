import streamlit as st

# Domestic Model (from Row 2: H2:K2)
M1_DOM = 3.332504304      # Cell J2 (Opening Weekend slope)
M2_DOM = 0.1631975235     # Cell I2 (Production Budget slope)
M3_DOM = 17.93605272      # Cell H2 (CinemaScore slope)
B_DOM = -170.858763       # Cell K2 (Domestic Intercept)

# Worldwide Model (from Row 9: H9:K9)
M1_WW = 7.40580118        # Cell J9 (Opening Weekend slope)
M2_WW = 1.31420456        # Cell I9 (Production Budget slope)
M3_WW = 41.83655214       # Cell H9 (CinemaScore slope)
B_WW = -501.0544971       # Cell K9 (Worldwide Intercept)

st.set_page_config(
    page_title="Box Office ROI & Revenue Predictor",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS: Bottom-Left Green + Top-Right Purple Streaks & Pure White Slider
st.markdown(
    """
    /* 1. Force the actual horizontal slider bar (track) to pure white */
    div[data-baseweb="slider"] > div > div {
        background: #FFFFFF !important;
        height: 6px !important;
        border-radius: 4px !important;
    }

    /* 2. Force the draggable circle (thumb) to pure white */
    div[data-baseweb="slider"] div[role="slider"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.8) !important;
    }

    /* 3. Force the active grade (B+) and F / A+ endpoint letters to pure white */
    div[data-testid="stSliderThumbValue"],
    div[data-testid="stSliderTickBarMin"],
    div[data-testid="stSliderTickBarMax"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Dark background with Emerald-Green streak in Bottom-Left & Royal-Purple in Top-Right */
    [data-testid="stAppViewContainer"] {
        background-color: #090612 !important;
        background-image:
            radial-gradient(ellipse at 10% 88%, rgba(16, 185, 129, 0.45) 0%, transparent 52%),
            radial-gradient(ellipse at 90% 15%, rgba(168, 85, 247, 0.42) 0%, transparent 52%),
            linear-gradient(35deg,
                rgba(16, 185, 129, 0.28) 0%,
                rgba(9, 6, 18, 0.92) 38%,
                rgba(9, 6, 18, 0.92) 62%,
                rgba(139, 0, 107, 0.32) 100%
            ) !important;
        background-attachment: fixed !important;
    }

    /* Frosted-glass dark card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(14, 11, 24, 0.82) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 16px !important;
        box-shadow:
            -12px 12px 35px rgba(16, 185, 129, 0.20),
            12px -12px 35px rgba(168, 85, 247, 0.22) !important;
        padding: 12px !important;
    }

    /* Pure White Slider Handle (draggable circle) */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #FFFFFF !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 0 8px rgba(255, 255, 255, 0.55) !important;
    }

    /* Pure White Slider Active Track (filled portion) */
    div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        background-color: #FFFFFF !important;
    }

    /* Pure White Selected Grade above thumb & F / A+ endpoint tick labels */
    div[data-testid="stSliderThumbValue"],
    div[data-testid="stSliderTickBarMin"],
    div[data-testid="stSliderTickBarMax"],
    div[data-baseweb="slider"] * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

GRADE_TO_NUM = {
    "F": 0, "D-": 1, "D": 2, "D+": 3,
    "C-": 4, "C": 5, "C+": 6,
    "B-": 7, "B": 8, "B+": 9,
    "A-": 10, "A": 11, "A+": 12
}

with st.container(border=True):
    st.subheader("🎬 BOX OFFICE ROI & REVENUE PREDICTOR")
    st.divider()

    col1_lbl, col1_in = st.columns([1.4, 1], vertical_alignment="center")
    col1_lbl.markdown("**Production Budget ($M):**")
    budget = col1_in.number_input(
        "Production Budget ($M)",
        min_value=1.0, max_value=500.0, value=120.0, step=5.0,
        label_visibility="collapsed"
    )

    col2_lbl, col2_in = st.columns([1.4, 1], vertical_alignment="center")
    col2_lbl.markdown("**Domestic Opening Weekend Gross ($M):**")
    opening = col2_in.number_input(
        "Opening Weekend Gross ($M)",
        min_value=0.1, max_value=400.0, value=55.0, step=1.0,
        label_visibility="collapsed"
    )

    col3_lbl, col3_in = st.columns([1.4, 1], vertical_alignment="center")
    col3_lbl.markdown("**Audience Score (CinemaScore):**")
    selected_grade = col3_in.select_slider(
        "Audience Score",
        options=list(GRADE_TO_NUM.keys()),
        value="B+",
        label_visibility="collapsed"
    )

    st.divider()

    score_num = GRADE_TO_NUM[selected_grade]

    pred_dom = (M1_DOM * opening) + (M2_DOM * budget) + (M3_DOM * score_num) + B_DOM
    pred_dom = max(opening, pred_dom)

    pred_ww = (M1_WW * opening) + (M2_WW * budget) + (M3_WW * score_num) + B_WW
    pred_ww = max(pred_dom, pred_ww)

    break_even_target = budget * 2.5
    roi_pct = ((pred_ww - break_even_target) / break_even_target) * 100

    res1_lbl, res1_val = st.columns([1.4, 1], vertical_alignment="center")
    res1_lbl.markdown("**PREDICTED TOTAL DOMESTIC GROSS:**")
    res1_val.markdown(f"### ${pred_dom:,.1f} Million")

    res2_lbl, res2_val = st.columns([1.4, 1], vertical_alignment="center")
    res2_lbl.markdown("**PREDICTED WORLDWIDE GROSS:**")
    res2_val.markdown(f"### ${pred_ww:,.1f} Million")

    res3_lbl, res3_val = st.columns([1.4, 1], vertical_alignment="center")
    res3_lbl.markdown("**ESTIMATED STUDIO ROI:**")
    if roi_pct >= 0:
        res3_val.markdown(f"### :green[+{roi_pct:,.1f}% (Profitable)]")
    else:
        res3_val.markdown(f"### :red[{roi_pct:,.1f}% (Below Break-Even)]")
