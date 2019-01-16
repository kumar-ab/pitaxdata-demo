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

# Get data for 2017
data17 = pd.read_excel('ITR6_2017_CROSS_SECTION_WB_TRNG_NEW.xlsx',
                       sheet_name='ITR6_2017_CROSS_SECTION_WB_TRNG')
count = len(data17)

# Rename some variables
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE',
           'TOTAL_INCOME_ALL':'GTI_BEFORE_LOSSES'}
data17 = data17.rename(renames, axis=1)
data17 = data17.fillna(0)

# Average amounts per company from the 2017 full sample
total_returns = 781141.0

# Calculate weights
WGT2017 = total_returns / count

# Assume 10% growth rate in number of firms filing
weights_df = pd.DataFrame({'WT2017': [WGT2017] * count,
                           'WT2018': [WGT2017 * 1.1] * count,
                           'WT2019': [WGT2017 * 1.1 * 1.1] * count})

# Export results
data17.round(6)
data17.to_csv('cit_cross.csv', index=False)
weights_df.to_csv('cit_cross_wgts.csv', index=False)
