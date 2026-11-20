import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
# print statements are used to represent tests


def make_congress(senate: pd.DataFrame, house: pd.DataFrame) -> pd.DataFrame:
    """
    Combines the Senate and House dataframes into a single dataframe
    """
    # Merge the two dataframes on the 'Start Date' and 'End Date' columns
    congress = pd.merge(
        senate[['Start Date', 'End Date', 'Democrats', 'Republicans',
                                                       'Party']],
        house[['Number', 'Start Date', 'End Date', 'Democrats', 'Republicans',
                                                                'Majority']],
        on=['Start Date', 'End Date'],
        suffixes=('_Senate', '_House')
    )
    # Rename columns for clarity
    congress.rename(columns={'Democrats_Senate': 'Senate Democrats',
                             'Republicans_Senate': 'Senate Republicans',
                             'Democrats_House': 'House Democrats',
                             'Republicans_House': 'House Republicans'},
                    inplace=True)

    return congress


def make_ordersvscongress(orders: pd.DataFrame,
                          congress: pd.DataFrame) -> pd.DataFrame:
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


def make_ordersvsapprovalavg(orders: pd.DataFrame,
                             approval: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the Executive Orders dataframe with the Approval Ratings dataframe
    by how many orders were signed during each president's term and the average
    approval ratings.
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


def make_ordersvsapprovalmonthly(orders: pd.DataFrame,
                                 approval: pd.DataFrame) -> pd.DataFrame:
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


def make_orderscongressgraph(orders_vs_congress: pd.DataFrame) -> plt.figure:
    """
    Creates a bar graph of the number of executive orders signed
    during each Congress
    """
    sns.set_theme()
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    sns.barplot(x="Number", y="Orders", hue="Senate Democrats",
                data=orders_vs_congress, ax=ax[0])
    sns.barplot(x="Number", y="Orders", hue="House Democrats",
                data=orders_vs_congress, ax=ax[1])
    ax[0].set_title("Executive Orders Signed by Congress, hued by Senate")
    ax[1].set_title("Executive Orders Signed by Congress, hued by House")
    ax[0].tick_params(axis="x", labelrotation=90)
    ax[1].tick_params(axis="x", labelrotation=90)
    fig.subplots_adjust(hspace=0.5)
    return fig


def make_orderspresapprovalgraph(orders_vs_approval:
                                 pd.DataFrame) -> plt.figure:
    """
    Creates a bar graph of the number of executive orders signed during
    each president's term
    """
    sns.set_theme()
    fig, ax = plt.subplots(2, 1, figsize=(12, 6))
    sns.barplot(x="President", y="Orders", hue="Average Approval",
                data=orders_vs_approval, ax=ax[0])
    sns.barplot(x="President", y="Orders", hue="Average Approval",
                data=orders_vs_approval, ax=ax[1])
    ax1 = ax[1].twinx()
    sns.scatterplot(x="President", y="Average Approval",
                    data=orders_vs_approval, ax=ax1)
    ax[0].set_title
    ("Executive Orders Signed by President, hued by Average Approval")
    ax[1].set_title
    ("Executive Orders Signed by President, " +
     "with Average Approval as a scatter plot")
    ax[0].tick_params(axis="x", labelrotation=90)
    ax[1].tick_params(axis="x", labelrotation=90)
    fig.subplots_adjust(hspace=1)
    return fig


def make_ordersapprovalmonthlygraph(orders_vs_approval:
                                    pd.DataFrame) -> plt.figure:
    """
    Creates a bar graph of the number of executive orders
    signed during each month
    """
    sns.set_theme()
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    orders_vs_approval["Year-Month"] = orders_vs_approval
    ["Year-Month"].astype(str)
    sns.lineplot(x="Year-Month", y="Orders", data=orders_vs_approval, ax=ax[0])
    sns.barplot(x="Year-Month", y="Orders", data=orders_vs_approval, ax=ax[1])
    ax1 = ax[1].twinx()
    sns.lineplot(x="Year-Month", y="Average Approval",
                 data=orders_vs_approval, ax=ax1)
    ax[0].set_title("Executive Orders Signed by Month")
    ax[1].set_title("Average Approval by Month")
    ax[0].tick_params(axis="x", labelrotation=90)
    ax[1].tick_params(axis="x", labelrotation=90)
    fig.subplots_adjust(hspace=0.5)
    ax[0].set_xticks(ax[0].get_xticks()[::12])
    ax[1].set_xticks(ax[1].get_xticks()[::12])
    return fig


def main():
    # Points directly to the folder where THIS .py script is saved
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

    congress = make_congress(senate, house)
    # print(congress.head())

    orders_vs_congress = make_ordersvscongress(orders, congress)
    # print(orders_vs_congress.head())
    president_orders_vs_approval = make_ordersvsapprovalavg(orders, approval)
    # print(president_orders_vs_approval.head())
    monthly_orders_vs_approval = make_ordersvsapprovalmonthly(orders, approval)
    # print(monthly_orders_vs_approval.head())

    orders_congress_graph = make_orderscongressgraph(orders_vs_congress)
    orders_congress_graph.savefig(script_dir / "orders_congress_graph.png")

    orders_pres_approval_graph = make_orderspresapprovalgraph
    (president_orders_vs_approval)
    orders_pres_approval_graph.savefig
    (script_dir / "orders_pres_approval_graph.png")

    orders_monthly_approval_graph = make_ordersapprovalmonthlygraph
    (monthly_orders_vs_approval)
    orders_monthly_approval_graph.savefig
    (script_dir / "orders_monthly_approval_graph.png")


if __name__ == "__main__":
    main()
