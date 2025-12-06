import requests
from bs4 import BeautifulSoup
import pandas as pd
import dotenv
import os

dotenv.load_dotenv()
output_path_ext = os.getenv("output_path_ext")



BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"


def get_book_data():
    all_books = []

    for page in range(1, 6):  # On scrape les 5 premières pages
        print(f"Scraping page {page}...")
        url = BASE_URL.format(page)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erreur sur la page {page}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.replace("£", "").strip()
            availability = book.find("p", class_="instock availability").text.strip()

            rating = book.find("p", class_="star-rating")
            rating_class = rating["class"][1] if rating else "None"

            book_link = book.h3.a["href"]
            full_link = "https://books.toscrape.com/catalogue/" + book_link

            all_books.append({
                "title": title,
                "price (£)": price,
                "availability": availability,
                "rating": rating_class,
                "link": full_link
            })

    return pd.DataFrame(all_books)


def save_raw_data(df, output_path_ext):
    df.to_csv(output_path_ext, index=False)
    print(f"✅ Données brutes sauvegardées dans {output_path_ext}")


if __name__ == "__main__":
    df_books = get_book_data()
    print(df_books.head())
    save_raw_data(df_books, output_path_ext)
