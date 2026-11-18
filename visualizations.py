import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def make_congress(senate: pd.DataFrame, house: pd.DataFrame) -> pd.DataFrame:
    """
    Combines the Senate and House dataframes into a single dataframe
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
    Combines the Executive Orders dataframe with the Congress dataframe
    """
    counts = []

    for _, row in congress.iterrows():
        count = (
            (orders["signing_date"] >= row["Start Date"]) &
            (orders["signing_date"] <= row["End Date"])
        ).sum()

        counts.append(count)

    orders_vs_congress = congress.copy()
    orders_vs_congress["Orders"] = counts
    return orders_vs_congress

def make_ordersvsapprovalavg(orders: pd.DataFrame, approval: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the Executive Orders dataframe with the Approval Ratings dataframe
    by how many orders were signed during each president's term and the average approval ratings.
    """

    counts = []
    president_approval = approval.groupby("President").agg(
        **{
            "Start Date": ("Start Date", "min"),
            "End Date": ("End Date", "max"),
            "Average Approval": ("Approving", "mean"),
            "Average Disapproval": ("Disapproving", "mean"),
            "Average Unsure": ("Unsure/NoData", "mean"),
            "Democrats Approving": ("Democrats Approving", "mean"),
            "Independents Approving": ("Independents Approving", "mean"),
            "Republicans Approving": ("Republicans Approving", "mean")
        }
    ).sort_values(by="Start Date", ascending=False).reset_index()
    for _, row in president_approval.iterrows():
        count = (
            (orders["signing_date"] >= row["Start Date"]) &
            (orders["signing_date"] <= row["End Date"])
        ).sum()

        counts.append(count)

    orders_vs_approval = president_approval.copy()
    orders_vs_approval["Orders"] = counts
    return orders_vs_approval

def make_ordersvsapprovalmonthly(orders: pd.DataFrame, approval: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the Executive Orders dataframe with the Approval Ratings dataframe
    by the average ratings per month and how many orders were signed
    """
    monthly = approval.copy()
    monthly["Year-Month"] = monthly["Start Date"].dt.to_period("M")
    monthly = monthly.groupby("Year-Month").agg(
        **{
            "Start Date": ("Start Date", "min"),
            "End Date": ("End Date", "max"),
            "Average Approval": ("Approving", "mean"),
            "Average Disapproval": ("Disapproving", "mean"),
            "Average Unsure": ("Unsure/NoData", "mean"),
            "Democrats Approving": ("Democrats Approving", "mean"),
            "Independents Approving": ("Independents Approving", "mean"),
            "Republicans Approving": ("Republicans Approving", "mean")
        }
    ).sort_values(by="Start Date", ascending=False).reset_index()
    monthly["Start Date"] = monthly["Year-Month"].dt.to_timestamp()

    monthly["End Date"] = (
        monthly["Year-Month"].dt.to_timestamp(how="end").dt.normalize()
    )
    counts = []

    for _, row in monthly.iterrows():
        count = (
            (orders["signing_date"] >= row["Start Date"]) &
            (orders["signing_date"] <= row["End Date"])
        ).sum()

        counts.append(count)

    orders_vs_approval = monthly.copy()
    orders_vs_approval["Orders"] = counts
    return orders_vs_approval

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

    president_orders_vs_approval = make_ordersvsapprovalavg(orders, approval)

    monthly_orders_vs_approval = make_ordersvsapprovalmonthly(orders, approval)

    

    

if __name__ == "__main__":
    main()