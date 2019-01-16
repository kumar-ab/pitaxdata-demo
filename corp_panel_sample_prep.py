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
data_full = pd.read_excel('ITR6_2017_2013_PANEL_new.xlsx',
                          sheet_name='ITR6_2017_2013_PANEL_new')

# Rename some variables
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE',
           'TOTAL_INCOME_ALL':'GTI_BEFORE_LOSSES', 'PAN_NO_HASH': 'ID_NO',
           'AY_0910_AMT_AMT_LOSS_BUSOTHSPL': 'AY_0910_AMT_LOSS_BUSOTHSPL'}
data_full = data_full.rename(renames, axis=1)
data_full = data_full.fillna(0)

"""
The following code handles the losses.
"""
# Create empty loss variables
loss_lag8 = np.zeros(len(data_full))
loss_lag7 = np.zeros(len(data_full))
loss_lag6 = np.zeros(len(data_full))
loss_lag5 = np.zeros(len(data_full))
loss_lag4 = np.zeros(len(data_full))
loss_lag3 = np.zeros(len(data_full))
loss_lag2 = np.zeros(len(data_full))
loss_lag1 = np.zeros(len(data_full))

def get_loss_type(year, lagnum, losstype):
    """
    Returns an array of the given loss type with the appropriate lag from the
    given year.
    """
    loss = np.zeros(len(data_full))
    lagyear = year - lagnum
    if lagyear < 2007:
        loss = np.zeros(len(data_full))
    elif lagyear == 2007:
        loss = np.array(data_full['AY_0708_AMT_LOSS_' + losstype])
    elif lagyear == 2008:
        loss = np.array(data_full['AY_0809_AMT_LOSS_' + losstype])
    elif lagyear == 2009:
        loss = np.array(data_full['AY_0910_AMT_LOSS_' + losstype])
    elif lagyear == 2010:
        loss = np.array(data_full['AY_1011_AMT_LOSS_' + losstype])
    elif lagyear == 2011:
        loss = np.array(data_full['AY_1112_AMT_LOSS_' + losstype])
    elif lagyear == 2012:
        loss = np.array(data_full['AY_1213_AMT_LOSS_' + losstype])
    elif lagyear == 2013:
        loss = np.array(data_full['AY_1314_AMT_LOSS_' + losstype])
    elif lagyear == 2014:
        loss = np.array(data_full['AY_1415_AMT_LOSS_' + losstype])
    else:
        loss = np.zeros(len(data_full))
    loss2 = np.where(data_full.ASSESSMENT_YEAR == year, loss, 0)
    return loss2

losstypelist = ['HPL', 'BUSOTHSPL', 'LSPCLTVBUS', 'LSPCFDBUS', 'STCL', 'LTCL',
                'OSLHR']

for year in range(2013, 2018):
    for losstype in losstypelist:
        loss_lag1 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 1, losstype), 0.)
        loss_lag2 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 2, losstype), 0.)
        loss_lag3 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 3, losstype), 0.)
        loss_lag4 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 4, losstype), 0.)
        loss_lag5 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 5, losstype), 0.)
        loss_lag6 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 6, losstype), 0.)
        loss_lag7 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 7, losstype), 0.)
        loss_lag8 += np.where(data_full.ASSESSMENT_YEAR == year,
                              get_loss_type(year, 8, losstype), 0.)

data_full['LOSS_LAG1'] = loss_lag1
data_full['LOSS_LAG2'] = loss_lag2
data_full['LOSS_LAG3'] = loss_lag3
data_full['LOSS_LAG4'] = loss_lag4
data_full['LOSS_LAG5'] = loss_lag5
data_full['LOSS_LAG6'] = loss_lag6
data_full['LOSS_LAG7'] = loss_lag7
data_full['LOSS_LAG8'] = loss_lag8


"""
The following code deals with the calculation of blow-up factors.
The blow-up factors are calculated to match 2013 results to 2017 results, with
2017 results calculated from the complete data and 2013 from the sample.
"""

# Get results for 2013
data13 = data_full[data_full['ASSESSMENT_YEAR'] == 2013].reset_index()
count = len(data13)

# Variable list we need to use
varlist = ['INCOME_HP', 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS',
           'PRFT_GAIN_BP_SPECLTV_BUS', 'PRFT_GAIN_BP_SPCFD_BUS',
           #'PRFT_GAIN_BP_INC_115BBF',
           'ST_CG_AMT_1', 'ST_CG_AMT_2',
           'LT_CG_AMT_1', 'LT_CG_AMT_2', 'AGGREGATE_LIABILTY']
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
               'LT_CG_AMT_2': 485197199930 / 781141.,
               'AGGREGATE_LIABILTY': 3954771854602 / 790443.}

# Totals in the sample
sample_results = {'no_returns': count}
blowup_results = {}

for var in varlist:
    sample_results[var] = 1.0 * sum(data13[var]) / count
    if sample_results[var] != 0:
        blowup_results[var] = [agg_results[var] / sample_results[var]]
    else:
        blowup_results[var] = [1.0]

# Produce weights for each observation in 2013
WT2013 = np.array([agg_results['no_returns'] / sample_results['no_returns']] *
                  count)
# Assume 10% growth rate in number of firms filing
weights_df = pd.DataFrame({'WT2017': [WT2013] * count,
                           'WT2018': [WT2013 * 1.1] * count,
                           'WT2019': [WT2013 * 1.1 * 1.1] * count})


# Export CSV and blowup results
blowup_df = pd.DataFrame.from_dict(blowup_results)
blowup_df.round(6)
blowup_df.to_csv('cit_panel_blowup.csv', index=False)
data_full.round(6)
data_full.to_csv('cit_panel.csv', index=False)


