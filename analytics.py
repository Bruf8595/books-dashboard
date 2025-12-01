import pandas as pd

# 1. Top 5 revenue days
def top_5_revenue_days(orders):
    daily = orders.groupby('date')['paid_price'].sum().reset_index()
    top5 = daily.sort_values('paid_price', ascending=False).head(5)
    return top5

# 2. Unique users (handle possible aliases)
def unique_users(orders, users):
    df = orders.merge(users, left_on='user_id', right_on='id', how='left')
    df['normalized_name'] = df['name'].astype(str).str.strip().str.lower()
    return df['normalized_name'].nunique()

# 3. Unique author sets
def unique_author_sets(books):
    sets = books['author'].apply(lambda x: tuple(sorted(x)))
    return sets.nunique()

# 4. Most popular author(s)
def most_popular_authors(orders, books):
    df = orders.merge(books, left_on='book_id', right_on='id', how='left')
    df = df.explode('author')
    popular = df.groupby('author')['quantity'].sum()
    max_count = popular.max()
    return popular[popular == max_count].index.tolist()

# 5. Top customer by total spending (all aliases)
def top_customers_with_aliases(orders, users):
    df = orders.merge(users, left_on='user_id', right_on='id', how='left')
    df['normalized_name'] = df['name'].astype(str).str.strip().str.lower()
    spending = df.groupby('normalized_name')['paid_price'].sum()
    max_spent = spending.max()
    top_names = spending[spending == max_spent].index.tolist()
    return df[df['normalized_name'].isin(top_names)]['user_id'].unique().tolist()

# 6. Run all analytics for a dataset
# It's probably better to do the same in "processes", but I'm too lazy
def run_all_analytics(books, orders, users):
    return {
        'top_5_days': top_5_revenue_days(orders),
        'unique_users': unique_users(orders, users),
        'unique_author_sets': unique_author_sets(books),
        'most_popular_authors': most_popular_authors(orders, books),
        'top_customers': top_customers_with_aliases(orders, users)
    }
