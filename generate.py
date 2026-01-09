import random
import pandas as pd

def generate_individual():
    # Simulate family carrier status
    parent1_carrier = random.choice([0, 1])
    parent2_carrier = random.choice([0, 1])

    # Child carrier probability (autosomal recessive)
    if parent1_carrier and parent2_carrier:
        carrier = 1 if random.random() < 0.67 else 0
    elif parent1_carrier or parent2_carrier:
        carrier = 1 if random.random() < 0.50 else 0
    else:
        carrier = 0

    # Disease occurs only if carrier (simplified assumption)
    affected_self = 1 if carrier and random.random() < 0.25 else 0

    # Family disease history
    affected_parent = 1 if (parent1_carrier or parent2_carrier) and random.random() < 0.30 else 0
    affected_sibling = 1 if carrier and random.random() < 0.20 else 0
    affected_child = 1 if carrier and random.random() < 0.15 else 0

    generation = random.choice([1, 2, 3])

    return {
        "affected_self": affected_self,
        "affected_parent": affected_parent,
        "affected_sibling": affected_sibling,
        "affected_child": affected_child,
        "generation": generation,
        "carrier": carrier   # LABEL
    }

# Generate dataset
data = [generate_individual() for _ in range(10000)]
df = pd.DataFrame(data)

# Save dataset
df.to_csv("synthetic_genetic_data.csv", index=False)

print(df.head())