import streamlit as st

# ===== GLOBAL PAGE CONFIG =====
st.set_page_config(
    page_title="Bayesian Genetic Risk Estimation",
    page_icon="🧬",
    layout="wide"
)

# ===== GLOBAL STYLING =====


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    background: #EAF6F6 !important;
}

h1, h2, h3 {
    color: #1B9AAA !important;
}

button[kind="primary"] {
    background-color: #1B9AAA !important;
    color: white !important;
    border-radius: 6px !important;
    font-size: 16px !important;
}

.streamlit-expanderHeader {
    color: #1B9AAA !important;
}

.streamlit-expander {
    background: #FFFFFF !important;
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)


button[kind="primary"] {
    background-color: #6A5ACD !important;
    color: white !important;
    border-radius: 8px !important;
}

.streamlit-expander {
    background: #FFF4DC !important;
    border-radius: 10px !important;
    margin-bottom:


# ===== BANNER =====
st.markdown(
    f"""
    <style>
    .banner {{
        width: 100%;
        height: 260px;
        background-image: linear-gradient(
            rgba(255, 255, 255, 0.2),
            rgba(250, 235, 215, 0.7)
        ), url("YOUR_RAW_GITHUB_BANNER_LINK_HERE");
        background-size: cover;
        background-position: center;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px;
    }}
    .banner h1 {{
        font-size: 50px;
        color: #4B0082;
        text-shadow: 1px 1px 4px #fff;
        font-weight: 600;
    }}
    </style>
    <div class="banner">
        <h1>Bayesian Genetic Risk Estimation</h1>
    </div>
    """,
    unsafe_allow_html=True
)

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


def x_linked_child_risk(mother, child_gender):
    if mother.affected:
        return 1.0, "Mother affected → 100% risk"
    if child_gender == "male":
        return mother.carrier_prob, "Male inherits X chromosome from mother"
    else:
        return mother.carrier_prob * 0.5, "Female has 50% chance from mother"


def calculate_child_risk(child, inheritance_type):
    explanation = []
    if inheritance_type == "AR":
        m = child.mother.carrier_prob
        f = child.father.carrier_prob
        risk = m * f * 0.25
        explanation += [
            "Autosomal Recessive Inheritance",
            "Child affected only if both parents pass allele",
            f"Risk = {m:.2f} × {f:.2f} × 0.25"
        ]
        return risk, explanation

    elif inheritance_type == "XL":
        risk, reason = x_linked_child_risk(child.mother, child.gender)
        explanation += ["X-Linked Inheritance", reason]
        return risk, explanation


# ===== MAIN CONTENT =====
st.caption("For educational use • Not medical advice 🧑‍⚕️")

st.header("👨‍👩‍👧 Family History Input")

col1, col2 = st.columns(2)

with col1:
    gm_aff = st.checkbox("Grandmother affected")
    m_aff = st.checkbox("Mother affected")

with col2:
    gf_aff = st.checkbox("Grandfather affected")
    f_aff = st.checkbox("Father affected")

child_gender = st.selectbox("Child gender:", ["male", "female"])
child_aff = st.checkbox("Child affected")
inheritance_type = st.selectbox("Inheritance type:", ["AR", "XL"])

if st.button("Calculate Risk"):
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

    st.subheader("📊 Carrier Probability Inference")
    for p in [grandmother, grandfather, mother, father]:
        prob, reason = infer_carrier_probability(p)
        p.carrier_prob = prob
        st.write(f"**{p.name}**: {prob*100:.2f}% — {reason}")

    risk, explanation = calculate_child_risk(child, inheritance_type)

    st.subheader("🎯 Child Risk Result")
    for line in explanation:
        st.write("•", line)

    st.success(f"Final estimated risk: **{risk*100:.2f}%**")


# ===== EXPANDERS (INFO BOXES) =====
st.header("📖 Genetic Inheritance Concepts")

with st.expander("How Does Bayesian Analysis Work?"):
    st.write("""
    Bayesian analysis updates a probability after considering new evidence.
    Posterior = (Prior × Likelihood) / Evidence.
    """)

with st.expander("Autosomal Recessive Inheritance"):
    st.write("""
    A person must inherit two mutated alleles (one from each parent) to be affected.
    Examples: cystic fibrosis, Tay-Sachs disease.
    """)

with st.expander("X-Linked Inheritance"):
    st.write("""
    Mutations occur on the X chromosome. Males are often more affected as they have one X chromosome.
    """)

with st.expander("Carrier Status"):
    st.write("""
    A carrier has one mutated and one normal allele. Carriers typically show no symptoms.
    """)

with st.expander("How to Interpret Your Results"):
    st.write("""
    The final percentage reflects updated genetic risk based on family history.
    """)


# ===== FOOTER =====
st.markdown("""
<hr>
<div style='text-align:center; color:grey;'>
Made with ❤️ for educational genetics visualization.
</div>
""", unsafe_allow_html=True)







