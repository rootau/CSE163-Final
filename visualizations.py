import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def make_congress(senate: pd.DataFrame, house: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the Senate and House dataframes into a single dataframe
    with columns: 'Congress', 'Start Date', 'End Date', 'Senate Seats',
    'House Seats'.
    """
    # Merge the two dataframes on the 'Start Date' and 'End Date' columns
    congress = pd.merge(
        senate[['Start Date', 'End Date', 'Democrats', 'Republicans', 'Party']],
        house[['Start Date', 'End Date', 'Democrats', 'Republicans', 'Majority']],
        on=['Start Date', 'End Date'],
        suffixes=('_Senate', '_House')
    )
    # Rename columns for clarity
    congress.rename(columns={'Democrats_Senate': 'Senate Democrats', 
                              'Republicans_Senate': 'Senate Republicans',
                              'Democrats_House': 'House Democrats',
                              'Republicans_House': 'House Republicans'}, inplace=True)
    
    return congress

def make_ordersvscongress(orders: pd.DataFrame, congress: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the Executive Orders dataframe with the Congress dataframe
    to analyze the relationship between executive orders and congressional composition.
    """
    counts = []

    for _, row in congress.iterrows():
        count = (
            (orders["signing_date"] >= row["Start Date"]) &
            (orders["signing_date"] <= row["End Date"])
        ).sum()

        counts.append(count)

    orders_vs_congress = congress[["Start Date", "End Date"]].copy()
    orders_vs_congress["Orders"] = counts
    return orders_vs_congress


def main():
    # Points directly to the folder where THIS .py script is saved
    script_dir = Path(__file__).resolve().parent
    senate_path = script_dir / "Cleaned_Senate.csv"
    house_path = script_dir / "Cleaned_House.csv"
    approval_path = script_dir / "Cleaned_Approval_Rating.csv"
    orders_path = script_dir / "Cleaned_Executive_Orders.csv"
    senate = pd.read_csv(senate_path, parse_dates=["Start Date", "End Date"])
    house = pd.read_csv(house_path, parse_dates=["Start Date", "End Date"])
    approval = pd.read_csv(approval_path, parse_dates=["Start Date", "End Date"])
    orders = pd.read_csv(orders_path, parse_dates=["signing_date"])

    congress = make_congress(senate, house)

    orders_vs_congress = make_ordersvscongress(orders, congress)

if __name__ == "__main__":
    main()