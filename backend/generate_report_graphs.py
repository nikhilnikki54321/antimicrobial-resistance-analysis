import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

# Configuration
DATA_PATH = "data/Bacteria_dataset_Multiresictance.csv"
OUTPUT_DIR = "../docs/assets"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Loading data from {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = pd.read_csv("../Bacteria_dataset_Multiresictance.csv")

# Set global plotting style to IEEE academic
plt.style.use('seaborn-v0_8-paper')
sns.set_context("paper", rc={"font.size":12,"axes.titlesize":14,"axes.labelsize":12})

print("Generating Age/Gender Demographics...")
# 1. Demographics Distribution (Age/Gender)
if 'age/gender' in df.columns:
    df[['Age', 'Gender']] = df['age/gender'].str.extract(r'(\d+)/([MF])')
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    
    plt.figure(figsize=(8, 6))
    sns.histplot(data=df.dropna(subset=['Age', 'Gender']), x='Age', hue='Gender', multiple='stack', bins=30, palette='Set2')
    plt.title('Age and Gender Distribution of Patients')
    plt.xlabel('Age (Years)')
    plt.ylabel('Patient Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_demographics.png'), dpi=300)
    plt.close()

print("Generating Top Resistant Drugs Bar Chart...")
# 2. Resistance Profile of Top Drugs
drug_columns = ['AMX/AMP', 'AMC', 'CZ', 'FOX', 'CTX/CRO', 'IPM', 'GEN', 'AN', 'CIP', 'C', 'Co-trimoxazole', 'colistine']
drug_columns = [col for col in drug_columns if col in df.columns]

if drug_columns:
    res_data = []
    for drug in drug_columns:
        counts = df[drug].value_counts(normalize=True)
        res_data.append({
            'Drug': drug,
            'Resistant (R)': counts.get('R', counts.get('r', 0)),
            'Susceptible (S)': counts.get('S', counts.get('s', 0))
        })
    res_df = pd.DataFrame(res_data).set_index('Drug').sort_values('Resistant (R)', ascending=False)
    
    res_df.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#d9534f', '#5cb85c'])
    plt.title('Antimicrobial Resistance Profile Across Key Antibiotics')
    plt.xlabel('Antibiotic Label / Drug')
    plt.ylabel('Proportion of Microbes')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_resistance_bars.png'), dpi=300)
    plt.close()

print("Generating Model Target Class Class Imbalance Chart...")
# 3. Microbe Family Frequency
if 'Souches' in df.columns:
    df['Microbe Core'] = df['Souches'].str.split(' ').str[1:].str.join(' ')
    top_microbes = df['Microbe Core'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(y=top_microbes.index, x=top_microbes.values, palette='viridis')
    plt.title('Top 10 Cultured Microbes Identified in Dataset')
    plt.xlabel('Frequency count')
    plt.ylabel('Taxonomy')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig3_microbes.png'), dpi=300)
    plt.close()


print("Generating Correlation Matrix...")
# 4. Correlation Matrix of Drugs
if drug_columns:
    numeric_df = df[drug_columns].replace({'S': 0, 's':0, 'R': 1, 'r':1})
    numeric_df = numeric_df.apply(pd.to_numeric, errors='coerce').dropna()
    
    plt.figure(figsize=(10, 8))
    corr = numeric_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, square=True)
    plt.title('Spearman Correlation Matrix between Antibiotic Resistances')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig4_correlation.png'), dpi=300)
    plt.close()


print("Generating Prediction Pipeline Architecture Mockup...")
# 5. Architecture Logic Diagram (Mock using matplotlib)
plt.figure(figsize=(8, 4))
plt.text(0.1, 0.5, 'Input Clinical Data\n(CSV Matrix)', size=12, ha='center', va='center', bbox=dict(boxstyle='round', facecolor='#e1f7d5'))
plt.arrow(0.25, 0.5, 0.1, 0, head_width=0.05, head_length=0.05, fc='k', ec='k')
plt.text(0.5, 0.5, 'MultiOutputClassifier\n(Random Forest)', size=12, ha='center', va='center', bbox=dict(boxstyle='round', facecolor='#d5e1f7'))
plt.arrow(0.7, 0.5, 0.1, 0, head_width=0.05, head_length=0.05, fc='k', ec='k')
plt.text(0.9, 0.5, 'S/R Resistance\nVectors Output', size=12, ha='center', va='center', bbox=dict(boxstyle='round', facecolor='#f7d5e1'))
plt.axis('off')
plt.title("Fig. 5: High-Level Logical Pipeline for Multi-Drug Classification")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'fig5_architecture.png'), dpi=300)
plt.close()

print("All charts successfully generated in docs/assets!")
