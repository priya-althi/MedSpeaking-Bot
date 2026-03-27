import pandas as pd
import re

df = pd.read_csv("medical_dataset.csv")

def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()  # remove extra spaces
    return text

df["clean_question"] = df["Symptoms/Question"].apply(clean)

df.to_csv("medical_clean.csv", index=False)
print("Preprocessing done. Duplicates removed. medical_clean.csv saved.")
