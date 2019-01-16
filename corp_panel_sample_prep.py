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

# Get full panel data
data_full = pd.read_excel('ITR6_2013_2015_PANEL_MERGE_SHORT_SAMPLE1.xlsx',
                          sheet_name='ITR6_2013_2015_PANEL_MERGE_SHOR')

# Rename some variables
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE',
           'TOTAL_INCOME_ALL':'GTI_BEFORE_LOSSES'}
data_full = data_full.rename(renames, axis=1)
data_full = data_full.fillna(0)

# Get results for 2013
data13 = data_full[data_full['ASSESSMENT_YEAR'] == 2013].reset_index()
count = len(data13)

# Variable list we need to use
varlist = ['INCOME_HP', 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS',
           'PRFT_GAIN_BP_SPECLTV_BUS', 'PRFT_GAIN_BP_SPCFD_BUS',
           'PRFT_GAIN_BP_INC_115BBF', 'ST_CG_AMT_1', 'ST_CG_AMT_2',
           'LT_CG_AMT_1', 'LT_CG_AMT_2']
# Average amounts for various measures
agg_results = {'no_returns': 781141.,
               'INCOME_HP': 134403176952 / 790443.,
               'PRFT_GAIN_BP_OTHR_SPECLTV_BUS': 11650386829465 / 783662.,
               'PRFT_GAIN_BP_SPECLTV_BUS': 2850073821 / 783662.,
               'PRFT_GAIN_BP_SPCFD_BUS': 27604158172 / 783662.,
               'PRFT_GAIN_BP_INC_115BBF': 147539582 / 783662.,
               'ST_CG_AMT_1': 82338302877 / 781141.,
               'ST_CG_AMT_2': 4641554226 / 781141.,
               'LT_CG_AMT_1': 250513034751 / 781141.,
               'LT_CG_AMT_2': 485197199930 / 781141.}

# Totals in the sample
sample_results = {'no_returns': count}
blowup_results = {}

for var in varlist:
    sample_results[var] = 1.0 * sum(data13[var]) / count
    blowup_results[var] = agg_results[var] / sample_results[var]

# Produce weights for each observation in 2013
WT2013 = np.array([agg_results['no_returns'] / sample_results['no_returns']] *
                  count)

# Export CSV and blowup results
blowup_df = pd.DataFrame(blowup_results)
blowup_df.round(6)
blowup_df.to_csv('cit_panel_blowup.csv', index=False)
data_full.round(6)
data_full.to_csv('cit_panel.csv', index=False)



