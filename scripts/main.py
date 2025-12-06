from extract import get_book_data, save_raw_data
from transform import transform_data, save_processed_data
from load import load_data_to_snowflake

import dotenv
import os

dotenv.load_dotenv()
output_path_ext = os.getenv("output_path_ext")

input_path_trans = os.getenv("output_path_ext")
output_path_trans = os.getenv("output_path_trans")




def run_pipeline():
    print("🚀 Lancement du pipeline e-commerce...\n")

    # ETAPE 1 : Extraction
    df_raw = get_book_data()
    save_raw_data(df_raw, output_path_ext)
   

    # ETAPE 2 : Transformation
    df_cleaned = transform_data(input_path_trans)
    save_processed_data(df_cleaned, output_path_trans)

    # ETAPE 3 : Chargement
    load_data_to_snowflake(output_path_trans)

    print("\n✅ PIPELINE TERMINÉ AVEC SUCCÈS")


if __name__ == "__main__":
    run_pipeline()
