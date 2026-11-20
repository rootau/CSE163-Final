import pandas as pd
import re
import numpy as np
from pathlib import Path
# print statements are used to present tests. 

# Points directly to the folder where THIS .py script is saved
script_dir = Path(__file__).resolve().parent
senate_path = script_dir / "Senate.csv"
house_path = script_dir / "House.csv"
orders_path = script_dir / "Executive_Orders.csv"
approval_path = script_dir / "Approval_Rating.csv"

senate = pd.read_csv(senate_path, encoding="latin1", skiprows=range(1, 147))
house = pd.read_csv(house_path, encoding="latin1", skiprows=158)
orders = pd.read_csv(orders_path, encoding="latin1")
approval = pd.read_csv(approval_path, encoding="latin1", header=None,
                       dtype=str, keep_default_na=False)

senate["Range"] = senate["Congress"].shift(-1)
senate = senate.dropna()
dates = senate["Range"].str.strip("()").str.split(" to ", expand=True)
senate["Start Date"] = pd.to_datetime(dates[0], format="%m/%d/%Y")
senate["End Date"] = pd.to_datetime(dates[1], format="%m/%d/%Y")
majority = senate["Majority"].str.split(" ", n=1, expand=True)
minority = senate["Minority"].str.split(" ", n=1, expand=True)
senate["Party"] = majority[1]
senate["Democrats"] = (
    majority[0].where(majority[1] == "Democrats",
                      minority[0])
)
senate["Republicans"] = (
    majority[0].where(majority[1] == "Republicans",
                      minority[0])
)
senate[["Democrats", "Republicans"]] = (
    senate[["Democrats", "Republicans"]].apply(pd.to_numeric)
)
senate.to_csv(script_dir / "Cleaned_Senate.csv", index=False)
# print(senate.head())


house[["Number", "Year Range"]] = house["Congress (Years)"].str.extract(
    r"(.+?)\s*\((.*?)\)"
)
dates = house["Year Range"].str.split(r"[-Ð]", expand=True)
house["Start Date"] = pd.to_numeric(dates[0], errors="coerce")
house["End Date"] = pd.to_numeric(dates[1], errors="coerce")
senate["Start Years"] = senate["Start Date"].dt.year
senate["End Years"] = senate["End Date"].dt.year
year_to_date = senate.set_index("Start Years")["Start Date"]
house["Start Date"] = house["Start Date"].map(year_to_date)
years_to_date = senate.set_index("End Years")["End Date"]
house["End Date"] = house["End Date"].map(years_to_date)
house["Democrats"] = pd.to_numeric(house["Democrats"], errors="coerce")
house["Republicans"] = pd.to_numeric(house["Republicans"], errors="coerce")
house["Majority"] = np.where(
    house["Democrats"] > house["Republicans"],
    "Democrats",
    "Republicans"
)
house = house.dropna()
house.to_csv(script_dir / "Cleaned_House.csv", index=False)
# print(house.head())


columns = [
    "President", "Start Date", "End Date",
    "Approving", "Disapproving", "Unsure/NoData",
    "Democrats Approving", "Independents Approving",
    "Republicans Approving"
]


def normalize_header(value):
    """
    Normalizes the header value to a standard format.
    """
    value = str(value).strip().lower().replace("�", "")
    value = re.sub(r"\s+", " ", value)

    if value == "president":
        return "President"
    if value.startswith("start date"):
        return "Start Date"
    if value.startswith("end date"):
        return "End Date"
    if value.startswith("approving"):
        return "Approving"
    if value.startswith("disapproving"):
        return "Disapproving"
    if value.startswith("unsure"):
        return "Unsure/NoData"
    if "democrat" in value:
        return "Democrats Approving"
    if "independent" in value:
        return "Independents Approving"
    if "republican" in value:
        return "Republicans Approving"

    return None


result = []
current_columns = {}

for _, row in approval.iterrows():

    # Detect a repeated header row
    if normalize_header(row.iloc[1]) == "Start Date":

        # Reset the column mapping for this section
        current_columns = {0: "President"}

        for i, value in enumerate(row):
            name = normalize_header(value)

            if name is not None:
                current_columns[i] = name

        continue

    if row.eq("").all():
        continue

    new_row = {}

    for i, column in current_columns.items():
        if row.iloc[i] != "":
            new_row[column] = row.iloc[i]

    if new_row.get("President") and new_row.get("Start Date"):
        result.append(new_row)


approval = pd.DataFrame(result, columns=columns)
approval["Start Date"] = pd.to_datetime(approval["Start Date"],
                                        format="%m/%d/%y")
approval["End Date"] = pd.to_datetime(approval["End Date"], format="%m/%d/%y")

approval["Start Date"] = approval["Start Date"].where(
    approval["Start Date"].dt.year <= 2026,
    approval["Start Date"] - pd.DateOffset(years=100)
)

approval["End Date"] = approval["End Date"].where(
    approval["End Date"].dt.year <= 2026,
    approval["End Date"] - pd.DateOffset(years=100)
)

insert_position = approval.index[
    approval["President"] == "Trump (1st)"
].min()

trump1 = approval[approval["President"] == "Trump (1st)"].copy()

# Combine rows with matching date ranges
trump1 = (
    trump1.groupby(["President", "End Date"], as_index=False)
    .first()
)

# Remove the original Trump (1st) rows
approval = approval[approval["President"] != "Trump (1st)"]

before = approval[approval.index < insert_position]
after = approval[approval.index > insert_position]

# Insert the combined rows between the two parts
approval = pd.concat(
    [before, trump1, after],
    ignore_index=True
)

approval_cols = ["Approving", "Disapproving", "Unsure/NoData"]

party_cols = [
    "Democrats Approving",
    "Independents Approving",
    "Republicans Approving"
]

# Check whether each row has any overall approval data
has_approval = approval[approval_cols].notna().any(axis=1)

# Check whether each row has any party approval data
has_party = approval[party_cols].notna().any(axis=1)

# Keep rows where both types of data are available
approval = approval[has_approval & has_party].copy()
approval.to_csv(script_dir / "Cleaned_Approval_Rating.csv", index=False)
# print(approval.head())

orders["signing_date"] = pd.to_datetime(orders["signing_date"],
                                        format="%m/%d/%y", errors="coerce")
orders["signing_date"] = orders["signing_date"].where(
    orders["signing_date"].dt.year <= 2026,
    orders["signing_date"] - pd.DateOffset(years=100)
)
orders.to_csv(script_dir / "Cleaned_Executive_Orders.csv", index=False)
# print(orders.head())
