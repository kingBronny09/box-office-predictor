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

# Custom CSS: Hide top-right toolbar + Style slider in Dark Royal Magenta (#8B006B)
st.markdown(
    """
    <style>
    /* Hide top-right Share, GitHub, 3-dots menu, header, and footer */
    [data-testid="stToolbar"],
    [data-testid="stHeader"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer {
        visibility: hidden !important;
        display: none !important;
    }

    /* Slider draggable circle */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #8B006B !important;
        border-color: #8B006B !important;
    }

    /* Slider filled track to the left of the circle */
    div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        background-color: #8B006B !important;
    }

    /* Slider active grade text (e.g., B+) */
    div[data-testid="stSliderThumbValue"] {
        color: #8B006B !important;
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
