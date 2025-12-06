import pandas as pd
import re

import dotenv
import os
dotenv.load_dotenv()

input_path_trans = os.getenv("output_path_ext")
output_path_trans = os.getenv("output_path_trans")


def transform_data(input_path_trans):
    # Charger les données brutes
    print("🔄 Chargement des données brutes...")
    df = pd.read_csv(input_path_trans)

    print("🔍 Données avant nettoyage :")
    print(df.head())

    # Convertir le prix en float
    df["price (£)"] = df["price (£)"].astype(str).str.replace(r"[^0-9.]", "", regex=True)
    df["price (£)"] = pd.to_numeric(df["price (£)"], errors="coerce")
    df = df.rename(columns={"price (£)": "price"})

    # Standardiser availability (True/False)
    df["in_stock"] = df["availability"].apply(
        lambda x: True if "In stock" in x else False
    )

    # Transformer le texte de rating en chiffre
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating_number"] = df["rating"].map(rating_map)

    # Supprimer les colonnes inutiles
    df = df.drop(columns=["availability", "rating"])

    # Gérer valeurs manquantes
    df = df.dropna()

    print("✅ Données après nettoyage :")
    print(df.head(10))

    return df


def save_processed_data(df, output_path_trans):
    df.to_excel(output_path_trans, index=False)
    print(f"✅ Données nettoyées sauvegardées dans {output_path_trans}")


if __name__ == "__main__":
    df_cleaned = transform_data(input_path_trans)
    save_processed_data(df_cleaned, output_path_trans)
