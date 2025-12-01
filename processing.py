import pandas as pd
import os
import re
import yaml
from pathlib import Path
from dateutil import parser
def load_and_clean(path: str) -> pd.DataFrame:

    folder = Path(path)

    if not folder.exists():
        raise FileNotFoundError(f"Папка не найдена: {path}")
    
    books_path = folder / "books.yaml"
    orders_path = folder / "orders.parquet"
    users_path = folder / "users.csv"

    with open(books_path, "r", encoding="utf-8") as f:
        books_raw = yaml.safe_load(f)
    books = pd.DataFrame(books_raw)
    books.columns = [col.lstrip(":") for col in books.columns]
    orders = pd.read_parquet(orders_path)
    users = pd.read_csv(users_path)



    # 1. Cleaning books:

    books = books.drop_duplicates().copy()
    books.dropna(subset=['title', 'author'], inplace=True)
    def normalize_authors(author):
        if isinstance(author, list):
            return [str(a).strip().lower() for a in author]
        else:
            return [str(author).strip().lower()]
    
    
    books['author'] = books['author'].apply(normalize_authors)

# 2. Cleaning orders:

    orders = orders.drop_duplicates().copy()



    orders.dropna(subset=['user_id', 'book_id'], inplace=True)

    def parse_price(price_str):
        if pd.isna(price_str):
            return None
        s = str(price_str)
        

        euro = 1.2
        is_euro = '€' in s
    
        s = s.replace('¢', '.')
        
        nums = re.findall(r'\d+\.\d+|\d+', s)
        if not nums:
            return None
        value = float(nums[0])
        if is_euro:
            value *= euro
        return value


    orders['unit_price'] = orders['unit_price'].apply(parse_price)
    orders.dropna(subset=['unit_price', 'quantity'], inplace=True)
    orders['paid_price'] = orders['quantity'] * orders['unit_price']

    orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")
    orders["unit_price"] = pd.to_numeric(orders["unit_price"], errors="coerce")

    def parse_date(ts):
        try:
            dt = parser.parse(str(ts), dayfirst=True, fuzzy=True, ignoretz=True)
            return pd.Timestamp(dt)
        except:
            return pd.NaT

    orders['timestamp'] = orders['timestamp'].apply(parse_date)

    orders['timestamp'] = pd.to_datetime(orders['timestamp'], errors='coerce')

        # remove invalid timestamps Was problem with NaT
    orders = orders.dropna(subset=['timestamp'])

    orders['date'] = orders['timestamp'].dt.date


# 3.     Cleaning users
    users = users.drop_duplicates().copy()
    users['name'] = users['name'].astype(str).str.strip().str.lower()
    users['phone'] = users['phone'].astype(str).str.replace(r'[\s\-\(\)\.]', '', regex=True)
    users['email'] = users['email'].astype(str).str.strip().str.lower()
    users = users.replace({'': None})

    return books, orders, users