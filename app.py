import streamlit as st
from hosp import Person, predict_carrier, calculate_risk

st.set_page_config(page_title="Genetic ML Risk", page_icon="🧬", layout="wide")
st.title("🧬 Genetic Carrier & Risk Predictor (Pretrained Model)")

st.write("This model runs fully in the browser using a pretrained machine learning classifier.")

# Family history input UI
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

    mother.carrier_prob = predict_carrier(mother, 2, maternal_gp, sibling_aff, child_aff)
    father.carrier_prob = predict_carrier(father, 2, paternal_gp, sibling_aff, child_aff)

    st.subheader("Carrier Probabilities")
    st.write(f"Mother: **{mother.carrier_prob*100:.2f}%**")
    st.write(f"Father: **{father.carrier_prob*100:.2f}%**")

    risk, rule = calculate_risk(child, mother, father, inh)

    st.subheader("Estimated Child Risk")
    st.success(f"Final risk: **{risk*100:.2f}%**")
    st.caption(f"Rule: {rule}")

