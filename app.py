import streamlit as st
import pandas as pd
import subprocess
import os

from train import train_model
from hosp import Person, predict_carrier, calculate_risk

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Genetic Carrier ML Pipeline",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Genetic Carrier Prediction Platform (ML-Powered)")

# =====================
# SESSION STATE SETUP
# =====================
if "df" not in st.session_state:
    st.session_state.df = None

if "model" not in st.session_state:
    st.session_state.model = None


# =====================
# TABS
# =====================
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Generate Dataset",
    "2️⃣ Train ML Model",
    "3️⃣ Predict Risk",
    "4️⃣ View Dataset"
])


# =====================
# TAB 1 — DATA GENERATION
# =====================
with tab1:
    st.header("📁 Generate Synthetic Genetic Dataset")

    rows = st.slider("Number of rows:", 1000, 20000, 5000)

    if st.button("Generate Dataset"):
        # Run generate.py as script
        st.write("Generating dataset...")

        # Pass row count as argument
        subprocess.run(["python3", "generate.py"], check=True)

        if os.path.exists("synthetic_genetic_data.csv"):
            df = pd.read_csv("synthetic_genetic_data.csv")
            st.session_state.df = df
            st.success("Dataset created successfully!")
            st.dataframe(df.head())
        else:
            st.error("Dataset not found. Ensure generate.py saves CSV as 'synthetic_genetic_data.csv'.")


# =====================
# TAB 2 — TRAIN MODEL
# =====================
with tab2:
    st.header("🤖 Train ML Model")

    if st.session_state.df is None:
        st.warning("Generate dataset first.")
    else:
        if st.button("Train Model"):
            model, acc, auc, *_ = train_model()
            st.session_state.model = model
            st.success("Model Trained Successfully!")
            st.write(f"**Accuracy:** {acc:.3f}")
            st.write(f"**ROC-AUC:** {auc:.3f}")


# =====================
# TAB 3 — INFERENCE (ML + RISK)
# =====================
with tab3:
    st.header("🎯 ML-Based Carrier Risk Prediction")

    if st.session_state.model is None:
        st.warning("Train the model first.")
    else:
        st.subheader("Family History Input")

        col1, col2 = st.columns(2)

        with col1:
            mother_aff = st.checkbox("Mother affected?")
            maternal_gp = st.checkbox("Maternal grandparent affected?")
            sibling_aff = st.checkbox("Sibling affected?")

        with col2:
            father_aff = st.checkbox("Father affected?")
            paternal_gp = st.checkbox("Paternal grandparent affected?")
            child_aff = st.checkbox("Child affected?")

        child_gender = st.selectbox("Child gender:", ["male", "female"])
        inh = st.selectbox("Inheritance pattern:", ["AR", "AD", "XL"])

        if st.button("Predict Risk"):
            mother = Person("Mother", "female", mother_aff)
            father = Person("Father", "male", father_aff)
            child = Person("Child", child_gender, child_aff)

            # ML carrier probabilities
            mother.carrier_prob = predict_carrier(
                mother, 2, maternal_gp, sibling_aff, child_aff
            )
            father.carrier_prob = predict_carrier(
                father, 2, paternal_gp, sibling_aff, child_aff
            )

            st.write(f"**Mother carrier probability:** {mother.carrier_prob*100:.2f}%")
            st.write(f"**Father carrier probability:** {father.carrier_prob*100:.2f}%")

            # Genetic risk estimate
            risk, rule = calculate_risk(child, mother, father, inh)
            st.subheader("📌 Final Genetic Risk Prediction")
            st.success(f"Estimated child risk: **{risk*100:.2f}%**")
            st.caption(f"Rule applied: {rule}")


# =====================
# TAB 4 — DATA VIEWER
# =====================
with tab4:
    st.header("📊 View Synthetic Dataset")

    if st.session_state.df is None:
        st.info("No dataset loaded.")
    else:
        st.dataframe(st.session_state.df)

        csv = st.session_state.df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Dataset CSV",
            csv,
            "synthetic_genetic_data.csv",
            "text/csv"
        )
