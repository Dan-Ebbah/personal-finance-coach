import os
import pandas as pd
from datetime import datetime
from .models import Transaction, SessionLocal, init_db

def categorize(description: str) -> str:
    desc = description.lower()
    if any(x in desc for x in ["grocery", "supermarket", "market"]):
        return "Groceries"
    if any(x in desc for x in ["restaurant", "cafe", "diner"]):
        return "Restaurants"
    if any(x in desc for x in ["uber", "lyft", "taxi"]):
        return "Transport"
    if any(x in desc for x in ["rent", "landlord"]):
        return "Rent"
    if any(x in desc for x in ["salary", "payroll", "income"]):
        return "Income"
    return "Other"

def ingest_csv(path: str):
    init_db()
    df = pd.read_csv(path)

    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            trans = Transaction(
                transaction_date=datetime.strptime(str(row['transaction_date']), '%m/%d/%Y').date(),
                transaction=row['transaction'],
                name=row['name'],
                memo=row.get('memo', ''),
                amount=float(row['amount']),
            )
            session.add(trans)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "../data/transactions_sample.csv")
    ingest_csv(csv_path)
    print("Ingested sample data.")
