import streamlit as st
import pandas as pd
from hosp import Person, predict_carrier, calculate_risk
import joblib

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Genetic Carrier Risk Predictor",
    page_icon="🧬",
    layout="wide"
)

# ============================================================
# LOAD TRAINED MODEL (REQUIRED FOR sklearn-BASED PREDICTIONS)
# ============================================================
try:
    model = joblib.load("carrier_model.pkl")
    st.session_state['model_loaded'] = True
except:
    st.session_state['model_loaded'] = False

# ============================================================
# UI HEADER
# ============================================================
st.title("🧬 Genetic Carrier & Inheritance Risk Predictor (ML + sklearn)")
st.caption("This model uses a pretrained Logistic Regression classifier (sklearn) to estimate carrier probability.")

# ============================================================
# UI INPUTS FOR FAMILY HISTORY
# ============================================================

col1, col2 = st.columns(2)

with col1:
    mother_aff = st.checkbox("Mother affected?")
    maternal_gp = st.checkbox("Maternal grandparent affected?")
    sibling_aff = st.checkbox("Sibling affected?")

with col2:
    father_aff = st.checkbox("Father affected?")
    paternal_gp = st.checkbox("Paternal grandparent affected?")
    child_aff = st.checkbox("Child affected?")

child_gender = st.selectbox("Child gender", ["male", "female"])
inh = st.selectbox("Inheritance pattern", ["AR", "AD", "XL"])

# ============================================================
# PREDICTION SECTION
# ============================================================

st.subheader("🔍 Prediction Output")

if not st.session_state['model_loaded']:
    st.error("❗ ERROR: carrier_model.pkl not found — train your model first using train.py")
else:
    if st.button("Predict Risk"):
        # Create person objects
        mother = Person("Mother", "female", mother_aff)
        father = Person("Father", "male", father_aff)
        child = Person("Child", child_gender, child_aff)

        # Predict carrier probabilities using sklearn model
        mother.carrier_prob = predict_carrier(
            mother, generation=2,
            affected_parent=maternal_gp,
            affected_sibling=sibling_aff,
            affected_child=child_aff
        )

        father.carrier_prob = predict_carrier(
            father, generation=2,
            affected_parent=paternal_gp,
            affected_sibling=sibling_aff,
            affected_child=child_aff
        )

        # Display carrier results
        st.subheader("🧪 Carrier Probabilities (sklearn)")
        st.write(f"Mother carrier probability: **{mother.carrier_prob*100:.2f}%**")
        st.write(f"Father carrier probability: **{father.carrier_prob*100:.2f}%**")

        # Risk based on inheritance rules
        risk, rule = calculate_risk(child, mother, father, inh)

        # Display final child risk
        st.subheader("👶 Estimated Child Genetic Risk")
        st.success(f"Estimated risk: **{risk*100:.2f}%**")
        st.caption(f"Rule applied: {rule}")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<hr>
<div style='text-align:center; color: gray;'>
Model trained using scikit-learn LogisticRegression • For educational purposes only.
</div>
""", unsafe_allow_html=True)
