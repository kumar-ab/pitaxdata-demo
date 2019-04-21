import pandas as pd


def add_income(income_data, match_index):
    """
    Function to match income data to the match index
    """
    merged_data = pd.merge(income_data, match_index, on="IDHH", how="right")

    return merged_data
