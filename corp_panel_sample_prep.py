"""
This script prepares the panel data for 2013-2015 to be used for 2017-2019.

We assume that aggregate totals have already been calcuated for the full data.
They must be saved in some form, and we will store them in agg_results.

For now, we produce the sample weight and blow-up factorsfor the entire sample.
A subsequent improvement should produce aggregate results by industry/sector,
and produce weights and blow-up factors by industry/sector. 

We may also want to consider weight adjustments to target other results, such
as totals for other measures and the distribution of firm sizes.
"""
import pandas as pd
import numpy as np

# Get ful lpanel data
data_full = pd.read_excel('ITR6_2013_2015_PANEL_MERGE_SHORT_SAMPLE1.xlsx',
                          sheet_name='ITR6_2013_2015_PANEL_MERGE_SHOR')
# Get results for 2013
data13 = data_full[data_full['ASSESSMENT_YEAR'] == 2013].reset_index()
count = len(data13)
# Aggregate totals for various measures
agg_results = {'no_returns': 1}

# Totals in the sample
sample_results = {'no_returns': count}

# Produce weights for each observation in 2013
WT2013 = np.array([agg_results['no_returns'] / sample_results['no_returns']] *
                  count)

def calc_blowup(measure):
    """
    Calculates the blowup factor for measure. Measure must be a string matching
    a variable name in sample_results and an aggregate amount in agg_results.
    """
    total13 = sum(data13[measure] * WT2013)
    total17 = agg_results[measure]
    blowup = total17 / total13
    return blowup

