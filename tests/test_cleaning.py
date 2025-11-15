# tests/test_cleaning.py
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils_cleaning import (
    normalize_email,
    normalize_country,
    normalize_phone_fr,
    convert_weight_to_kg,
    normalize_currency
)

def test_normalize_email():
    assert normalize_email("Test@Mail.com") == "test@mail.com"
    assert normalize_email("   user@mail.com  ") == "user@mail.com"
    assert normalize_email("invalid") is None

def test_normalize_country():
    assert normalize_country("fr") == "France"
    assert normalize_country("ch") == "Suisse"
    assert normalize_country("Belgique") == "Belgique"

def test_normalize_phone_fr():
    assert normalize_phone_fr("0642702383") == "+33642702383"
    assert normalize_phone_fr("+33642702383") == "+33642702383"
    assert normalize_phone_fr("invalid") is None

def test_convert_weight_to_kg():
    assert convert_weight_to_kg(1000, "g") == 1.0
    assert convert_weight_to_kg(1, "kg") == 1.0
    # approximation allowed
    assert round(convert_weight_to_kg(1, "lb"), 6) == round(0.45359237, 6)

def test_normalize_currency():
    assert normalize_currency("€") == "EUR"
    assert normalize_currency("$") == "USD"
    assert normalize_currency("usd") == "USD"
