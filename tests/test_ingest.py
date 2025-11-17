import pytest
from src.ingest import categorize, ingest_csv
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
