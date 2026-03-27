import pandas as pd
import re

# Load cleaned dataset
df = pd.read_csv("medical_clean.csv")

# Basic symptom vocabulary (you can extend later)
SYMPTOM_KEYWORDS = [
    "fever","headache","pain","stomach","abdomen","gas","acid","vomit","diarrhea",
    "cough","cold","sneeze","breath","chest","heart","bp","pressure",
    "tooth","teeth","gum","mouth","jaw",
    "eye","vision","blur","red","itch","ear","nose","throat",
    "skin","rash","itching","acne",
    "weight","obese","fat","tired","fatigue","weak",
    "urine","burning","infection","swelling","joint","knee","back","neck",
    "sleep","stress","anxiety","period","cramps"
]

def extract_tags(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z ]', '', text)
    words = set(text.split())

    tags = set()
    for w in words:
        if w in SYMPTOM_KEYWORDS:
            tags.add(w)

    return ",".join(sorted(tags))

# Create new column
df["symptom_tags"] = df["Symptoms/Question"].apply(extract_tags)

# Save new dataset
df.to_csv("medical_tagged.csv", index=False)

print("✅ symptom_tags added. File saved as medical_tagged.csv")
