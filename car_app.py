import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #16213e;
        --muted: #667085;
        --line: #e6e9ef;
        --panel: #ffffff;
        --accent: #e74c3c;
        --accent-dark: #c0392b;
        --teal: #0f9f8f;
        --gold: #f2a93b;
    }

    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #eef3f8 46%, #f7f9fc 100%);
        color: var(--ink);
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }

    section[data-testid="stSidebar"] {
        background: #16213e;
        border-right: 1px solid rgba(255, 255, 255, 0.12);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #f7fbff !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #16213e !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.28) !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] input[type="number"] {
        background: #ffffff !important;
        color: #16213e !important;
        -webkit-text-fill-color: #16213e !important;
        caret-color: #16213e !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] input::placeholder {
        color: #667085 !important;
        -webkit-text-fill-color: #667085 !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"] {
        background: #f4f7fb !important;
        color: #16213e !important;
        border-color: #d8dee8 !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"] svg {
        fill: #16213e !important;
        color: #16213e !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
        margin-bottom: 12px;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] label {
        color: #dce8f6 !important;
        font-weight: 700 !important;
        margin-bottom: 6px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #ffffff !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.16);
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        min-height: 44px !important;
        background: #ffffff !important;
        border: 1px solid #d8dee8 !important;
        border-radius: 8px !important;
        color: #16213e !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
        color: #16213e !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {
        color: #16213e !important;
        fill: #16213e !important;
    }

    .sidebar-section-title {
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-left: 4px solid #0f9f8f;
        border-radius: 8px;
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: 0;
        margin: 18px 0 12px 0;
        padding: 10px 12px;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-dark));
        border: 0;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 700;
        min-height: 3rem;
        box-shadow: 0 10px 24px rgba(231, 76, 60, 0.24);
    }

    .stButton > button:hover {
        border: 0;
        color: #ffffff;
        transform: translateY(-1px);
    }

    .hero {
        background: linear-gradient(135deg, #16213e 0%, #263b64 52%, #0f9f8f 100%);
        color: #ffffff;
        padding: 28px 30px;
        border-radius: 8px;
        margin-bottom: 18px;
        box-shadow: 0 18px 44px rgba(22, 33, 62, 0.20);
    }

    .hero h1 {
        color: #ffffff;
        font-size: 2.45rem;
        line-height: 1.08;
        margin: 0 0 8px 0;
        letter-spacing: 0;
    }

    .hero p {
        color: #dce8f6;
        font-size: 1.02rem;
        margin: 0;
        max-width: 720px;
    }

    .section-title {
        color: var(--ink);
        font-size: 1.22rem;
        font-weight: 800;
        margin: 22px 0 12px 0;
    }

    .metric-card,
    .example-card,
    .model-pill,
    .detail-item,
    .tip-list {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 10px 26px rgba(22, 33, 62, 0.08);
    }

    .metric-card {
        padding: 18px;
        min-height: 120px;
    }

    .metric-card.primary {
        border-color: rgba(15, 159, 143, 0.35);
        background: linear-gradient(180deg, #ffffff 0%, #edfdfa 100%);
    }

    .metric-card.warning {
        border-color: rgba(242, 169, 59, 0.38);
        background: linear-gradient(180deg, #ffffff 0%, #fff6e7 100%);
    }

    .metric-label,
    .detail-label {
        color: var(--muted);
        font-size: 0.84rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0;
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--ink);
        font-size: 1.85rem;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 8px;
    }

    .metric-note {
        color: var(--muted);
        font-size: 0.92rem;
    }

    .range-card {
        background: #16213e;
        color: #ffffff;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 14px;
        border-left: 5px solid var(--teal);
    }

    .range-card strong {
        color: #ffffff;
        font-size: 1.22rem;
    }

    .range-card p {
        color: #dce8f6;
        margin: 8px 0 0 0;
    }

    .factor-chip {
        display: inline-block;
        background: #eef6ff;
        color: #1f4e8c;
        border: 1px solid #cfe4ff;
        border-radius: 999px;
        padding: 7px 12px;
        margin: 0 8px 8px 0;
        font-weight: 650;
        font-size: 0.9rem;
    }

    .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .detail-item {
        padding: 14px;
    }

    .detail-value {
        color: var(--ink);
        font-size: 1.04rem;
        font-weight: 800;
    }

    .tip-list {
        padding: 16px 18px;
    }

    .tip-list li {
        margin: 8px 0;
    }

    .example-card {
        padding: 18px;
        min-height: 150px;
    }

    .example-card h3 {
        color: var(--ink);
        font-size: 1.08rem;
        margin: 0 0 10px 0;
    }

    .example-card .price {
        color: var(--teal);
        font-size: 1.35rem;
        font-weight: 850;
        margin-top: 8px;
    }

    .example-card p {
        color: var(--muted);
        margin: 5px 0;
    }

    .model-pill {
        padding: 15px;
        text-align: center;
    }

    .model-pill strong {
        color: var(--ink);
        display: block;
        font-size: 1.15rem;
    }

    .model-pill span {
        color: var(--muted);
        font-size: 0.86rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    @media (max-width: 720px) {
        .hero {
            padding: 22px;
        }

        .hero h1 {
            font-size: 1.9rem;
        }

        .detail-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_metric_card(label, value, note, card_class=""):
    st.markdown(
        f"""
        <div class="metric-card {card_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_example_card(title, year_text, price_text, kms_text, estimate_text):
    st.markdown(
        f"""
        <div class="example-card">
            <h3>{title}</h3>
            <p>{year_text}</p>
            <p>{price_text}</p>
            <p>{kms_text}</p>
            <div class="price">{estimate_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_model():
    try:
        return joblib.load("car_prediction_model.pkl")
    except FileNotFoundError:
        return None


st.markdown(
    """
    <div class="hero">
        <h1>Car Price Prediction System</h1>
        <p>Get a clean resale estimate using model-based pricing, vehicle age, mileage, fuel type, transmission, and ownership details.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

model = load_model()

if model is None:
    st.error("**Model file not found!**")
    st.info(
        """
        Please train and save the model first so that
        `car_prediction_model.pkl` is available in this project folder.
        """
    )
    st.stop()


st.sidebar.title("Car Details")

st.sidebar.markdown(
    '<div class="sidebar-section-title">Basic Information</div>',
    unsafe_allow_html=True,
)
year = st.sidebar.slider("Manufacturing Year", 2000, 2026, 2015)
present_price = st.sidebar.number_input(
    "Current Ex-showroom Price (Lakh)", 0.0, 50.0, 5.0, 0.1
)
kms_driven = st.sidebar.number_input("Kilometers Driven", 0, 500000, 50000, 1000)

st.sidebar.markdown(
    '<div class="sidebar-section-title">Car Specifications</div>',
    unsafe_allow_html=True,
)
fuel_type = st.sidebar.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
selling_type = st.sidebar.selectbox("Selling Type", ["Dealer", "Individual"])
transmission = st.sidebar.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.sidebar.selectbox("Number of Previous Owners", [0, 1, 2, 3])

current_year = 2026
car_age = current_year - year

st.sidebar.markdown("---")
predict_btn = st.sidebar.button(
    "Get Price Estimate", type="primary", use_container_width=True
)


if predict_btn:
    fuel_encoded = {"Petrol": 0, "Diesel": 1, "CNG": 2}[fuel_type]
    selling_encoded = {"Dealer": 0, "Individual": 1}[selling_type]
    transmission_encoded = {"Manual": 0, "Automatic": 1}[transmission]

    input_data = pd.DataFrame(
        {
            "Year": [year],
            "Present_Price": [present_price],
            "Driven_kms": [kms_driven],
            "Fuel_Type": [fuel_encoded],
            "Selling_type": [selling_encoded],
            "Transmission": [transmission_encoded],
            "Owner": [owner],
        }
    )

    predicted_price = model.predict(input_data)[0]
    depreciation = present_price - predicted_price
    depreciation_percent = (
        (depreciation / present_price) * 100 if present_price > 0 else 0
    )

    st.markdown(
        '<div class="section-title">Price Estimation Result</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card(
            "Estimated Selling Price",
            f"₹{predicted_price:.2f}L",
            "Model predicted market value",
            "primary",
        )

    with col2:
        render_metric_card(
            "Current Showroom Price",
            f"₹{present_price:.2f}L",
            "Original ex-showroom reference",
        )

    with col3:
        render_metric_card(
            "Total Depreciation",
            f"₹{depreciation:.2f}L",
            f"{depreciation_percent:.1f}% value drop",
            "warning",
        )

    st.markdown('<div class="section-title">Price Analysis</div>', unsafe_allow_html=True)

    analysis_col, gauge_col = st.columns([2, 1])

    with analysis_col:
        lower_estimate = predicted_price * 0.9
        upper_estimate = predicted_price * 1.1

        st.markdown(
            f"""
            <div class="range-card">
                <strong>Expected Price Range: ₹{lower_estimate:.2f}L - ₹{upper_estimate:.2f}L</strong>
                <p>This is the typical market range for similar vehicles.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        factors = []

        if car_age <= 2:
            factors.append("Very new car - minimal depreciation")
        elif car_age <= 5:
            factors.append("Relatively new - good resale value")
        elif car_age <= 10:
            factors.append("Moderate age - average market value")
        else:
            factors.append("Older car - higher depreciation")

        if kms_driven < 30000:
            factors.append("Low mileage - adds value")
        elif kms_driven < 80000:
            factors.append("Average mileage")
        else:
            factors.append("High mileage - reduces value")

        if transmission == "Automatic":
            factors.append("Automatic transmission - premium pricing")

        if fuel_type == "Diesel":
            factors.append("Diesel - preferred for high usage")
        elif fuel_type == "Petrol":
            factors.append("Petrol - standard option")

        if selling_type == "Dealer":
            factors.append("Dealer listing - may offer better warranty")

        st.markdown('<div class="metric-label">Price Factors</div>', unsafe_allow_html=True)
        st.markdown(
            "".join(f'<span class="factor-chip">{factor}</span>' for factor in factors),
            unsafe_allow_html=True,
        )

    with gauge_col:
        max_price = max(present_price * 1.2, predicted_price * 1.2, 1)

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=predicted_price,
                title={"text": "Estimated Price"},
                number={"prefix": "₹", "suffix": "L"},
                gauge={
                    "axis": {"range": [0, max_price]},
                    "bar": {"color": "#0f9f8f"},
                    "steps": [
                        {"range": [0, present_price * 0.3], "color": "#eef1f5"},
                        {
                            "range": [present_price * 0.3, present_price * 0.7],
                            "color": "#fff1c9",
                        },
                        {
                            "range": [present_price * 0.7, max_price],
                            "color": "#dff8f4",
                        },
                    ],
                    "threshold": {
                        "line": {"color": "#e74c3c", "width": 4},
                        "thickness": 0.75,
                        "value": present_price,
                    },
                },
            )
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#16213e"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Your Car Details</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="detail-grid">
            <div class="detail-item"><div class="detail-label">Manufacturing Year</div><div class="detail-value">{year}</div></div>
            <div class="detail-item"><div class="detail-label">Car Age</div><div class="detail-value">{car_age} years</div></div>
            <div class="detail-item"><div class="detail-label">Kilometers Driven</div><div class="detail-value">{kms_driven:,} km</div></div>
            <div class="detail-item"><div class="detail-label">Fuel Type</div><div class="detail-value">{fuel_type}</div></div>
            <div class="detail-item"><div class="detail-label">Transmission</div><div class="detail-value">{transmission}</div></div>
            <div class="detail-item"><div class="detail-label">Selling Type</div><div class="detail-value">{selling_type}</div></div>
            <div class="detail-item"><div class="detail-label">Previous Owners</div><div class="detail-value">{owner}</div></div>
            <div class="detail-item"><div class="detail-label">Showroom Price</div><div class="detail-value">₹{present_price:.2f} Lakhs</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Tips to Get Better Price</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="tip-list">
            <ul>
                <li>Keep service records ready.</li>
                <li>Clean the car before inspection.</li>
                <li>Compare similar listings before finalizing the price.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Enter your car details in the sidebar and click **Get Price Estimate**")

    st.markdown('<div class="section-title">Example Valuations</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        render_example_card(
            "Recent Car", "Year: 2020", "Price: ₹8.5L", "Kms: 20,000", "₹6.5L - ₹7.5L"
        )

    with col2:
        render_example_card(
            "Mid-range Car",
            "Year: 2015",
            "Price: ₹6.0L",
            "Kms: 50,000",
            "₹3.5L - ₹4.5L",
        )

    with col3:
        render_example_card(
            "Older Car", "Year: 2010", "Price: ₹5.0L", "Kms: 100,000", "₹1.5L - ₹2.5L"
        )

    st.markdown('<div class="section-title">Model Information</div>', unsafe_allow_html=True)
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown(
            '<div class="model-pill"><span>Algorithm</span><strong>ML Regression</strong></div>',
            unsafe_allow_html=True,
        )
    with info_col2:
        st.markdown(
            '<div class="model-pill"><span>Accuracy</span><strong>~85%</strong></div>',
            unsafe_allow_html=True,
        )
    with info_col3:
        st.markdown(
            '<div class="model-pill"><span>Dataset</span><strong>300+ cars</strong></div>',
            unsafe_allow_html=True,
        )
