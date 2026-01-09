

# Person Class


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

def ask_yes_no(question):
    while True:
        ans = input(question + " (y/n): ").strip().lower()
        if ans in ("y", "n"):
            return ans == "y"
        print("Please enter y or n.")


# ----------------------------
# Bayesian Carrier Inference
# (Autosomal Recessive)
# ----------------------------

def infer_carrier_probability(person):
    """
    Bayesian inference using family history
    """

    # Case 1: Person affected
    if person.affected:
        return 1.0, "Person is affected → carrier probability = 1.0"

    # Case 2: Has affected child
    for child in person.children:
        if child.affected:
            return 1.0, "Affected child → parent must be a carrier"

    # Case 3: Affected sibling
    if person.mother:
        for sib in person.mother.children:
            if sib is not person and sib.affected:
                return 0.67, "Affected sibling → Bayesian posterior ≈ 0.67"

    # Case 4: Both parents carriers
    if person.mother and person.father:
        if (person.mother.carrier_prob == 1.0 and
                person.father.carrier_prob == 1.0):
            return 0.67, "Both parents carriers → posterior ≈ 0.67"

    # Case 5: No family history
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
    mother = child.mother
    father = child.father

    explanation = []

    if inheritance_type == "AR":
        m = mother.carrier_prob
        f = father.carrier_prob

        risk = m * f * 0.25

        explanation.append("Autosomal Recessive Inheritance")
        explanation.append("Child affected only if both parents pass allele")
        explanation.append(f"Risk = {m:.2f} × {f:.2f} × 0.25")

        return risk, explanation

    elif inheritance_type == "XL":
        risk, reason = x_linked_child_risk(mother, child.gender)
        explanation.append("X-Linked Inheritance")
        explanation.append(reason)
        return risk, explanation


# ----------------------------
# Explanation Printer
# ----------------------------

def explain_person(person):
    prob, reason = infer_carrier_probability(person)
    person.carrier_prob = prob

    print(f"{person.name} ({person.gender})")
    print(f"  Affected: {person.affected}")
    print(f"  Carrier probability: {prob*100:.2f}%")
    print(f"  Reason: {reason}\n")


# ----------------------------
# MAIN PROGRAM
# ----------------------------

def main():
    print("\n===== BAYESIAN GENETIC INHERITANCE ANALYSIS =====\n")

    # -------- Generation 1 --------
    print("Enter family history (3 generations)\n")

    gm_aff = ask_yes_no("Is the grandmother affected?")
    gf_aff = ask_yes_no("Is the grandfather affected?")

    grandmother = Person("Grandmother", "female", gm_aff)
    grandfather = Person("Grandfather", "male", gf_aff)

    # -------- Generation 2 --------
    m_aff = ask_yes_no("Is the mother affected?")
    f_aff = ask_yes_no("Is the father affected?")

    mother = Person("Mother", "female", m_aff)
    father = Person("Father", "male", f_aff)

    mother.mother = grandmother
    mother.father = grandfather

    grandmother.children.append(mother)
    grandfather.children.append(mother)

    # -------- Generation 3 --------
    gender = input("Enter child gender (male/female): ").strip().lower()
    child_aff = ask_yes_no("Is the child affected?")

    child = Person("Child", gender, child_aff)
    child.mother = mother
    child.father = father

    mother.children.append(child)
    father.children.append(child)

    # -------- Bayesian Inference --------
    print("\n**Carrier Probability Inference **\n")

    explain_person(grandmother)
    explain_person(grandfather)
    explain_person(mother)
    explain_person(father)

    # -------- Risk Estimation --------
    inheritance_type = input("Enter inheritance type (AR / XL): ").strip().upper()

    print("\n** Child Risk Estimation **")

    risk, explanation = calculate_child_risk(child, inheritance_type)

    print(f"Child gender: {child.gender}")
    print(f"Inheritance type: {inheritance_type}\n")

    for line in explanation:
        print(" ", line)

    print(f"\nFinal Risk of Child Being Affected: {risk*100:.2f}%")
    print("\n================================================\n")


# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    main()
