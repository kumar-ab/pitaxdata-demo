import numpy as np
import pandas as pd

data = pd.read_csv('SAMPLE_ITR/SAMPLE_AY_2017-18.TXT', sep='|')
data['AGEGRP'] = np.where(data.AGE < 60, 0,
                          np.where((data.AGE < 80) & (data.AGE >= 60), 1, 2))
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE'}
data = data.rename(renames, axis=1)
data.to_csv('pit.csv', index=False)
