import streamlit as st
import numpy as np
import pandas as pd

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
    page_title="BOXOFFICEIQ",
    page_icon="🎬",
    layout="centered"
)

# Clean CSS: Green bottom-left & Purple top-right background + Hide toolbar/badges + Crisp White Tabs & Button + Top-Left Brand
st.markdown(
    """
    <style>
    /* Hide top-right toolbar, footer, status widgets, and Streamlit Cloud creator/manage badges */
    [data-testid="stToolbar"],
    [data-testid="stHeader"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="manage-app-button"],
    [class*="viewerBadge"],
    [class*="StatusWidget"],
    a[href*="streamlit.io/cloud"],
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* Top-Left Fixed Brand Title */
    .top-left-brand {
        position: fixed;
        top: 18px;
        left: 24px;
        z-index: 99999;
        font-size: 1.25rem;
        font-weight: 900;
        letter-spacing: 0.1em;
        color: #FFFFFF;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        user-select: none;
    }

    /* Push main content down slightly on smaller screens so it never overlaps the top-left brand */
    @media (max-width: 900px) {
        .block-container {
            padding-top: 3.5rem !important;
        }
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

    /* All-White Submit buttons */
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

    <div class="top-left-brand">🎬 BOXOFFICEIQ</div>
    """,
    unsafe_allow_html=True
)

GRADE_TO_NUM = {
    "F": 0, "D-": 1, "D": 2, "D+": 3,
    "C-": 4, "C": 5, "C+": 6,
    "B-": 7, "B": 8, "B+": 9,
    "A-": 10, "A": 11, "A+": 12
}

tab1, tab2, tab3, tab4, tab5 = st.tabs(["HOME", "PREDICTOR", "MONTE CARLO", "ACCURATELY PREDICTED FILMS", "TOP 10"])

# ==========================================================
# TAB 1: HOME (About the Website)
# ==========================================================
with tab1:
    with st.container(border=True):
        st.subheader("🎬 ABOUT THE WEBSITE")
        st.divider()

        st.markdown(
            "**BOXOFFICEIQ** is a data-driven box office forecasting and movie analytics platform built to predict "
            "a film's final theatrical run and studio profitability right after its opening weekend."
        )

        st.markdown("**What You Can Do Here:**")
        st.markdown(
            "- **Predict Final Box Office & Studio ROI (`PREDICTOR`):** Plug in any movie's production budget, domestic opening weekend gross, "
            "and opening-night CinemaScore to forecast its final Domestic Gross, Worldwide Gross, and whether it clears Hollywood's 2.5× break-even threshold.\n"
            "- **Simulate Thousands of Box Office Outcomes (`MONTE CARLO`):** Run up to 10,000 simulated theatrical runs to visualize best-case, "
            "worst-case, and profit probability distributions.\n"
            "- **Explore Real-World Accuracy (`ACCURATELY PREDICTED FILMS`):** See side-by-side examples of modern theatrical releases where "
            "BOXOFFICEIQ's opening-weekend projections closely matched actual final box office totals.\n"
            "- **Browse All-Time Records (`TOP 10`):** Compare the 10 highest-grossing global blockbusters in cinema history against the 10 biggest studio box office flops."
        )

        st.divider()
        st.caption("Select the **PREDICTOR** or **MONTE CARLO** tab at the top to test a movie, or explore the historical charts across the navigation bar.")

