import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import config


def split_age_gender(df):
    parts = df["age/gender"].astype(str).str.split("/", expand=True)
    df = df.copy()
    df["age"] = pd.to_numeric(parts[0], errors="coerce")
    df["gender"] = parts[1].map({"M": 1, "F": 0, "m": 1, "f": 0}) if parts.shape[1] > 1 else 0
    return df


def encode_targets(df, drug_columns):
    df = df.copy()
    for col in drug_columns:
        df[col] = df[col].astype(str).str.strip().map(
            {"S": 0, "R": 1, "s": 0, "r": 1}
        )
    return df


def clean_boolean(df, col):
    df = df.copy()
    df[col] = df[col].astype(str).str.strip().str.lower()
    df[col] = df[col].map({
        "yes": 1, "true": 1, "1": 1, "1.0": 1,
        "no": 0, "false": 0, "0": 0, "0.0": 0, "nan": 0, "none": 0, "": 0
    }).fillna(0).astype(int)
    return df


def extract_microbe_name(souches_val):
    if pd.isna(souches_val):
        return "Unknown"
    parts = str(souches_val).strip().split(" ", 1)
    return parts[1] if len(parts) > 1 else parts[0]


# Normalize messy microbe names to clean canonical names
MICROBE_NORMALIZE = {
    "E. coli": "Escherichia coli",
    "E.coli": "Escherichia coli",
    "E.cli": "Escherichia coli",
    "E.coi": "Escherichia coli",
    "Escherichia coli": "Escherichia coli",
    "Klebsiella pneumoniae": "Klebsiella pneumoniae",
    "Klbsiella pneumoniae": "Klebsiella pneumoniae",
    "Klebsie.lla pneumoniae": "Klebsiella pneumoniae",
    "Proteus mirabilis": "Proteus mirabilis",
    "Proeus mirabilis": "Proteus mirabilis",
    "Prot.eus mirabilis": "Proteus mirabilis",
    "Protus mirabilis": "Proteus mirabilis",
    "Pseudomonas aeruginosa": "Pseudomonas aeruginosa",
    "Acinetobacter baumannii": "Acinetobacter baumannii",
    "Morganella morganii": "Morganella morganii",
    "Serratia marcescens": "Serratia marcescens",
    "Citrobacter spp.": "Citrobacter spp.",
    "Enterobacteria spp.": "Enterobacteria spp.",
    "Enteobacteria spp.": "Enterobacteria spp.",
    "Enter.bacteria spp.": "Enterobacteria spp.",
}


def normalize_microbe(name):
    return MICROBE_NORMALIZE.get(name, "Other")


def load_and_clean():
    df = pd.read_csv(config.RAW_CSV)

    df = split_age_gender(df)

    for col in ["Diabetes", "Hypertension", "Hospital_before"]:
        if col in df.columns:
            df = clean_boolean(df, col)

    df["Infection_Freq"] = pd.to_numeric(
        df["Infection_Freq"], errors="coerce"
    ).fillna(0)

    # Extract and normalize microbe names
    df["microbe_raw"] = df["Souches"].apply(extract_microbe_name)
    df["microbe"] = df["microbe_raw"].apply(normalize_microbe)

    df = encode_targets(df, config.DRUG_COLUMNS)

    df["age"] = df["age"].fillna(df["age"].median())
    df["gender"] = df["gender"].fillna(0).astype(int)

    # One-hot encode microbe
    microbe_dummies = pd.get_dummies(df["microbe"], prefix="microbe")

    feature_cols = ["age", "gender", "Diabetes", "Hypertension",
                    "Hospital_before", "Infection_Freq"]

    X = pd.concat([df[feature_cols], microbe_dummies], axis=1)
    y = df[config.DRUG_COLUMNS].copy()

    valid_mask = y.notna().all(axis=1)
    X = X.loc[valid_mask].reset_index(drop=True)
    y = y.loc[valid_mask].reset_index(drop=True)

    X = X.fillna(0)
    y = y.fillna(0).astype(int)

    scaler = MinMaxScaler()
    X[["age", "Infection_Freq"]] = scaler.fit_transform(
        X[["age", "Infection_Freq"]]
    )

    all_feature_names = list(X.columns)
    microbe_columns = [c for c in X.columns if c.startswith("microbe_")]

    return (X.values, y.values, all_feature_names,
            config.DRUG_COLUMNS, scaler, microbe_columns)


def get_microbe_list():
    df = pd.read_csv(config.RAW_CSV)
    df["microbe"] = df["Souches"].apply(extract_microbe_name).apply(normalize_microbe)
    return sorted([m for m in df["microbe"].dropna().unique().tolist() if m != "Other"])
