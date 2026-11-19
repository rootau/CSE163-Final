import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def get_sum_quan(pd: pd.DataFrame, col: str) -> pd.Series:
    """
    Gets the summary of any quantitative values.
    """

    return pd[col].describe()


def get_unique_values(pd: pd.DataFrame, col: str) -> pd.Series:
    """
    Gets the summary of any catigorical values by getting the count
    of unique values.
    """

    return pd[col].value_counts(ascending=False)

def get_month(pd: pd.DataFrame, time: str) -> pd.Series:
    """
    Gets the number of values in a month
    """
    months = pd.copy()
    months["Month"] = pd[time].dt.to_period("M")
    return months.groupby("Month").size().reset_index(
        name="Count").sort_values(by="Month", ascending=False)

def main():

    # Points directly to the folder where THIS .py script is saved
    # script_dir = Path(__file__).resolve().parent
    # senate_path = script_dir / "Cleaned_Senate.csv"
    # house_path = script_dir / "Cleaned_House.csv"
    # approval_path = script_dir / "Cleaned_Approval_Rating.csv"
    # orders_path = script_dir / "Cleaned_Executive_Orders.csv"

    # senate_path = pd.read_csv("Cleaned_Senate.csv")
    # house_path = pd.read_csv("Cleaned_House.csv")
    # approval_path = pd.read_csv("Cleaned_Approval_Rating.csv")
    # orders_path = pd.read_csv("Cleaned_Executive_Orders.csv")

    script_dir = Path(__file__).resolve().parent
    senate_path = script_dir / "Cleaned_Senate.csv"
    house_path = script_dir / "Cleaned_House.csv"
    approval_path = script_dir / "Cleaned_Approval_Rating.csv"
    orders_path = script_dir / "Cleaned_Executive_Orders.csv"
    senate = pd.read_csv(senate_path, parse_dates=["Start Date", "End Date"])
    house = pd.read_csv(house_path, parse_dates=["Start Date", "End Date"])
    approval = pd.read_csv(approval_path, parse_dates=["Start Date", 
                                                       "End Date"])
    orders = pd.read_csv(orders_path, parse_dates=["signing_date"])

    # Gets all summaries of columns with quantitive data. 

    # Executive Order summary
    print(get_month(orders, "signing_date"))
    
    # Approval Rating Summaries
    print(get_unique_values(approval, "President"))
    print(get_sum_quan(approval, "Approving"))
    print(get_sum_quan(approval, "Disapproving"))
    print(get_sum_quan(approval, "Unsure/NoData"))
    print(get_sum_quan(approval, "Republicans Approving"))
    print(get_sum_quan(approval, "Democrats Approving"))
    print(get_sum_quan(approval, "Independents Approving"))

    # House Summaries 
    print(get_sum_quan(house, "Democrats"))
    print(get_sum_quan(house, "Republicans"))
    print(get_unique_values(house ,"Majority"))
    

    # Senate Summaries
    print(get_sum_quan(senate, "Democrats"))
    print(get_sum_quan(senate, "Republicans"))
    print(get_sum_quan(senate, "Other"))
    print(get_sum_quan(senate, "Vacant"))
if __name__ == "__main__":
    main()