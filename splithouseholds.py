import pandas as pd
import numpy as np


income_vars = [
    "INCSALARY", "INCNONAG", "INCAGLAB", "INCNREGA", "INCNONNREGA",
    "FM41C", "NF5", "NF25", "NF45", "IN1", "IN2", "IN3A", "IN3B", "IN4A",
    "IN4B", "IN5", "IN6", "IN7", "INCCROP", "INCAG", "INCOTHER"
]
min_age = 18  # minimum age to earn income
max_age = 65  # maximum age to earn income


def split_households(data):
    """
    Function to split up a household into individual members
    Parameters
    ----------
    data: Pandas DataFrame with household data
    Returns
    -------
    Pandas DataFrame of individual tax units
    """
    def count_memebers(df):
        """
        Counts the number of adults in the household as definied by min_age
        and max_age as well as the total number in that household
        """
        mask_code = 0
        num_adults = ((df["Age"] >= min_age) & (df["Age"] <= max_age)).sum()
        # ensure that there's at least one income earner
        if num_adults == 0:
            # count number older than max age
            num_adults = (df["Age"] > max_age).sum()
            mask_code = 1
            if num_adults == 0:
                num_adults = (df["Age"] < min_age).sum()
                mask_code = 2

        total = len(df)
        return num_adults, total, mask_code

    hh_path = "Demographic and other particulars of household members - Block 4  - Level 4 - 68.dta"
    household_demo = pd.read_stata(hh_path, columns=["HHID", "Age"])
    # convert to integer so that we can merge this later
    household_demo["HHID"] = household_demo["HHID"].astype(int)
    # count up the number of adults and total members for each household
    counts = household_demo.groupby("HHID").apply(count_memebers)
    count_df = counts.apply(pd.Series)
    count_df.columns = ["num_adults", "total_members", "mask_code"]
    count_df = count_df.reset_index()
    count_df["HHID"] = count_df["HHID"].astype(int)
    # merge count data onto the full dataframe
    data_count = data.merge(count_df, on="HHID", how="right")

    # columns in the consumption data that need to be divided
    consumption_cols = data_count.filter(regex=r"CONS_*|cwt").columns

    # split consumption among all household members
    for col in consumption_cols:
        data_count[col] = data_count[col] / data_count["total_members"]

    # split income among all adults
    for col in income_vars:
        data_count[col] = data_count[col] / data_count["num_adults"]

    # merge age data to income and consumption data
    merged_df = data_count.merge(household_demo, on="HHID", how="left")
    # zero out income data for those not within income earning age.
    # if no one in the household is within the income range, use the mask_code.
    # If mask_code is 1, then all the income is assigned to those above the
    # max age. If mask_code is 2, all the income is assigned to those below
    # the income range
    age_mask = (merged_df["Age"] >= min_age) & (merged_df["Age"] <= max_age)
    mask_code = merged_df["mask_code"]
    for col in income_vars:
        merged_df[col] = np.where(
            (age_mask) & (mask_code == 0), merged_df[col],
            np.where(
                (merged_df["Age"] > max_age) & (mask_code == 1),
                merged_df[col],
                np.where(
                    (merged_df["Age"] < min_age) & (mask_code == 2),
                    merged_df[col], 0.0
                )
            )
        )

    return merged_df
