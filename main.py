from processing import load_and_clean
from analytics import run_all_analytics

data_folders = ["data/DATA1", "data/DATA2", "data/DATA3"]

results = {}
for folder in data_folders:
    books, orders, users = load_and_clean(folder)
    results[folder] = run_all_analytics(books, orders, users)


for folder, res in results.items():
    print(f"--- {folder} ---")
    print("Top 5 days:", res['top_5_days'])
    print("Unique users:", res['unique_users'])
    print("Unique author sets:", res['unique_author_sets'])
    print("Most popular authors:", res['most_popular_authors'])
    print("Top customers:", res['top_customers'])
