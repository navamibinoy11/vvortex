import streamlit as st
import pandas as pd

# Import backend modules
from generate import generate_dataset
from train import train_model
from hosp import Person, predict_carrier, calculate_risk

# ===== GLOBAL PAGE CONFIG =====
st.set_page_config(
    page_title="Genetic Carrier ML Pipeline",
    page_icon="🧬",
    layout="wide"
)

# ===== GLOBAL STYLING =====
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)


st.title("🧬 Genetic Carrier Prediction Platform (Bayesian + ML)")

# ===== SESSION STATE INITIALIZATION =====
if "df" not in st.session_state:
    st.session_state.df = None

if "model" not in st.session_state:
    st.session_state.model = None

# ===== TABS =====
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Generate Dataset",
    "2️⃣ Train ML Model",
    "3️⃣ Predict Risk",
    "4️⃣ View Dataset"
])


# ==================== TAB 1: DATA GENERATION ====================
with tab1:
    st.header("📁 Generate Synthetic Genetic Dataset")

    rows = st.slider("Number of samples to generate:", 1000, 20000, 5000)

    if st.button("Generate Dataset"):
        df = generate_dataset(rows)
        st.session_state.df = df
        df.to_csv("synthetic_genetic_data.csv", index=False)
        st.success(f"Generated {rows} records & saved to synthetic_genetic_data.csv")
        st.dataframe(df.head())


# ==================== TAB 2: TRAIN ML MODEL ====================
with tab2:
    st.header("🤖 Train Machine Learning Model")

    if st.session_state.df is None:
        st.warning("Please generate dataset first in Step 1.")
    else:
        if st.button("Train Logistic Regression Model"):
            model, acc, auc, *_ = train_model()
            st.session_state.model = model
            st.success("Model trained successfully!")
            st.write(f"**Accuracy:** {acc:.4f}")
            st.write(f"**ROC-AUC Score:** {auc:.4f}")


# ==================== TAB 3: PREDICT RISK USING ML ====================
with tab3:
    st.header("🎯 Predict Carrier Risk Using ML Model")

    if st.session_state.model is None:
        st.warning("Train the model first in Step 2.")
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

        if st.button("Compute ML Risk Prediction"):
            # Create persons
            mother = Person("Mother", "female", mother_aff)
            father = Person("Father", "male", father_aff)
            child = Person("Child", child_gender, child_aff)

            # ML carrier probability predictions
            mother.carrier_prob = predict_carrier(
                mother, generation=2, affected_parent=maternal_gp,
                affected_sibling=sibling_aff, affected_child=child_aff
            )

            father.carrier_prob = predict_carrier(
                father, generation=2, affected_parent=paternal_gp,
                affected_sibling=sibling_aff, affected_child=child_aff
            )

            st.write(f"**Mother carrier probability:** {mother.carrier_prob*100:.2f}%")
            st.write(f"**Father carrier probability:** {father.carrier_prob*100:.2f}%")

            # Risk calculation
            risk, rule = calculate_risk(child, mother, father, inh)

            st.subheader("📌 Final Predicted Risk")
            st.success(f"**{risk*100:.2f}%** likelihood based on ML + inheritance rule")
            st.caption(f"Rule applied: {rule}")


# ==================== TAB 4: VIEW DATASET ====================
with tab4:
    st.header("📊 View or Download Latest Dataset")

    if st.session_state.df is None:
        st.info("Dataset not generated yet.")
    else:
        st.dataframe(st.session_state.df)

        csv = st.session_state.df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download Dataset as CSV",
            data=csv,
            file_name="synthetic_genetic_data.csv",
            mime="text/csv"
        )
