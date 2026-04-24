import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
DATA_MODELS = os.path.join(BASE_DIR, "data", "models")
RAW_CSV = os.path.join(DATA_RAW, "Bacteria_dataset_Multiresictance.csv")

DRUG_COLUMNS = [
    "AMX/AMP", "AMC", "CZ", "FOX", "CTX/CRO", "IPM",
    "GEN", "AN", "Acide nalidixique", "ofx", "CIP",
    "C", "Co-trimoxazole", "Furanes", "colistine"
]

DRUG_DISPLAY_NAMES = {
    "AMX/AMP": "Amoxicillin/Ampicillin",
    "AMC": "Amoxicillin-Clavulanate",
    "CZ": "Cefazolin",
    "FOX": "Cefoxitin",
    "CTX/CRO": "Cefotaxime/Ceftriaxone",
    "IPM": "Imipenem",
    "GEN": "Gentamicin",
    "AN": "Amikacin",
    "Acide nalidixique": "Nalidixic Acid",
    "ofx": "Ofloxacin",
    "CIP": "Ciprofloxacin",
    "C": "Chloramphenicol",
    "Co-trimoxazole": "Co-trimoxazole",
    "Furanes": "Nitrofurantoin",
    "colistine": "Colistin"
}

FEATURE_COLUMNS = ["age", "gender", "Diabetes", "Hypertension",
                   "Hospital_before", "Infection_Freq"]

DROP_COLUMNS = ["ID", "Name", "Email", "Address",
                "Collection_Date", "Notes", "Souches", "age/gender"]
