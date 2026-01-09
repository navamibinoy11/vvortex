




import streamlit as st

st.set_page_config(page_title="Bayesian Genetic Risk App", layout="wide")

# ---------- CSS FOR ANIMATION ----------
st.markdown("""
<style>
.slide-in {
  animation: slideIn 1s ease-out;
}
@keyframes slideIn {
  from { transform: translateY(50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)








# ============================================================
# BAYESIAN GENETIC INHERITANCE MODEL (WEB VERSION)
# ============================================================

class Person:
    def __init__(self, name, gender, affected=False):
        self.name = name
        self.gender = gender
        self.affected = affected
        self.mother = None
        self.father = None
        self.children = []
        self.carrier_prob = None


POPULATION_CARRIER_RATE = 0.02


# ----------------------------
# Bayesian Carrier Inference
# ----------------------------
def infer_carrier_probability(person):
    if person.affected:
        return 1.0, "Person is affected → carrier probability = 100%"

    for child in person.children:
        if child.affected:
            return 1.0, "Affected child → parent must be a carrier"

    if person.mother:
        for sib in person.mother.children:
            if sib is not person and sib.affected:
                return 0.67, "Affected sibling → posterior ≈ 67%"

    return POPULATION_CARRIER_RATE, "No family history → population prior"


# ----------------------------
# X-Linked Risk
# ----------------------------
def x_linked_child_risk(mother, child_gender):
    if mother.affected:
        return 1.0, "Mother affected → 100% risk"

    if child_gender == "male":
        return mother.carrier_prob, "Male inherits X chromosome from mother"
    else:
        return mother.carrier_prob * 0.5, "Female has 50% chance from mother"


# ----------------------------
# Child Risk Calculation
# ----------------------------
def calculate_child_risk(child, inheritance_type):
    explanation = []

    if inheritance_type == "AR":
        m = child.mother.carrier_prob
        f = child.father.carrier_prob
        risk = m * f * 0.25
        explanation.append("Autosomal Recessive Inheritance")
        explanation.append("Child affected only if both parents pass allele")
        explanation.append(f"Risk = {m:.2f} × {f:.2f} × 0.25")
        return risk, explanation

    elif inheritance_type == "XL":
        risk, reason = x_linked_child_risk(child.mother, child.gender)
        explanation.append("X-Linked Inheritance")
        explanation.append(reason)
        return risk, explanation


# ============================================================
# STREAMLIT USER INTERFACE
# ============================================================

st.title("Bayesian Genetic Risk Estimation")
st.caption("Educational model • Not medical advice")

st.header("Family History Input")

gm_aff = st.checkbox("Grandmother affected")
gf_aff = st.checkbox("Grandfather affected")

m_aff = st.checkbox("Mother affected")
f_aff = st.checkbox("Father affected")

child_gender = st.selectbox("Child gender", ["male", "female"])
child_aff = st.checkbox("Child affected")

inheritance_type = st.selectbox("Inheritance type", ["AR", "XL"])

if st.button("Calculate Risk"):

    # Build family tree
    grandmother = Person("Grandmother", "female", gm_aff)
    grandfather = Person("Grandfather", "male", gf_aff)

    mother = Person("Mother", "female", m_aff)
    father = Person("Father", "male", f_aff)

    child = Person("Child", child_gender, child_aff)

    mother.mother = grandmother
    mother.father = grandfather
    grandmother.children.append(mother)
    grandfather.children.append(mother)

    child.mother = mother
    child.father = father
    mother.children.append(child)
    father.children.append(child)

    # Infer carrier probabilities
    st.subheader("Carrier Probability Inference")
    for p in [grandmother, grandfather, mother, father]:
        prob, reason = infer_carrier_probability(p)
        p.carrier_prob = prob
        st.markdown(f'''
<div class="slide-in" style="font-size: 24px; font-weight: bold; color: #0b3d91;">
Final Risk of Child Being Affected: {risk*100:.2f}%
</div>
''', unsafe_allow_html=True)

    # Calculate child risk
    risk, explanation = calculate_child_risk(child, inheritance_type)

    st.subheader("Child Risk Result")
    for line in explanation:
        st.write("•", line)

    st.success(f"Final estimated risk: **{risk*100:.2f}%**")

