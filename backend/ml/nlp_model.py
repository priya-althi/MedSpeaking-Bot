import os
import pickle
import pandas as pd
import re
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, "medical_clean.csv"))

def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["clean_question"] = df["Symptoms/Question"].apply(clean)

print("Loading sentence transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = df["clean_question"].tolist()
embeddings = model.encode(sentences, show_progress_bar=True)

with open(os.path.join(BASE_DIR, "symptom_embeddings.pkl"), "wb") as f:
    pickle.dump(embeddings, f)

print("✅ Symptom embeddings saved successfully.")
