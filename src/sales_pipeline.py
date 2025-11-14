import pandas as pd
import re

#date
def normaliser_date(dates):
    dt = pd.to_datetime(dates, errors='coerce')
    return dt.date()

#montant
def normaliser_amount(amount):
    return pd.to_numeric(amount,errors='coerce')

