




import streamlit as st

css = """
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

/* Change global font */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Header style */
h1, h2, h3 {
    color: #1e3d58;
    font-weight: 600;
}

/* Container styling */
div.block-container {
    padding: 2rem 3rem;
    background: #f7f9fc;
    border-radius: 10px;
}

/* Buttons */
button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    border: none !important;
    transition: all 0.2s ease;
}

button[kind="primary"]:hover {
    transform: scale(1.04);
    background-color: #1d4ed8 !important;
}

/* Input boxes */
input, textarea {
    border-radius: 8px !important;
}

/* Tables */
table {
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
}

/* Hide footer & menu if desired */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
"""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


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
        st.write(f"**{p.name}**: {prob*100:.2f}% — {reason}")

    # Calculate child risk
    risk, explanation = calculate_child_risk(child, inheritance_type)

    st.subheader("Child Risk Result")
    for line in explanation:
        st.write("•", line)

    st.success(f"Final estimated risk: **{risk*100:.2f}%**")

