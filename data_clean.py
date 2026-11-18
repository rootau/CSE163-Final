import pandas as pd

from pathlib import Path

# Points directly to the folder where THIS .py script is saved
script_dir = Path(__file__).resolve().parent
senate_path = script_dir / "Senate.csv"
house_path = script_dir / "House.csv"
orders_path = script_dir / "Executive_Orders.csv"
approval_path = script_dir / "Approval_Rating.csv"

senate = pd.read_csv(senate_path, encoding="latin1")
house = pd.read_csv(house_path, encoding="latin1")
orders = pd.read_csv(orders_path, encoding="latin1")
approval = pd.read_csv(approval_path, encoding="latin1")

senate["Range"] = senate["Congress"].shift(-1)
senate = senate.dropna()
senate.to_csv(script_dir / "Cleaned_Senate.csv", index=False)

print(approval.head(1))