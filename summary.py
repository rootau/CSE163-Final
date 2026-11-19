import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def get_sum_quan(pd: pd.dataframe, col: Str) -> pd.DataFrame:
    """
    Gets the summary of any quantitative values.
    """

    return pd[col].describe()


def get_unique_values(pd: pd.dataframe, col: String) -> pd.DataFrame:
    """
    Gets the summary of any catigorical values by getting the count
    of unique values.
    """

    return pd[col].value_counts(ascending=False)


def main():

    # Points directly to the folder where THIS .py script is saved
    # script_dir = Path(__file__).resolve().parent
    # senate_path = script_dir / "Cleaned_Senate.csv"
    # house_path = script_dir / "Cleaned_House.csv"
    # approval_path = script_dir / "Cleaned_Approval_Rating.csv"
    # orders_path = script_dir / "Cleaned_Executive_Orders.csv"

    senate_path = pd.read_csv("Cleaned_Senate.csv")
    house_path = pd.read_csv("Cleaned_House.csv")
    approval_path = pd.read_csv("Cleaned_Approval_Rating.csv")
    orders_path = pd.read_csv("Cleaned_Executive_Orders.csv")

    # Gets all summaries of columns with quantitive data. 

    # Executive Order summary
    
    # Approval Rating Summaries
    print(get_unique_values(approval_path, "President"))
    print(get_sum_quan(approval_path, "Approving"))
    print(get_sum_quan(approval_path, "Disapproving"))
    print(get_sum_quan(approval_path, "Unsure/NoData"))
    print(get_sum_quan(approval_path, "Republicans Approving"))
    print(get_sum_quan(approval_path, "Democrats Approving"))
    print(get_sum_quan(approval_path, "Independents Approving"))

    # House Summaries 
    print(get_sum_quan(house_path, "Democrats"))
    print(get_sum_quan(house_path, "Republicans"))
    print(get_unique_values(house_path ,"Majority"))
    

    # Senate Summaries
if __name__ == "__main__":
    main()