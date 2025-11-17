import tempfile
from datetime import date
from pathlib import Path

import pytest
from httpx import delete

from src.ingest import categorize, ingest_csv
from src.models import init_db, SessionLocal, Transaction


class TestCategoriesIngest:
    def test_groceries_category(self):
        assert categorize("Walmart Supermarket") == "Groceries"
        assert categorize("Local grocery store") == "Groceries"

    def test_restaurants_category(self):
        assert categorize("Dinner at Italian Restaurant") == "Restaurants"
        assert categorize("Morning Cafe visit") == "Restaurants"

    def test_transport_category(self):
        assert categorize("Uber ride to airport") == "Transport"
        assert categorize("Lyft downtown") == "Transport"

    def test_rent_category(self):
        assert categorize("Monthly rent payment") == "Rent"
        assert categorize("Paid landlord for April") == "Rent"

    def test_income_category(self):
        assert categorize("Monthly salary received") == "Income"
        assert categorize("Payroll deposit") == "Income"

    def test_other_category(self):
        assert categorize("Book purchase") == "Other"
        assert categorize("Gym membership fee") == "Other"


class TestIngestCSV:
    @pytest.fixture
    def temp_csv(self):
        csv_content = """transaction_date,transaction,name,memo,amount
01/15/2025,DEBIT,STARBUCKS,Coffee,-12.45
01/14/2025,CREDIT,PAYROLL DEPOSIT,Salary,2850.00
01/13/2025,DEBIT,WHOLE FOODS,Groceries,-45.67"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file_path = temp_file.name

        yield temp_file_path

        Path(temp_file_path).unlink(missing_ok=True)
    @pytest.fixture
    def clean_db(self):
        init_db()
        session = SessionLocal()
        session.query(Transaction).delete()
        session.commit()
        session.close()
        yield
        session = SessionLocal()
        session.query(Transaction).delete()
        session.commit()
        session.close()

    def test_ingest_csv(self, temp_csv, clean_db):
        ingest_csv(temp_csv)

        session = SessionLocal()
        try:
            transactions = session.query(Transaction).all()
            assert len(transactions) == 3

            first = transactions[0]
            assert first.transaction_date == date(2025, 1, 15)
            assert first.transaction == 'DEBIT'
            assert first.name == 'STARBUCKS'
            assert first.memo == 'Coffee'
            assert first.amount == -12.45
        finally:
            session.close()

    def test_ingest_csv_with_missing_memo(self, clean_db):
        invalid_csv_content = """transaction_date,transaction,name,amount
01/15/2025,DEBIT,TEST MERCHANT,-10.00"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(invalid_csv_content)
            temp_file_path = temp_file.name


        try:
            ingest_csv(temp_file_path)

            session = SessionLocal()
            try:
                transaction = session.query(Transaction).first()
                assert transaction.memo == ''
            finally:
                session.close()
        finally:
            Path(temp_file_path).unlink(missing_ok=True)


    def test_ingest_csv_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            ingest_csv("non_existent_file.csv")
