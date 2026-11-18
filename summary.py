import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def getSumQuan(pd: pd.dataframe, col: String):
    # Gets the summary of any quantitative values.

    return pd[col].describe()


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
    print(getSumQuan(house_path, "Democrats"))
    print(getSumQuan(house_path, "Republicans"))
if __name__ == "__main__":
    main()