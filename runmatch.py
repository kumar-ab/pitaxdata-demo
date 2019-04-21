import pandas as pd
from matchfiles import matchfiles
from addconsup import add_consump
from addincome import add_income
from splithouseholds import split_households


def runmatch(verbose=False):
    """
    Function to call all the other functions that match the records
    """
    if verbose:
        print("Reading Data")
    income_file = "36151-0002-Data.tsv"
    income_data = pd.read_csv(income_file, sep="\t", na_values=" ")
    if verbose:
        print("Matching files")
    match_index = matchfiles(income_data)
    match_index.to_csv("match_index.csv")
    if verbose:
        print("Adding consumption data")
    matched_consump = add_consump(match_index)
    # Drop HHID to prevent duplication of column name
    if verbose:
        print("Adding income data")
    income_data = income_data.drop("HHID", axis=1)
    combined_data = add_income(income_data, matched_consump)
    combined_data = combined_data.fillna(0.0)
    combined_data.to_csv("combined_data.csv")
    if verbose:
        print("Splitting up household data")
    split_data = split_households(combined_data)
    split_data.to_csv("surveryunits.csv")


if __name__ == "__main__":
    runmatch(verbose=True)
