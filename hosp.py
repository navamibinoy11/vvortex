import joblib
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# ------------------------------------------------------------
# Load trained ML model
# ------------------------------------------------------------

model = joblib.load("carrier_model.pkl")


# ------------------------------------------------------------
# Person class
# ------------------------------------------------------------

class Person:
    def __init__(self, name, gender, affected):
        self.name = name
        self.gender = gender
        self.affected = affected
        self.carrier_prob = 0.0


# ------------------------------------------------------------
# Input helpers
# ------------------------------------------------------------

def ask_yes_no(q):
    return input(q + " (y/n): ").strip().lower() == "y"


# ------------------------------------------------------------
# Convert family history to ML features
# ------------------------------------------------------------

def get_features(person, generation, affected_parent, affected_sibling, affected_child):
    """
    Feature order MUST match training:
    affected_self, affected_parent, affected_sibling, affected_child, generation
    """
    return [[
        int(person.affected),
        int(affected_parent),
        int(affected_sibling),
        int(affected_child),
        generation
    ]]


def predict_carrier(person, generation, affected_parent, affected_sibling, affected_child):
    features = get_features(
        person, generation, affected_parent, affected_sibling, affected_child
    )
    return model.predict_proba(features)[0][1]


# ------------------------------------------------------------
# Risk calculation (AR / AD / XL)
# ------------------------------------------------------------

def calculate_risk(child, mother, father, inh):
    if inh == "AR":
        risk = mother.carrier_prob * father.carrier_prob * 0.25
        rule = "Autosomal Recessive: m × f × 0.25"

    elif inh == "AD":
        risk = 1 - ((1 - mother.carrier_prob) * (1 - father.carrier_prob))
        rule = "Autosomal Dominant: 1 − (1−m)(1−f)"

    elif inh == "XL":
        if child.gender == "male":
            risk = mother.carrier_prob
            rule = "X-linked (male): depends only on mother"
        else:
            risk = mother.carrier_prob * 0.5
            rule = "X-linked (female): mother × 0.5"

    else:
        raise ValueError("Invalid inheritance type")

    return risk, rule


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

def predict_from_inputs(
    gm_aff, gf_aff,
    mother_aff, father_aff,
    sibling_aff,
    child_gender, child_aff,
    inheritance_type
):
    mother = Person("Mother", "female", mother_aff)
    father = Person("Father", "male", father_aff)
    child = Person("Child", child_gender, child_aff)

    mother.carrier_prob = predict_carrier(
        mother, generation=2,
        affected_parent=(gm_aff or gf_aff),
        affected_sibling=False,
        affected_child=child_aff
    )

    father.carrier_prob = predict_carrier(
        father, generation=2,
        affected_parent=False,
        affected_sibling=False,
        affected_child=child_aff
    )

    risk, rule = calculate_risk(child, mother, father, inheritance_type)

    return {
        "mother_prob": mother.carrier_prob,
        "father_prob": father.carrier_prob,
        "risk": risk,
        "rule": rule
    }


def main():
    print("\n=== ML-BASED GENETIC RISK PREDICTOR (3 GENERATIONS) ===\n")

    # ---------------- GRANDPARENTS ----------------
    print("Enter GRANDPARENTS information")
    gm_aff = ask_yes_no("Is maternal grandmother affected?")
    gf_aff = ask_yes_no("Is maternal grandfather affected?")

    affected_parent_mother = gm_aff or gf_aff

    # ---------------- PARENTS ----------------
    print("\nEnter PARENTS information")
    mother = Person("Mother", "female", ask_yes_no("Is mother affected?"))
    father = Person("Father", "male", ask_yes_no("Is father affected?"))

    affected_parent_father = ask_yes_no("Is any paternal grandparent affected?")

    # ---------------- CHILD ----------------
    print("\nEnter CHILD information")
    child_gender = input("Enter child gender (male/female): ").strip().lower()
    child = Person("Child", child_gender, ask_yes_no("Is child affected?"))

    # ---------------- SIBLING HISTORY ----------------
    affected_sibling = ask_yes_no("Does the child have any affected siblings?")

    # ---------------- ML CARRIER PREDICTION ----------------
    mother.carrier_prob = predict_carrier(
        mother, generation=2,
        affected_parent=affected_parent_mother,
        affected_sibling=False,
        affected_child=child.affected
    )

    father.carrier_prob = predict_carrier(
        father, generation=2,
        affected_parent=affected_parent_father,
        affected_sibling=False,
        affected_child=child.affected
    )

    print("\nCarrier probabilities (from ML):")
    print(f"Mother: {mother.carrier_prob*100:.2f}%")
    print(f"Father: {father.carrier_prob*100:.2f}%")

    # ---------------- RISK ESTIMATION ----------------
    inh = input("\nEnter inheritance type (AR / AD / XL): ").strip().upper()

    risk, rule = calculate_risk(child, mother, father, inh)

    print("\nRule used:", rule)
    print(f"FINAL PREDICTED RISK: {risk*100:.2f}%")
    print("\n===============================================\n")

    


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
    
