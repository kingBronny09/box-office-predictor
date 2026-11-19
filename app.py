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

# Clean CSS: Green bottom-left & Purple top-right background + Hide toolbar + Crisp White Tabs & Button
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

    /* Top Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: rgba(255, 255, 255, 0.65) !important;
        padding: 10px 14px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #FFFFFF !important;
        height: 3px !important;
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
# TOP NAVIGATION TABS
# ==========================================================
tab1, tab2, tab3, tab4 = st.tabs(["Predictor", "How It Works & Accuracy", "Accurately Predicted Films", "Top 10 Highest Grossing"])

# ==========================================================
# TAB 1: MAIN PREDICTOR (Form-gated so it waits for "PREDICT")
# ==========================================================
with tab1:
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

# ==========================================================
# TAB 2: HOW IT WORKS & MODEL ACCURACY
# ==========================================================
with tab2:
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
            "**Essentially what this means is that our Domestic Box Office Predictor is ~ 87% accurate and our Worldwide Box Office Predictor is ~ 80% accurate. We are constantly updating our database and adding data to make it as accurate as possible.**"
        )

        st.divider()

        st.markdown("**3. How Studio ROI is Calculated**")
        st.markdown(
            "Movie theaters keep roughly **50% of ticket sales**, and studios spend millions on global marketing on top of production costs. "
            "Ben Affleck famously said that a film normally must make 4× its budget to break even. This can be true in some cases, but we still follow Hollywood's Break-Even Rule. "
            "Following Hollywood's standard **2.5× Break-Even Rule**, a film generally needs to earn **2.5 times its production budget** worldwide just to break even before turning a theatrical profit."
        )

# ==========================================================
# TAB 3: ACCURATELY PREDICTED FILMS (Placeholder ready for your picks)
# ==========================================================
with tab3:
    with st.container(border=True):
        st.subheader("🎯 ACCURATELY PREDICTED FILMS")
        st.divider()
        st.caption("Coming soon — real-world movies where the model's opening-weekend forecast closely matched actual final box office totals.")

# ==========================================================
# TAB 4: TOP 10 HIGHEST-GROSSING FILMS OF ALL TIME
# ==========================================================
with tab4:
    with st.container(border=True):
        st.subheader("🏆 TOP 10 HIGHEST-GROSSING FILMS OF ALL TIME")
        st.caption("Unadjusted worldwide theatrical box office totals.")
        st.divider()

        top_10_movies = [
            {"rank": "#1", "title": "Avatar (2009)", "worldwide": "$2.923B", "budget": "$237M"},
            {"rank": "#2", "title": "Avengers: Endgame (2019)", "worldwide": "$2.799B", "budget": "$356M"},
            {"rank": "#3", "title": "Avatar: The Way of Water (2022)", "worldwide": "$2.320B", "budget": "$350M"},
            {"rank": "#4", "title": "Titanic (1997)", "worldwide": "$2.264B", "budget": "$200M"},
            {"rank": "#5", "title": "Ne Zha 2 (2025)", "worldwide": "$2.150B", "budget": "$80M"},
            {"rank": "#6", "title": "Star Wars: The Force Awakens (2015)", "worldwide": "$2.071B", "budget": "$447M"},
            {"rank": "#7", "title": "Avengers: Infinity War (2018)", "worldwide": "$2.052B", "budget": "$325M"},
            {"rank": "#8", "title": "Spider-Man: No Way Home (2021)", "worldwide": "$1.922B", "budget": "$200M"},
            {"rank": "#9", "title": "Inside Out 2 (2024)", "worldwide": "$1.699B", "budget": "$200M"},
            {"rank": "#10", "title": "Jurassic World (2015)", "worldwide": "$1.671B", "budget": "$150M"},
        ]

        # Header Row
        h1, h2, h3, h4 = st.columns([0.6, 2.6, 1.2, 1.0])
        h1.markdown("**Rank**")
        h2.markdown("**Film**")
        h3.markdown("**Worldwide**")
        h4.markdown("**Budget**")
        st.divider()

        # Movie Rows
        for movie in top_10_movies:
            c1, c2, c3, c4 = st.columns([0.6, 2.6, 1.2, 1.0], vertical_alignment="center")
            c1.markdown(f"**{movie['rank']}**")
            c2.markdown(f"**{movie['title']}**")
            c3.markdown(f":green[**{movie['worldwide']}**]")
            c4.markdown(f"{movie['budget']}")
