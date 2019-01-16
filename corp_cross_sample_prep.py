"""
This script prepares the cross-section sample for 2017. For now, we treat this
sample as being representative (even though it may not be). 

We assume that aggregate totals have already been calcuated for the full data.
They must be saved in some form, and we will store them in agg_results.

For now, we produce the sample weight for the entire sample. A subsequent
improvement should produce aggregate results by industry/sector, and produce
weights by industry/sector. 

We may also want to consider weight adjustments to target other results, such
as totals for other measures and the distribution of firm sizes.
"""
import pandas as pd
import numpy as np

# Get data for 2017
data_full = pd.read_excel('ITR6_2017_2013_PANEL_WITHOUTDUPL_14.01.2019.xlsx',
                          sheet_name='ITR6_2017_2013_PANEL_WITHOUTDUP')
data17 = data_full[data_full['ASSESSMENT_YEAR'] == 2017].reset_index()
count = len(data17)

# Aggregate totals for various measures
agg_results = {'no_returns': 1}

# Totals in the sample
sample_results = {'no_returns': count}

# Calculate weights
WGT2017 = agg_results['no_returns'] / sample_results['no_returns']

# Assume 10% growth rate in number of firms filing
weights_df = pd.DataFrame({'WT2017': [WGT2017] * count,
                           'WT2018': [WGT2017 * 1.1] * count,
                           'WT2019': [WGT2017 * 1.1 * 1.1] / count})
data17.to_csv('cit_cross.csv', index=False)
weights_df.to_csv('cit_cross_wgts.csv', index=False)
