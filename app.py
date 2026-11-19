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

# Clean CSS: Green bottom-left & Purple top-right background + Hide toolbar + Solid White PREDICT Button
st.markdown(
    """
    <style>
    /* Hide top-right toolbar & footer */
    [data-testid="stToolbar"], [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
    }

    /* Green bottom-left & Purple top-right background streaks */
    [data-testid="stAppViewContainer"] {
        background-color: #090612;
        background-image:
            radial-gradient(circle at 10% 90%, rgba(16, 185, 129, 0.45), transparent 45%),
            radial-gradient(circle at 90% 10%, rgba(168, 85, 247, 0.45), transparent 45%);
        background-attachment: fixed;
    }

    /* Frosted dark cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(14, 11, 24, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 16px;
    }

    /* Remove extra inner border around st.form so it blends seamlessly into the card */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }

    /* All-White PREDICT button */
    [data-testid="stFormSubmitButton"] button {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #090612 !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 1.05rem !important;
        transition: opacity 0.2s ease, transform 0.1s ease;
    }
    [data-testid="stFormSubmitButton"] button p {
        color: #090612 !important;
        font-weight: 800 !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        opacity: 0.9 !important;
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

# ==========================================================
# CARD 1: MAIN PREDICTOR (Form-gated so it waits for "PREDICT")
# ==========================================================
with st.container(border=True):
    st.subheader("🎬 BOX OFFICE ROI & REVENUE PREDICTOR")
    st.divider()

    with st.form("predictor_form"):
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

        st.write("")
        submitted = st.form_submit_button("PREDICT", use_container_width=True)

    if submitted:
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
    else:
        st.caption("Adjust the budget, opening weekend, and CinemaScore above, then click **PREDICT**.")

st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)


# ==========================================================
# CARD 2: HOW IT WORKS & MODEL ACCURACY (Below the fold)
# ==========================================================
with st.container(border=True):
    st.subheader("📊 HOW THIS PREDICTOR WORKS & ACCURACY")
    st.divider()

    st.markdown("**1. The Model & Training Data**")
    st.markdown(
        "This predictor uses **multivariable linear regression** trained on **a large amount modern wide-release movies** "
        "(spanning from $10M horror hits to $2B blockbusters, as well as major box office flops). It weighs three key opening-weekend signals:"
    )
    st.markdown(
        "- **Domestic Opening Weekend ($M):** This is easily the strongest predictor of total theatrical momentum.\n"
        "- **Production Budget ($M):** Captures studio marketing scale and global release footprint.\n"
        "- **Opening-Night CinemaScore (`F` to `A+`):** It may not seem like a big deal, but a single grade step adds roughly **+$17.9M** domestically and **+$41.8M** worldwide."
    )

    st.divider()

    st.markdown("**2. Model Accuracy ($R^2$ Fit)**")
    acc1, acc2 = st.columns(2)
    acc1.metric(label="Domestic Box Office Accuracy (R²)", value="86.5%")
    acc2.metric(label="Worldwide Box Office Accuracy (R²)", value="79.6%")

    st.caption(
        "An R² of 86.5% means these three inputs explain over four-fifths of the variation in final domestic box office totals. "
        "Worldwide accuracy (79.6%) is slightly lower because certain franchises over-perform internationally relative to their domestic debut."
    )
    st.markdown(
        "- **Essentially what this means is that our Domestic Box Office Predictor is  ~ 87% accurate and our Worldwide Box Office Predictor is ~ 80% accurate. We are constantly updating our database and adding data to make it as accurate as possible.** "
    )

    st.divider()

    st.markdown("**3. How Studio ROI is Calculated**")
    st.markdown(
        "Movie theaters keep roughly **50% of ticket sales**, and studios spend millions on global marketing (P&A) on top of production costs. "
        "Following Hollywood's standard **2.5× Break-Even Rule**, a film generally needs to earn **2.5 times its production budget** worldwide just to break even before turning a theatrical profit."
    )
