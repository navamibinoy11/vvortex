import streamlit as st
from hosp import predict_from_inputs

st.set_page_config(page_title="Genetic Risk Predictor", layout="centered")

st.title("🧬 Genetic Risk Prediction System")
st.write("ML-based carrier prediction + Mendelian inheritance")

st.header("Family History Input")

col1, col2 = st.columns(2)

with col1:
    gm_aff = st.checkbox("Maternal Grandmother affected")
    gf_aff = st.checkbox("Maternal Grandfather affected")

with col2:
    mother_aff = st.checkbox("Mother affected")
    father_aff = st.checkbox("Father affected")

sibling_aff = st.checkbox("Affected sibling present")

st.header("Child Information")
child_gender = st.selectbox("Child Gender", ["male", "female"])
child_aff = st.checkbox("Child affected")

inheritance_type = st.selectbox(
    "Inheritance Type",
    ["AR", "AD", "XL"]
)

if st.button("Predict Risk"):
    result = predict_from_inputs(
        gm_aff, gf_aff,
        mother_aff, father_aff,
        sibling_aff,
        child_gender, child_aff,
        inheritance_type
    )

    st.subheader("Results")

    st.write(f"**Mother carrier probability:** {result['mother_prob']*100:.2f}%")
    st.write(f"**Father carrier probability:** {result['father_prob']*100:.2f}%")

    st.markdown("---")
    st.write(f"**Rule used:** {result['rule']}")
    st.success(f"**Final predicted risk:** {result['risk']*100:.2f}%")
