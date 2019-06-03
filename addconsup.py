import pandas as pd


def add_consump(match_index):
    """
    Function to add consumption data to the match index and return a DataFrame
    containing all consumption variables
    """
    gst_data = pd.read_csv("gst.csv")

    merged_data = pd.merge(gst_data, match_index, left_on="ID_NO",
                           right_on="HHID", how="right")

    return merged_data
