
import pandas as pd
from openpyxl.workbook import Workbook
import snowflake.connector

import dotenv
import os
dotenv.load_dotenv()

user = os.getenv("user")
password = os.getenv("password")
account = os.getenv("account")   
warehouse = os.getenv("warehouse")
database = os.getenv("database")
schema = os.getenv("schema")         

input_path_load = os.getenv("output_path_trans")

def load_data_to_snowflake(input_path_load):
    df = pd.read_excel(input_path_load)

    print("📊 STATISTIQUES DU DATASET \n")
    print(f"Nombre de livres : {df.shape[0]}")
    print(f"Prix moyen : £{round(df['price'].mean(), 2)}")
    print(f"Note moyenne : {round(df['rating_number'].mean(), 2)}")

    # Chargement dans Snowflake
    
    # 1. Connexion à Snowflake
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    # 3. Créer un curseur
    cur = conn.cursor()

    # 4. Insérer les données ligne par ligne
    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO BOOK_FINAL (title, price, link, in_stock, rating_number)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row['title'], row['price'], row['link'], row['in_stock'], row['rating_number'])
        )

    # 5. Fermer la connexion
    cur.close()
    conn.close()

    print("✅ Données chargées dans Snowflake avec succès !")

    
    
if __name__ == "__main__":
    load_data_to_snowflake(input_path_load)
