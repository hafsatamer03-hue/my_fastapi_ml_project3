import requests
import streamlit as st

API_URL = "https://iris-fastapi-ml-dxducedrhtfsepbt.italynorth-01.azurewebsites.net"

st.set_page_config(
    page_title="Iris AI Predictor",
    page_icon="🌸",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #fff7fb 100%);
}

.main-card {
    background: white;
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.title {
    font-size: 48px;
    font-weight: 800;
    color: #1f2937;
    text-align: center;
}

.subtitle {
    font-size: 18px;
    color: #6b7280;
    text-align: center;
    margin-bottom: 30px;
}

.result-box {
    background: linear-gradient(135deg, #6366f1, #ec4899);
    color: white;
    padding: 25px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0px 10px 25px rgba(99,102,241,0.25);
}

.result-title {
    font-size: 20px;
    opacity: 0.9;
}

.result-class {
    font-size: 42px;
    font-weight: 800;
}

.small-note {
    color: #6b7280;
    font-size: 14px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌸 Iris Flower AI Predictor</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>A creative Streamlit frontend connected to a FastAPI ML model deployed on Azure</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("🌿 Enter Flower Measurements")

    sepal_length = st.slider("Sepal Length", 0.1, 10.0, 5.1, 0.1)
    sepal_width = st.slider("Sepal Width", 0.1, 10.0, 3.5, 0.1)
    petal_length = st.slider("Petal Length", 0.1, 10.0, 1.4, 0.1)
    petal_width = st.slider("Petal Width", 0.1, 10.0, 0.2, 0.1)

    predict_button = st.button("🔮 Predict Flower Type", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("📌 Current Input")

    st.write({
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    })

    st.markdown("### 🌐 API Status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=10)
        if health.status_code == 200:
            st.success("FastAPI Backend is running")
        else:
            st.warning("API responded but may have an issue")
    except Exception:
        st.error("Could not connect to FastAPI API")

    st.markdown("</div>", unsafe_allow_html=True)

if predict_button:
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=15)

        if response.status_code == 200:
            result = response.json()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class='result-box'>
                    <div class='result-title'>Predicted Flower Class</div>
                    <div class='result-class'>🌸 {result["prediction_class"].title()}</div>
                    <div>Prediction Number: {result["prediction_number"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### 📊 Prediction Probabilities")
            probabilities = result["probabilities"]

            for flower, probability in probabilities.items():
                st.write(f"**{flower.title()}**")
                st.progress(probability)

            st.markdown("### 🧾 Full API Response")
            st.json(result)

        else:
            st.error("API Error")
            st.write(response.text)

    except Exception as error:
        st.error("Connection Error")
        st.write(error)

st.markdown("---")
st.markdown(
    "<div class='small-note'>Built with Streamlit + FastAPI + Azure App Service</div>",
    unsafe_allow_html=True
)