# ==========================================================
# TAB 2: MAIN PREDICTOR (Form-gated so it waits for "PREDICT")
# ==========================================================
with tab2:
    with st.container(border=True):
        st.subheader("🎬 Box Office Predictor and ROI Prediction")
        st.divider()

        with st.form("predictor_form"):
            col1_lbl, col1_in = st.columns([1.4, 1], vertical_alignment="center")
            col1_lbl.markdown("**Production Budget ($M):**")
            budget = col1_in.number_input(
                "Production Budget ($M)",
                min_value=0.2, max_value=700.0, value=100.0, step=5.0,
                label_visibility="collapsed"
            )

            col2_lbl, col2_in = st.columns([1.4, 1], vertical_alignment="center")
            col2_lbl.markdown("**Domestic Opening Weekend Gross ($M):**")
            opening = col2_in.number_input(
                "Opening Weekend Gross ($M)",
                min_value=0.03, max_value=450.0, value=50.0, step=1.0,
                label_visibility="collapsed"
            )

            col3_lbl, col3_in = st.columns([1.4, 1], vertical_alignment="center")
            col3_lbl.markdown("**Audience Score (CinemaScore):**")
            selected_grade = col3_in.select_slider(
                "Audience Score",
                options=list(GRADE_TO_NUM.keys()),
                value="C+",
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
            st.caption("Adjust the budget of your desired film, adjust the opening weekend sales, and CinemaScore above, then click **PREDICT**.")
    
    st.markdown("<div style='height: 96px;'></div>", unsafe_allow_html=True)
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
# TAB 3: MONTE CARLO SIMULATION
# ==========================================================
with tab3:
    with st.container(border=True):
        st.subheader("🎲 MONTE CARLO BOX OFFICE SIMULATION")
        st.caption(
            "Simulates thousands of possible theatrical runs using our regression model's unexplained variance "
            "to measure downside risk, upside potential, and profit odds."
        )
        st.divider()

        with st.form("monte_carlo_form"):
            mc_b_lbl, mc_b_in = st.columns([1.4, 1], vertical_alignment="center")
            mc_b_lbl.markdown("**Production Budget ($M):**")
            mc_budget = mc_b_in.number_input(
                "MC Production Budget ($M)",
                min_value=0.2, max_value=700.0, value=100.0, step=5.0,
                label_visibility="collapsed"
            )

            mc_o_lbl, mc_o_in = st.columns([1.4, 1], vertical_alignment="center")
            mc_o_lbl.markdown("**Domestic Opening Weekend Gross ($M):**")
            mc_opening = mc_o_in.number_input(
                "MC Opening Weekend Gross ($M)",
                min_value=0.03, max_value=450.0, value=50.0, step=1.0,
                label_visibility="collapsed"
            )

            mc_g_lbl, mc_g_in = st.columns([1.4, 1], vertical_alignment="center")
            mc_g_lbl.markdown("**Audience Score (CinemaScore):**")
            mc_grade = mc_g_in.select_slider(
                "MC Audience Score",
                options=list(GRADE_TO_NUM.keys()),
                value="C+",
                label_visibility="collapsed"
            )

            mc_s_lbl, mc_s_in = st.columns([1.4, 1], vertical_alignment="center")
            mc_s_lbl.markdown("**Number of Simulated Runs:**")
            num_sims = mc_s_in.select_slider(
                "Simulated Runs",
                options=[10, 100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000],
                value=2000,
                label_visibility="collapsed"
            )

            st.write("")
            mc_submitted = st.form_submit_button("RUN SIMULATION", use_container_width=True)

        if mc_submitted:
            st.divider()

            mc_score_num = GRADE_TO_NUM[mc_grade]

            base_dom = (M1_DOM * mc_opening) + (M2_DOM * mc_budget) + (M3_DOM * mc_score_num) + B_DOM
            base_dom = max(mc_opening, base_dom)

            base_ww = (M1_WW * mc_opening) + (M2_WW * mc_budget) + (M3_WW * mc_score_num) + B_WW
            base_ww = max(base_dom, base_ww)

            mc_break_even = mc_budget * 2.5

            # Simulate Domestic (18% std dev from 13.5% unexplained variance) and Worldwide (24% std dev from 20.4% unexplained variance)
            rng = np.random.default_rng(seed=42)
            sim_dom = np.maximum(mc_opening, rng.normal(loc=base_dom, scale=base_dom * 0.18, size=num_sims))
            sim_ww = np.maximum(sim_dom, rng.normal(loc=base_ww, scale=base_ww * 0.24, size=num_sims))

            p10 = np.percentile(sim_ww, 10)
            p50 = np.percentile(sim_ww, 50)
            p90 = np.percentile(sim_ww, 90)
            prob_profit = np.mean(sim_ww >= mc_break_even) * 100

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("10th % (Low)", f"${p10:,.0f}M")
            m2.metric("Median (50th %)", f"${p50:,.0f}M")
            m3.metric("90th % (High)", f"${p90:,.0f}M")
            m4.metric("Odds of Profit", f"{prob_profit:.1f}%")

            st.write("")
            st.markdown("**Simulated Worldwide Gross Distribution ($M)**")

            counts, bin_edges = np.histogram(sim_ww, bins=30)
            bin_centers = np.round((bin_edges[:-1] + bin_edges[1:]) / 2, 1)

            chart_df = pd.DataFrame({
                "Projected Worldwide Gross ($M)": bin_centers,
                "Loss (Below 2.5× Break-Even)": [
                    c if val < mc_break_even else 0 for val, c in zip(bin_centers, counts)
                ],
                "Profitable (Above 2.5× Break-Even)": [
                    c if val >= mc_break_even else 0 for val, c in zip(bin_centers, counts)
                ],
            })

            st.bar_chart(
                chart_df,
                x="Projected Worldwide Gross ($M)",
                y=["Loss (Below 2.5× Break-Even)", "Profitable (Above 2.5× Break-Even)"],
                color=["#EF4444", "#10B981"]
            )

            st.caption(
                f"Break-Even Target (2.5× Budget): **${mc_break_even:,.1f}M** | "
                f"Expected Domestic Range (10th–90th %): **${np.percentile(sim_dom, 10):,.0f}M – ${np.percentile(sim_dom, 90):,.0f}M**"
            )
        else:
            st.caption("Set your film's parameters and number of simulations above, then click **RUN SIMULATION**.")

# ==========================================================
# TAB 4: ACCURATELY PREDICTED FILMS (Placeholder ready for your picks)
# ==========================================================
with tab4:
    with st.container(border=True):
        st.subheader("🎯 ACCURATELY PREDICTED FILMS")
        st.divider()
        st.caption("Coming soon — times when the predictor accurately predicted the film's box office numbers.")

# ==========================================================
# TAB 5: TOP 10 HIGHEST-GROSSING & TOP 10 BIGGEST FLOPS
# ==========================================================
with tab5:
    # --- CARD A: TOP 10 HIGHEST-GROSSING FILMS ---
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

        h1, h2, h3, h4 = st.columns([0.6, 2.6, 1.2, 1.0])
        h1.markdown("**Rank**")
        h2.markdown("**Film**")
        h3.markdown("**Worldwide**")
        h4.markdown("**Budget**")
        st.divider()

        for movie in top_10_movies:
            c1, c2, c3, c4 = st.columns([0.6, 2.6, 1.2, 1.0], vertical_alignment="center")
            c1.markdown(f"**{movie['rank']}**")
            c2.markdown(f"**{movie['title']}**")
            c3.markdown(f":green[**{movie['worldwide']}**]")
            c4.markdown(f"{movie['budget']}")

    st.markdown("<div style='height: 96px;'></div>", unsafe_allow_html=True)
    st.markdown("When talking about the Top 10 Highest Grossing, it's hard not to mention the stinkers. Here are the...")

    # --- CARD B: TOP 10 BIGGEST WORLDWIDE BOX OFFICE FLOPS ---
    with st.container(border=True):
        st.subheader("📉 TOP 10 BIGGEST WORLDWIDE BOX OFFICE FLOPS")
        st.caption("Ranked by estimated unadjusted studio net loss (accounting for production budget, marketing, and theater cuts).")
        st.divider()

        top_10_flops = [
            {"rank": "#1", "title": "The Marvels (2023)", "worldwide": "$206.1M", "budget": "$270M", "loss": "-$237M"},
            {"rank": "#2", "title": "John Carter (2012)", "worldwide": "$284.1M", "budget": "$264M", "loss": "-$200M"},
            {"rank": "#3", "title": "Strange World (2022)", "worldwide": "$73.6M", "budget": "$180M", "loss": "-$197M"},
            {"rank": "#4", "title": "The Lone Ranger (2013)", "worldwide": "$260.5M", "budget": "$225M", "loss": "-$190M"},
            {"rank": "#5", "title": "Mortal Engines (2018)", "worldwide": "$83.7M", "budget": "$110M", "loss": "-$175M"},
            {"rank": "#6", "title": "The Flash (2023)", "worldwide": "$271.3M", "budget": "$200M", "loss": "-$155M"},
            {"rank": "#7", "title": "King Arthur: Legend of the Sword (2017)", "worldwide": "$148.7M", "budget": "$175M", "loss": "-$153M"},
            {"rank": "#8", "title": "Jungle Cruise (2021)", "worldwide": "$220.9M", "budget": "$200M", "loss": "-$150M"},
            {"rank": "#9", "title": "Joker: Folie à Deux (2024)", "worldwide": "$206.4M", "budget": "$190M", "loss": "-$144M"},
            {"rank": "#10", "title": "Mars Needs Moms (2011)", "worldwide": "$39.0M", "budget": "$150M", "loss": "-$144M"},
        ]

        fh1, fh2, fh3, fh4, fh5 = st.columns([0.55, 2.35, 1.0, 0.9, 1.0])
        fh1.markdown("**Rank**")
        fh2.markdown("**Film**")
        fh3.markdown("**Worldwide**")
        fh4.markdown("**Budget**")
        fh5.markdown("**Est. Loss**")
        st.divider()

        for flop in top_10_flops:
            fc1, fc2, fc3, fc4, fc5 = st.columns([0.55, 2.35, 1.0, 0.9, 1.0], vertical_alignment="center")
            fc1.markdown(f"**{flop['rank']}**")
            fc2.markdown(f"**{flop['title']}**")
            fc3.markdown(f"{flop['worldwide']}")
            fc4.markdown(f"{flop['budget']}")
            fc5.markdown(f":red[**{flop['loss']}**]")
