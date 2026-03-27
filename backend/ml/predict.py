import os
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "medical_tagged.csv"))

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- TEXT CLEANING ----------------
def clean(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ---------------- EMERGENCY CHECK ----------------
def emergency_check(text):
    text = text.lower()

    emergency_keywords = [
        "vomiting blood",
        "blood in vomit",
        "black stool",
        "black stools",
        "chest pain",
        "left arm pain",
        "arm numb",
        "face drooping",
        "slurred speech",
        "vision loss",
        "unconscious",
        "seizure",
        "fracture",
        "heavy bleeding",
        "accident"
    ]

    for keyword in emergency_keywords:
        if keyword in text:
            return True

    return False


# ---------------- MAIN FUNCTION ----------------
def get_medical_response(user_text):

    user_text = clean(user_text)

    # ==================================================
    # 🔴 STEP 1: EMERGENCY CHECK (HIGHEST PRIORITY)
    # ==================================================
    if emergency_check(user_text):
        return {
            "status": "final",
            "disease": "Possible Medical Emergency",
            "medicine": "Immediate Medical Attention Required",
            "advice": "Your symptoms may indicate a serious condition. Please consult a doctor or visit the nearest hospital immediately."
        }

    # ==================================================
    # 🔵 STEP 2: RULE-BASED COMMON CONDITIONS
    # ==================================================


# ---- STOMACH ----
    if any(p in user_text for p in ["stomach pain", "stomach ache", "belly pain", "abdominal pain"]):
        return {
        "status": "final",
        "disease": "Indigestion / Gastritis",
        "medicine": "Antacids, Omeprazole",
        "advice": "Eat light meals, avoid spicy food, and drink warm fluids. See doctor if pain continues."
    }

    if any(p in user_text for p in ["vomiting", "loose motions", "diarrhea"]):
        return {
        "status": "final",
        "disease": "Food Poisoning / Stomach Infection",
        "medicine": "ORS, Ondansetron",
        "advice": "Drink ORS and avoid outside food. Consult doctor if severe."
    }

    if any(p in user_text for p in ["gas", "bloating", "acidity", "heartburn"]):
        return {
        "status": "final",
        "disease": "Acidity / Gas",
        "medicine": "Antacids, Simethicone",
        "advice": "Avoid oily food and carbonated drinks. Eat slowly."
    }

# ---- GENERAL SICK FEELING ----
    if any(p in user_text for p in ["feeling sick", "not feeling well", "nausea", "weak and sick"]):
        return {
        "status": "final",
        "disease": "Viral Infection / General Illness",
        "medicine": "Paracetamol, ORS",
        "advice": "Take rest, drink fluids, and consult doctor if symptoms worsen."
    }

# ---- FEVER ----
    if any(p in user_text for p in ["fever", "temperature", "high fever"]):
        return {
        "status": "final",
        "disease": "Viral Fever",
        "medicine": "Paracetamol",
        "advice": "Drink fluids and take rest. See doctor if fever lasts more than 2 days."
    }

# ---- HEADACHE ----
    if "headache" in user_text:
        return {
        "status": "final",
        "disease": "Headache / Migraine",
        "medicine": "Paracetamol",
        "advice": "Rest in a quiet place and reduce screen time."
    }

# ---- DENTAL ----
    if any(p in user_text for p in ["gum", "tooth", "teeth", "mouth"]):
        return {
        "status": "final",
        "disease": "Dental / Gum Infection",
        "medicine": "Antiseptic Gel, Pain Reliever",
        "advice": "Maintain oral hygiene and visit dentist if pain continues."
    }

# ---- WEIGHT ----
    if any(p in user_text for p in ["overweight", "weight gain", "obese"]):
        return {
        "status": "final",
        "disease": "Overweight",
        "medicine": "No medicine required",
        "advice": "Follow healthy diet and exercise regularly. Consult doctor for guidance."
    }

# ---- COLD / COUGH / THROAT ----
    if any(p in user_text for p in ["cold", "runny nose", "sneezing"]):
        return {
        "status": "final",
        "disease": "Common Cold",
        "medicine": "Cetirizine, Paracetamol",
        "advice": "Take rest, drink warm fluids, avoid cold drinks."
    }

    if any(p in user_text for p in ["cough", "dry cough"]):
        return {
        "status": "final",
        "disease": "Cough",
        "medicine": "Cough Syrup",
        "advice": "Drink warm water and avoid dust and smoke."
    }

    if any(p in user_text for p in ["sore throat", "throat pain", "pain while swallowing"]):
        return {
        "status": "final",
        "disease": "Throat Infection",
        "medicine": "Lozenges, Paracetamol",
        "advice": "Gargle with warm salt water and rest your voice."
    }

# ---- SKIN ISSUES ----
    if any(p in user_text for p in ["itchy skin", "skin itching", "rash"]):
        return {
        "status": "final",
        "disease": "Skin Allergy / Rash",
        "medicine": "Antihistamine, Calamine Lotion",
        "advice": "Avoid scratching and keep skin clean and dry."
    }

    if any(p in user_text for p in ["acne", "pimples"]):
        return {
        "status": "final",
        "disease": "Acne",
        "medicine": "Benzoyl Peroxide Gel",
        "advice": "Wash face twice daily and avoid oily cosmetics."
    }

    if any(p in user_text for p in ["fungal infection", "ringworm", "itching between toes"]):
        return {
        "status": "final",
        "disease": "Fungal Infection",
        "medicine": "Antifungal Cream",
        "advice": "Keep area dry and avoid sharing towels."
    }

# ---- EYE ----
    if any(p in user_text for p in ["red eyes", "eye itching", "eye watering"]):
        return {
        "status": "final",
        "disease": "Eye Allergy / Conjunctivitis",
        "medicine": "Lubricating Eye Drops",
        "advice": "Avoid touching eyes and keep them clean."
    }

# ---- EAR ----
    if any(p in user_text for p in ["ear pain", "ear itching"]):
        return {
        "status": "final",
        "disease": "Ear Infection",
        "medicine": "Ear Drops",
        "advice": "Keep ear dry and consult doctor if pain increases."
    }

# ---- NOSE ----
    if any(p in user_text for p in ["nose block", "sinus pain", "face pain near nose"]):
        return {
        "status": "final",
        "disease": "Sinusitis",
        "medicine": "Steam Inhalation, Decongestant",
        "advice": "Do steam inhalation and avoid cold exposure."
    }

# ---- BP / HEART ----
    if any(p in user_text for p in ["high bp", "blood pressure", "hypertension"]):
        return {
        "status": "final",
        "disease": "High Blood Pressure",
        "medicine": "BP Medicines (Doctor Prescribed)",
        "advice": "Reduce salt, exercise, and check BP regularly."
    }

    if any(p in user_text for p in ["chest discomfort", "heart pain", "palpitations"]):
        return {
        "status": "final",
        "disease": "Heart Related Issue",
        "medicine": "Consult Doctor",
        "advice": "Do not ignore chest discomfort. Please consult doctor."
    }

# ---- DIABETES ----
    if any(p in user_text for p in ["high sugar", "diabetes", "frequent urination", "excessive thirst"]):
        return {
        "status": "final",
        "disease": "Diabetes",
        "medicine": "Sugar Control Medicines",
        "advice": "Check blood sugar and follow diabetic diet."
    }

# ---- JOINT & BODY PAIN ----
    if any(p in user_text for p in ["joint pain", "knee pain", "arthritis"]):
        return {
        "status": "final",
        "disease": "Joint Pain / Arthritis",
        "medicine": "Pain Relievers",
        "advice": "Do gentle exercises and avoid strain."
    }

    if any(p in user_text for p in ["back pain", "neck pain"]):
        return {
        "status": "final",
        "disease": "Muscle Strain",
        "medicine": "Pain Relievers",
        "advice": "Apply warm compress and maintain good posture."
    }

    if any(p in user_text for p in ["body pains", "body ache"]):
        return {
        "status": "final",
        "disease": "Viral Body Pains",
        "medicine": "Paracetamol",
        "advice": "Take rest and drink fluids."
    }

# ---- PERIOD / WOMEN HEALTH ----
    if any(p in user_text for p in ["period pain", "menstrual cramps", "stomach pain during periods"]):
        return {
        "status": "final",
        "disease": "Menstrual Cramps",
        "medicine": "Meftal-Spas, Paracetamol",
        "advice": "Use hot water bag, take rest, and avoid cold food."
    }

    if any(p in user_text for p in ["irregular periods", "missed periods"]):
        return {
        "status": "final",
        "disease": "Irregular Menstrual Cycle",
        "medicine": "Consult Gynecologist",
        "advice": "Track cycles and consult doctor for hormonal evaluation."
    }

    if any(p in user_text for p in ["white discharge", "vaginal itching"]):
        return {
        "status": "final",
        "disease": "Vaginal Infection",
        "medicine": "Clotrimazole (Doctor Prescribed)",
        "advice": "Maintain hygiene and consult gynecologist."
    }

# ---- URINE PROBLEMS ----
    if any(p in user_text for p in ["burning urine", "pain while urinating", "frequent urination"]):
        return {
        "status": "final",
        "disease": "Urinary Tract Infection (UTI)",
        "medicine": "Nitrofurantoin (Doctor Prescribed), ORS",
        "advice": "Drink plenty of water and avoid holding urine."
    }

    if any(p in user_text for p in ["lower back pain with urine", "kidney pain"]):
        return {
        "status": "final",
        "disease": "Possible Kidney Infection / Stone",
        "medicine": "Pain Relievers",
        "advice": "Consult doctor for urine test and scan."
    }

# ---- CONSTIPATION ----
    if any(p in user_text for p in ["constipation", "hard stools"]):
        return {
        "status": "final",
        "disease": "Constipation",
        "medicine": "Isabgol, Lactulose Syrup",
        "advice": "Drink water and eat fiber-rich foods."
    }

# ---- ACID REFLUX ----
    if any(p in user_text for p in ["burning in chest", "acid reflux", "sour taste"]):
        return {
        "status": "final",
        "disease": "Acid Reflux (GERD)",
        "medicine": "Omeprazole, Ranitidine",
        "advice": "Avoid late meals and spicy food."
    }

# ---- STRESS / ANXIETY ----
    if any(p in user_text for p in ["stress", "anxiety", "panic", "fear"]):
        return {
        "status": "final",
        "disease": "Stress / Anxiety",
        "medicine": "No self-medication",
        "advice": "Practice relaxation and consult doctor if persistent."
    }

    if any(p in user_text for p in ["sleep problem", "insomnia", "not sleeping"]):
        return {
        "status": "final",
        "disease": "Sleep Disturbance",
        "medicine": "Melatonin (Doctor Prescribed)",
        "advice": "Avoid phone before sleep and maintain sleep routine."
    }

# ---- ALLERGIES ----
    if any(p in user_text for p in ["allergy", "itching after food", "hives"]):
        return {
        "status": "final",
        "disease": "Allergic Reaction",
        "medicine": "Cetirizine, Levocetirizine",
        "advice": "Avoid trigger foods and consult doctor if severe."
    }

    if any(p in user_text for p in ["dust allergy", "seasonal allergy"]):
        return {
        "status": "final",
        "disease": "Allergic Rhinitis",
        "medicine": "Cetirizine, Montelukast",
        "advice": "Avoid dust and use mask outdoors."
    }
    # ==================================================
    # 🟢 STEP 3: ML FALLBACK (TAG MATCHING + SIMILARITY)
    # ==================================================

    user_words = set(user_text.split())

    best_score = 0
    best_row = None

    for _, row in df.iterrows():
        tags = set(str(row["symptom_tags"]).split(","))
        score = len(tags & user_words)

        if score > best_score:
            best_score = score
            best_row = row

    # If no good match
    if best_score <= 1:
        return {
            "status": "clarification",
            "message": "Please explain your symptoms more clearly."
        }

    return {
        "status": "final",
        "disease": best_row["Disease Prediction"],
        "medicine": best_row["Recommended Medicines"],
        "advice": best_row["Advice"]
    }