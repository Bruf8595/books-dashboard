Bookstore Analytics Dashboard
Overview

This project is a personal exploration of bookstore sales data. It analyzes orders, books, and users to generate insights and visualize daily revenue. The goal was to practice data cleaning, aggregation, and dashboard creation with Python.

Features

Top 5 days by revenue – Identify the days with the highest total sales.

Unique users – Count real unique users, considering possible aliases or changes in address, phone, or email.

Unique author sets – Determine the number of unique author combinations for all books.

Most popular authors – Find the author(s) with the highest sold book count.

Top customers – List user IDs of top spenders, including aliases.

Daily revenue chart – A simple, interactive line chart showing revenue trends over time.

## Requirements

- Python 3.10+
- Pandas
- Matplotlib
- Streamlit
- Seaborn (optional, for styling)

Setup

Create a virtual environment:
```bash
python -m venv .venv
```

Activate the environment:

Windows:
```bash
.venv\Scripts\activate
```
Install dependencies:

```bash
pip install -r requirements.txt
```

Usage

Run the main script to generate analytics for all datasets:

```bash
python main.py
```
Run the dashboard to view daily revenue charts and other metrics:
```bash
python dashboard.py
```