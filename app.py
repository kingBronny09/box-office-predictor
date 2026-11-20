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

    /* All-White PREDICT button */
    [data-testid="stFormSubmitButton"] button
