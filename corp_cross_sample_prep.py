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
import numpy as np
import pandas as pd

# Get data for 2017
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

for losstype in losstypelist:
    loss_lag1 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 1, losstype), 0.)
    loss_lag2 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 2, losstype), 0.)
    loss_lag3 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 3, losstype), 0.)
    loss_lag4 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 4, losstype), 0.)
    loss_lag5 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 5, losstype), 0.)
    loss_lag6 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 6, losstype), 0.)
    loss_lag7 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 7, losstype), 0.)
    loss_lag8 += np.where(data_full.ASSESSMENT_YEAR == 2017,
                          get_loss_type(2017, 8, losstype), 0.)

data_full['LOSS_LAG1'] = loss_lag1
data_full['LOSS_LAG2'] = loss_lag2
data_full['LOSS_LAG3'] = loss_lag3
data_full['LOSS_LAG4'] = loss_lag4
data_full['LOSS_LAG5'] = loss_lag5
data_full['LOSS_LAG6'] = loss_lag6
data_full['LOSS_LAG7'] = loss_lag7
data_full['LOSS_LAG8'] = loss_lag8




data17 = data_full[data_full['ASSESSMENT_YEAR'] == 2017].reset_index()
count = len(data17)



# Average amounts per company from the 2017 full sample
total_returns = 781141.0

# Calculate weights
WGT2017 = total_returns / count

# Assume 10% growth rate in number of firms filing
weights_df = pd.DataFrame({'WT2017': [WGT2017] * count,
                           'WT2018': [WGT2017 * 1.1] * count,
                           'WT2019': [WGT2017 * 1.1**2] * count,
                           'WT2020': [WGT2017 * 1.1**3] * count,
                           'WT2021': [WGT2017 * 1.1**4] * count})

# Export results
data17.round(6)
data17.to_csv('cit_cross.csv', index=False)
weights_df.to_csv('cit_cross_wgts.csv', index=False)
