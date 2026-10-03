import streamlit as st
import pandas as pd
import joblib

from pathlib import Path
from datetime import timedelta


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PJM Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# PROFESSIONAL DARK ENERGY THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL APPLICATION BACKGROUND
       ======================================================== */

    .stApp {

        background:
            linear-gradient(
                rgba(1, 8, 20, 0.78),
                rgba(2, 14, 31, 0.90)
            ),
            linear-gradient(
                135deg,
                rgba(0, 50, 100, 0.18),
                rgba(0, 0, 0, 0.20)
            ),
            url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=2600&q=95");

        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;

        color: #edf7ff;
    }


    /* ========================================================
       PREMIUM BACKGROUND OVERLAY
       ======================================================== */

    .stApp::before {

        content: "";

        position: fixed;

        inset: 0;

        background:

            radial-gradient(
                circle at 82% 12%,
                rgba(0, 174, 255, 0.13),
                transparent 32%
            ),

            radial-gradient(
                circle at 8% 75%,
                rgba(0, 115, 220, 0.11),
                transparent 38%
            ),

            linear-gradient(
                180deg,
                rgba(2, 10, 24, 0.08),
                rgba(2, 10, 24, 0.30)
            );

        pointer-events: none;

        z-index: 0;
    }


    /* ========================================================
       MAIN CONTENT
       ======================================================== */

    .main {

        position: relative;

        z-index: 1;
    }


    .block-container {

        max-width: 1500px;

        padding-top: 2.4rem;
        padding-bottom: 3rem;

        padding-left: 2.8rem;
        padding-right: 2.8rem;
    }


    /* ========================================================
       SIDEBAR - PREMIUM CONTROL PANEL
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:

            linear-gradient(
                180deg,
                rgba(2, 12, 27, 0.985),
                rgba(4, 23, 46, 0.985),
                rgba(2, 17, 35, 0.985)
            );

        border-right:
            1px solid
            rgba(76, 182, 255, 0.28);

        box-shadow:

            12px 0 40px
            rgba(0, 0, 0, 0.50),

            inset -1px 0
            rgba(103, 196, 255, 0.08);
    }


    /* ========================================================
       SIDEBAR TEXT
       ======================================================== */

    section[data-testid="stSidebar"] * {

        color: #edf7ff !important;
    }


    section[data-testid="stSidebar"] h1 {

        color: #ffffff !important;

        font-size: 1.55rem !important;

        font-weight: 850 !important;

        letter-spacing: -0.4px;

        margin-bottom: 0.15rem !important;
    }


    section[data-testid="stSidebar"] h2 {

        color: #ffffff !important;

        font-size: 1.18rem !important;

        font-weight: 800 !important;
    }


    section[data-testid="stSidebar"] h3 {

        color: #f4faff !important;

        font-size: 1.02rem !important;

        font-weight: 780 !important;
    }


    section[data-testid="stSidebar"] p {

        color: #a9c5df !important;

        line-height: 1.55;

        font-size: 0.88rem;
    }


    section[data-testid="stSidebar"] strong {

        color: #ffffff !important;

        font-weight: 800 !important;
    }


    /* ========================================================
       SIDEBAR CAPTION
       ======================================================== */

    section[data-testid="stSidebar"] .stCaption {

        color: #74b8e8 !important;

        font-size: 0.75rem !important;

        font-weight: 700 !important;

        letter-spacing: 1.1px;

        text-transform: uppercase;
    }


    /* ========================================================
       SIDEBAR DIVIDERS
       ======================================================== */

    section[data-testid="stSidebar"] hr {

        border: none;

        height: 1px;

        background:

            linear-gradient(
                90deg,
                transparent,
                rgba(90, 190, 255, 0.28),
                transparent
            );

        margin: 1.15rem 0;
    }


    /* ========================================================
       SIDEBAR INPUT
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-baseweb="input"] > div {

        background:

            linear-gradient(
                145deg,
                rgba(9, 34, 61, 0.98),
                rgba(5, 24, 47, 0.98)
            ) !important;

        border:
            1px solid
            rgba(92, 190, 250, 0.28) !important;

        border-radius: 13px;

        min-height: 44px;

        box-shadow:

            inset 0 1px 0
            rgba(255,255,255,0.035),

            0 5px 16px
            rgba(0,0,0,0.18);
    }


    section[data-testid="stSidebar"] input {

        color: #ffffff !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       SIDEBAR EXPANDERS
       ======================================================== */

    section[data-testid="stSidebar"]
    .streamlit-expanderHeader {

        background:

            linear-gradient(
                135deg,
                rgba(9, 37, 67, 0.98),
                rgba(5, 25, 48, 0.98)
            );

        border:
            1px solid
            rgba(96, 190, 246, 0.22);

        border-radius: 13px;

        color: #ffffff !important;

        font-weight: 760;

        padding: 0.82rem 0.9rem;

        box-shadow:

            0 7px 20px
            rgba(0,0,0,0.16);

        transition: all 0.2s ease;
    }


    section[data-testid="stSidebar"]
    .streamlit-expanderHeader:hover {

        border-color:
            rgba(104, 207, 255, 0.46);

        background:

            linear-gradient(
                135deg,
                rgba(12, 48, 84, 0.99),
                rgba(6, 29, 55, 0.99)
            );
    }


    section[data-testid="stSidebar"]
    .streamlit-expanderContent {

        background:

            linear-gradient(
                180deg,
                rgba(4, 22, 42, 0.98),
                rgba(3, 17, 34, 0.98)
            );

        border:
            1px solid
            rgba(81, 170, 230, 0.14);

        border-top: none;

        border-radius:
            0 0 13px 13px;

        color: #d7e9f8 !important;

        padding-top: 0.65rem;
    }


    /* ========================================================
       SIDEBAR METRICS
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stMetric"] {

        background:

            linear-gradient(
                145deg,
                rgba(9, 38, 68, 0.90),
                rgba(4, 25, 49, 0.92)
            );

        border:
            1px solid
            rgba(91, 188, 247, 0.17);

        border-radius: 12px;

        padding: 10px 12px;

        margin-bottom: 8px;
    }


    section[data-testid="stSidebar"]
    div[data-testid="stMetricLabel"] {

        color: #8fb5d7 !important;

        font-size: 0.72rem !important;

        font-weight: 750 !important;

        text-transform: uppercase;
    }


    section[data-testid="stSidebar"]
    div[data-testid="stMetricValue"] {

        color: #ffffff !important;

        font-size: 1.18rem !important;

        font-weight: 820 !important;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    h1 {

        color: #ffffff !important;

        font-size: 2.75rem !important;

        font-weight: 850 !important;

        letter-spacing: -1.1px;

        line-height: 1.12;

        margin-bottom: 0.35rem !important;

        text-shadow:
            0 4px 20px
            rgba(0,0,0,0.72);
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    h2 {

        color: #f5fbff !important;

        font-size: 1.65rem !important;

        font-weight: 820 !important;

        letter-spacing: -0.35px;

        margin-top: 1.8rem !important;

        margin-bottom: 0.8rem !important;

        text-shadow:
            0 3px 14px
            rgba(0,0,0,0.62);
    }


    h3 {

        color: #e7f6ff !important;

        font-size: 1.22rem !important;

        font-weight: 780 !important;

        margin-top: 1.25rem !important;

        margin-bottom: 0.65rem !important;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p,
    li {

        color: #d2e6f7;

        line-height: 1.6;
    }


    /* ========================================================
       INTRO TEXT
       ======================================================== */

    .intro-text {

        color: #a9c7df;

        font-size: 1.02rem;

        line-height: 1.7;

        margin-bottom: 1.4rem;

        text-shadow:
            0 2px 8px
            rgba(0,0,0,0.60);
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background:

            linear-gradient(
                145deg,
                rgba(12, 44, 78, 0.94),
                rgba(4, 24, 47, 0.97)
            );

        border:
            1px solid
            rgba(99, 194, 255, 0.25);

        border-radius: 18px;

        padding: 20px;

        min-height: 125px;

        box-shadow:

            0 14px 38px
            rgba(0,0,0,0.34),

            inset 0 1px 0
            rgba(255,255,255,0.045);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    div[data-testid="stMetric"]:hover {

        transform:
            translateY(-3px);

        box-shadow:

            0 18px 42px
            rgba(0,0,0,0.43),

            0 0 24px
            rgba(0,157,255,0.13);
    }


    div[data-testid="stMetric"] label {

        color: #91b8d9 !important;

        font-size: 0.74rem !important;

        font-weight: 760 !important;

        letter-spacing: 0.75px;

        text-transform: uppercase;
    }


    div[data-testid="stMetricValue"] {

        color: #ffffff !important;

        font-size: 1.80rem !important;

        font-weight: 850 !important;

        letter-spacing: -0.5px;

        text-shadow:
            0 2px 11px
            rgba(0,0,0,0.42);
    }


    div[data-testid="stMetricDelta"] {

        color: #72d9ff !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button,
    .stDownloadButton > button {

        min-height: 48px;

        border-radius: 13px;

        font-size: 0.94rem;

        font-weight: 800;

        letter-spacing: 0.25px;

        color: #ffffff !important;

        background:

            linear-gradient(
                135deg,
                #00a0e8,
                #006bd6
            );

        border:
            1px solid
            rgba(133, 221, 255, 0.34);

        box-shadow:

            0 9px 25px
            rgba(0, 103, 205, 0.28);

        transition:
            all 0.2s ease;
    }


    .stButton > button:hover,
    .stDownloadButton > button:hover {

        transform:
            translateY(-2px);

        background:

            linear-gradient(
                135deg,
                #08b1f2,
                #0879e3
            );

        box-shadow:

            0 13px 31px
            rgba(0, 123, 235, 0.38);
    }


    /* ========================================================
       SELECTBOXES / INPUTS
       ======================================================== */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {

        background:

            rgba(7, 31, 57, 0.94) !important;

        border:
            1px solid
            rgba(96, 189, 245, 0.24) !important;

        border-radius: 11px;

        color: #ffffff !important;
    }


    input {

        color: #ffffff !important;
    }


    /* ========================================================
       MAIN EXPANDERS
       ======================================================== */

    .streamlit-expanderHeader {

        background:

            linear-gradient(
                135deg,
                rgba(9, 37, 67, 0.96),
                rgba(6, 26, 49, 0.96)
            );

        border:
            1px solid
            rgba(95, 185, 240, 0.20);

        border-radius: 12px;

        color: #f2f8ff !important;

        font-weight: 750;

        padding: 0.8rem 1rem;
    }


    .streamlit-expanderContent {

        background:
            rgba(5, 22, 42, 0.94);

        border:
            1px solid
            rgba(100, 180, 240, 0.12);

        border-top: none;

        border-radius:
            0 0 12px 12px;

        color: #d8e9f8 !important;
    }


    /* ========================================================
       CHART CONTAINERS
       ======================================================== */

    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"],
    div[data-testid="stPlotlyChart"] {

        background:

            linear-gradient(
                145deg,
                rgba(5, 27, 51, 0.92),
                rgba(3, 19, 38, 0.96)
            );

        border:
            1px solid
            rgba(91, 184, 244, 0.17);

        border-radius: 17px;

        padding: 11px;

        box-shadow:
            0 13px 32px
            rgba(0,0,0,0.25);
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 15px;

        overflow: hidden;

        border:
            1px solid
            rgba(103, 190, 245, 0.18);

        box-shadow:
            0 13px 30px
            rgba(0,0,0,0.28);

        background:
            rgba(4, 21, 40, 0.94);
    }


    /* ========================================================
       ALERT / INFO BOXES
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px;

        background:
            rgba(6, 29, 54, 0.94);

        border:
            1px solid
            rgba(97, 190, 242, 0.20);
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border: none;

        height: 1px;

        background:

            linear-gradient(
                90deg,
                transparent,
                rgba(110, 196, 248, 0.32),
                transparent
            );

        margin: 1.45rem 0;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {

        color: #6f91af;

        text-align: center;

        font-size: 0.76rem;

        padding: 1.8rem 0 0.5rem 0;

        letter-spacing: 0.25px;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {

            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {

            font-size: 2rem !important;
        }

        h2 {

            font-size: 1.4rem !important;
        }

        div[data-testid="stMetric"] {

            min-height: 105px;

            padding: 15px;
        }

        div[data-testid="stMetricValue"] {

            font-size: 1.4rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model_path = BASE_DIR / "xgb_model.pkl"

    if not model_path.exists():

        raise FileNotFoundError(
            "xgb_model.pkl was not found."
        )

    return joblib.load(model_path)


# ============================================================
# LOAD METADATA
# ============================================================

@st.cache_resource
def load_metadata():

    feature_path = BASE_DIR / "feature_columns.pkl"

    holiday_path = BASE_DIR / "holiday_dates.pkl"

    if not feature_path.exists():

        raise FileNotFoundError(
            "feature_columns.pkl was not found."
        )

    if not holiday_path.exists():

        raise FileNotFoundError(
            "holiday_dates.pkl was not found."
        )

    feature_columns = list(
        joblib.load(feature_path)
    )

    holiday_dates = joblib.load(
        holiday_path
    )

    # Convert holiday values into date objects

    cleaned_holidays = set()

    for date_value in holiday_dates:

        try:

            cleaned_holidays.add(
                pd.Timestamp(
                    date_value
                ).date()
            )

        except Exception:

            pass

    return (
        feature_columns,
        cleaned_holidays
    )


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    data_path = (
        BASE_DIR /
        "PJMW_MW_Hourly.xlsx"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            "PJMW_MW_Hourly.xlsx was not found."
        )

    df = pd.read_excel(
        data_path
    )

    # --------------------------------------------------------
    # Detect Datetime column
    # --------------------------------------------------------

    if "Datetime" not in df.columns:

        possible_date_columns = [

            col

            for col in df.columns

            if "date" in str(col).lower()

            or "time" in str(col).lower()

        ]

        if not possible_date_columns:

            raise ValueError(
                "Datetime column was not found."
            )

        df = df.rename(
            columns={
                possible_date_columns[0]:
                    "Datetime"
            }
        )


    # --------------------------------------------------------
    # Detect target column
    # --------------------------------------------------------

    if "PJMW_MW" not in df.columns:

        possible_target_columns = [

            col

            for col in df.columns

            if "pjmw" in str(col).lower()

            or "mw" in str(col).lower()

        ]

        if not possible_target_columns:

            raise ValueError(
                "PJMW_MW column was not found."
            )

        df = df.rename(
            columns={
                possible_target_columns[0]:
                    "PJMW_MW"
            }
        )


    # --------------------------------------------------------
    # Convert Datetime
    # --------------------------------------------------------

    df["Datetime"] = pd.to_datetime(
        df["Datetime"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # Convert target
    # --------------------------------------------------------

    df["PJMW_MW"] = pd.to_numeric(
        df["PJMW_MW"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # Remove invalid rows
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "Datetime",
            "PJMW_MW"
        ]
    )


    # --------------------------------------------------------
    # Sort data
    # --------------------------------------------------------

    df = (
        df
        .sort_values("Datetime")
        .reset_index(drop=True)
    )

    return df


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(
    history,
    holiday_dates
):

    current_time = (

        history["Datetime"].iloc[-1]

        + timedelta(hours=1)

    )

    features = {

        "Hour":
            current_time.hour,

        "Day":
            current_time.day,

        "DayOfWeek":
            current_time.dayofweek,

        "Month":
            current_time.month,

        "Year":
            current_time.year,

        "IsWeekend":
            int(
                current_time.dayofweek
                in [5, 6]
            ),

        "IsHoliday":
            int(
                current_time.date()
                in holiday_dates
            ),

        # ----------------------------------------------------
        # Lag features
        # ----------------------------------------------------

        "lag_1":
            history[
                "PJMW_MW"
            ].iloc[-1],

        "lag_2":
            history[
                "PJMW_MW"
            ].iloc[-2],

        "lag_3":
            history[
                "PJMW_MW"
            ].iloc[-3],

        "lag_24":
            history[
                "PJMW_MW"
            ].iloc[-24],

        "lag_48":
            history[
                "PJMW_MW"
            ].iloc[-48],

        "lag_168":
            history[
                "PJMW_MW"
            ].iloc[-168],

        # ----------------------------------------------------
        # Rolling features
        # ----------------------------------------------------

        "rolling_mean_24":

            history[
                "PJMW_MW"
            ]

            .iloc[-24:]

            .mean(),

        "rolling_mean_168":

            history[
                "PJMW_MW"
            ]

            .iloc[-168:]

            .mean(),

        "rolling_std_24":

            history[
                "PJMW_MW"
            ]

            .iloc[-24:]

            .std(),
    }

    return (

        pd.DataFrame(
            [features]
        ),

        current_time

    )


# ============================================================
# FORECAST GENERATION
# ============================================================

def generate_forecast(

    historical_df,
    days,
    model,
    feature_columns,
    holiday_dates

):

    if len(historical_df) < 168:

        raise ValueError(
            "At least 168 hourly observations "
            "are required for forecasting."
        )


    history = historical_df[
        [
            "Datetime",
            "PJMW_MW"
        ]
    ].copy()


    predictions = []


    # --------------------------------------------------------
    # Generate hourly predictions
    # --------------------------------------------------------

    for _ in range(
        int(days) * 24
    ):

        x_future, timestamp = (
            create_features(
                history,
                holiday_dates
            )
        )


        # ----------------------------------------------------
        # Check required features
        # ----------------------------------------------------

        missing_columns = [

            col

            for col in feature_columns

            if col not in x_future.columns

        ]

        if missing_columns:

            raise ValueError(
                f"Missing model features: "
                f"{missing_columns}"
            )


        # ----------------------------------------------------
        # Model prediction
        # ----------------------------------------------------

        prediction = float(

            model.predict(

                x_future[
                    feature_columns
                ]

            )[0]

        )


        # ----------------------------------------------------
        # Demand cannot be negative
        # ----------------------------------------------------

        prediction = max(
            0.0,
            prediction
        )


        # ----------------------------------------------------
        # Save prediction
        # ----------------------------------------------------

        predictions.append(

            {

                "Datetime":
                    timestamp,

                "Forecast_MW":
                    prediction

            }

        )


        # ----------------------------------------------------
        # Recursive forecasting
        # ----------------------------------------------------

        next_row = pd.DataFrame(

            {

                "Datetime":
                    [timestamp],

                "PJMW_MW":
                    [prediction]

            }

        )


        history = pd.concat(

            [

                history,

                next_row

            ],

            ignore_index=True

        )


    return pd.DataFrame(
        predictions
    )


# ============================================================
# LOAD REQUIRED FILES
# ============================================================

try:

    model = load_model()

    feature_columns, holiday_dates = (
        load_metadata()
    )

    df = load_data()

except Exception as error:

    st.error(
        f"Application setup failed: {error}"
    )

    st.info(
        "Place forecast.py, xgb_model.pkl, "
        "feature_columns.pkl, holiday_dates.pkl "
        "and PJMW_MW_Hourly.xlsx in the same folder."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚡ Energy AI"
)

st.sidebar.caption(
    "PJM DEMAND FORECASTING SYSTEM"
)

st.sidebar.divider()


# ============================================================
# FORECAST SETTINGS
# ============================================================

st.sidebar.subheader(
    "🎯 Forecast Settings"
)

forecast_days = st.sidebar.number_input(

    "Forecast Horizon (Days)",

    min_value=1,

    value=30,

    step=1

)

st.sidebar.caption(

    f"Hourly predictions: "
    f"{int(forecast_days) * 24:,}"

)

st.sidebar.divider()


# ============================================================
# SYSTEM STATUS
# ============================================================

st.sidebar.subheader(
    "🟢 System Status"
)

st.sidebar.success(
    "Model loaded"
)

st.sidebar.success(
    "Dataset loaded"
)

st.sidebar.success(
    "Forecast engine ready"
)

st.sidebar.divider()


# ============================================================
# MODEL INFORMATION
# ============================================================

with st.sidebar.expander(

    "🤖 Model Information",

    expanded=False

):

    st.write(
        "**Model:** XGBoost Regressor"
    )

    st.write(
        "**Target Variable:** PJMW_MW"
    )

    st.write(
        "**Forecast Frequency:** Hourly"
    )

    st.write(
        "**Forecast Type:** "
        "Recursive Multi-Step Forecasting"
    )

    st.write(
        "**Maximum Forecast Horizon:** "
        "No fixed limit"
    )

    st.write(
        "**Features:** Hour, Day, DayOfWeek, "
        "Month, Year, IsWeekend, IsHoliday, "
        "lag variables and rolling statistics."
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

with st.sidebar.expander(

    "📊 Dataset Information",

    expanded=False

):

    st.metric(
        "Observations",
        f"{len(df):,}"
    )

    st.metric(
        "Features",
        f"{len(feature_columns)}"
    )

    st.write(
        "**Data Start:** "
        f"{df['Datetime'].min().strftime('%d %b %Y')}"
    )

    st.write(
        "**Data End:** "
        f"{df['Datetime'].max().strftime('%d %b %Y')}"
    )


# ============================================================
# MODEL DETAILS
# ============================================================

with st.sidebar.expander(

    "⚙️ Model Details",

    expanded=False

):

    st.write(
        "**Algorithm:** XGBoost Regressor"
    )

    st.write(
        "**Frequency:** Hourly"
    )

    st.write(
        "**Target:** PJMW_MW"
    )

    st.write(
        "**Forecast Type:** Recursive"
    )

    st.write(
        "**Forecast Horizon:** User Defined"
    )


# ============================================================
# DATA STATUS
# ============================================================

st.sidebar.divider()

st.sidebar.subheader(
    "📡 Data Status"
)

st.sidebar.success(
    "Dataset loaded successfully"
)

st.sidebar.caption(
    f"{len(df):,} hourly observations available"
)


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "⚡ PJM Energy Intelligence"
)

st.markdown(

    """
    <p class="intro-text">
        Machine learning powered electricity demand forecasting
        using an XGBoost regression model.
    </p>
    """,

    unsafe_allow_html=True

)


# ============================================================
# HISTORICAL OVERVIEW
# ============================================================

st.header(
    "Historical Overview"
)


latest_value = (

    df[
        "PJMW_MW"
    ]

    .iloc[-1]

)


average_value = (

    df[
        "PJMW_MW"
    ]

    .mean()

)


peak_value = (

    df[
        "PJMW_MW"
    ]

    .max()

)


minimum_value = (

    df[
        "PJMW_MW"
    ]

    .min()

)


latest_timestamp = (

    df[
        "Datetime"
    ]

    .iloc[-1]

)


# ============================================================
# HISTORICAL KPI METRICS
# ============================================================

m1, m2, m3, m4 = (
    st.columns(4)
)


with m1:

    st.metric(

        "Current Demand",

        f"{latest_value:,.0f} MW"

    )


with m2:

    st.metric(

        "Historical Average",

        f"{average_value:,.0f} MW"

    )


with m3:

    st.metric(

        "Peak Demand",

        f"{peak_value:,.0f} MW"

    )


with m4:

    st.metric(

        "Last Observation",

        latest_timestamp.strftime(
            "%d %b %Y %H:%M"
        )

    )


# ============================================================
# HISTORICAL DEMAND CHART
# ============================================================

st.subheader(
    "Historical Demand — Last 7 Days"
)

st.caption(
    "Hourly electricity demand from the most recent seven-day period."
)


historical_chart = (

    df

    .tail(24 * 7)

    .set_index(
        "Datetime"
    )

    [
        [
            "PJMW_MW"
        ]
    ]

)


st.line_chart(

    historical_chart,

    height=400

)


# ============================================================
# FORECAST SECTION
# ============================================================

st.header(
    "Future Energy Forecast"
)

st.markdown(

    f"""
    <p class="intro-text">
        Generate <strong style="color:#ffffff;">
        {int(forecast_days) * 24:,} hourly predictions
        </strong>
        for the next
        <strong style="color:#ffffff;">
        {int(forecast_days):,} day(s)
        </strong>.
    </p>
    """,

    unsafe_allow_html=True

)


# ============================================================
# FORECAST BUTTON
# ============================================================

generate_forecast_button = st.button(

    "⚡ Generate Forecast",

    type="primary",

    use_container_width=True

)


# ============================================================
# FORECAST GENERATION
# ============================================================

if generate_forecast_button:

    with st.spinner(

        f"Generating "
        f"{int(forecast_days):,}-day "
        f"hourly forecast..."

    ):

        try:

            forecast_df = generate_forecast(

                df,

                int(forecast_days),

                model,

                feature_columns,

                holiday_dates

            )


            # ------------------------------------------------
            # Store forecast
            # ------------------------------------------------

            st.session_state[
                "forecast_df"
            ] = forecast_df


            st.success(
                "Forecast generated successfully."
            )


        except Exception as error:

            st.error(

                f"Forecast generation failed: "
                f"{error}"

            )


# ============================================================
# FORECAST RESULTS
# ============================================================

if "forecast_df" in st.session_state:

    forecast_df = (

        st.session_state[
            "forecast_df"
        ]

    )


    st.divider()


    # ========================================================
    # FORECAST SUMMARY
    # ========================================================

    st.header(
        "Forecast Results"
    )


    average_forecast = (

        forecast_df[
            "Forecast_MW"
        ]

        .mean()

    )


    maximum_forecast = (

        forecast_df[
            "Forecast_MW"
        ]

        .max()

    )


    minimum_forecast = (

        forecast_df[
            "Forecast_MW"
        ]

        .min()

    )


    peak_row = (

        forecast_df.loc[

            forecast_df[
                "Forecast_MW"
            ]

            .idxmax()

        ]

    )


    peak_time = (
        peak_row[
            "Datetime"
        ]
    )


    # ========================================================
    # FORECAST KPI METRICS
    # ========================================================

    f1, f2, f3, f4 = (
        st.columns(4)
    )


    with f1:

        st.metric(

            "Average Forecast",

            f"{average_forecast:,.0f} MW"

        )


    with f2:

        st.metric(

            "Forecast Peak",

            f"{maximum_forecast:,.0f} MW"

        )


    with f3:

        st.metric(

            "Forecast Minimum",

            f"{minimum_forecast:,.0f} MW"

        )


    with f4:

        st.metric(

            "Expected Peak Time",

            peak_time.strftime(
                "%d %b %H:%M"
            )

        )


    # ========================================================
    # FORECAST CHART
    # ========================================================

    st.subheader(
        "Forecasted Demand"
    )

    st.caption(
        "Hourly predicted electricity demand over the selected forecast horizon."
    )


    forecast_chart = (

        forecast_df

        .set_index(
            "Datetime"
        )

        [
            [
                "Forecast_MW"
            ]
        ]

    )


    st.line_chart(

        forecast_chart,

        height=430

    )


    # ========================================================
    # FORECAST STATISTICS
    # ========================================================

    st.subheader(
        "Forecast Statistics"
    )


    s1, s2, s3 = (
        st.columns(3)
    )


    with s1:

        st.metric(

            "Forecast Hours",

            f"{len(forecast_df):,}"

        )


    with s2:

        st.metric(

            "Forecast Period",

            (
                forecast_df[
                    "Datetime"
                ].min().strftime(
                    "%d %b %Y"
                )

                + " — "

                +

                forecast_df[
                    "Datetime"
                ].max().strftime(
                    "%d %b %Y"
                )
            )

        )


    with s3:

        st.metric(

            "Forecast Peak",

            f"{maximum_forecast:,.0f} MW"

        )


    # ========================================================
    # HOURLY FORECAST TABLE
    # ========================================================

    st.subheader(
        "Hourly Forecast Data"
    )


    display_df = (
        forecast_df.copy()
    )


    display_df["Datetime"] = (

        display_df[
            "Datetime"
        ]

        .dt.strftime(
            "%d-%b-%Y %H:%M"
        )

    )


    display_df["Forecast_MW"] = (

        display_df[
            "Forecast_MW"
        ]

        .round(2)

    )


    st.dataframe(

        display_df,

        use_container_width=True,

        height=450,

        hide_index=True

    )


    # ========================================================
    # DOWNLOAD FORECAST
    # ========================================================

    st.subheader(
        "Export Forecast"
    )


    csv_data = (

        forecast_df.to_csv(
            index=False
        )

    )


    st.download_button(

        label="⬇️ Download Forecast CSV",

        data=csv_data,

        file_name=(

            f"pjm_"
            f"{int(forecast_days)}"
            f"_day_forecast.csv"

        ),

        mime="text/csv",

        use_container_width=True

    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(

    """
    <p class="footer-text">
        ⚡ PJM Hourly Energy Consumption Forecasting
        &nbsp;•&nbsp;
        XGBoost Regression
        &nbsp;•&nbsp;
        Streamlit
    </p>
    """,

    unsafe_allow_html=True

)
