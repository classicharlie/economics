import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fredapi import Fred
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms


# convert pandas ts to an mpl readable ts only for graphing
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# this is a very rudimentary login system so we can each use our own api keys
user = str(input('new script, who dis? '))

if user == 'charlie':
    fred = Fred(api_key='ecae2fc8d6c684847525a828ae7a3ab8')
    x = 1

elif user == 'noah':
    fred = Fred(api_key='9c9998bd36a2bdbcf4e13c63b0a5edaf')
    x = 2

elif user == 'anon':
    fred = Fred(api_key='') # register for a key at https://research.stlouisfed.org/docs/api/api_key.html
    x = 3

else:
    print('fuq u')
    user = input('u bitch, tell me one more goddamn time. ')
    x = 0


# this conditional houses our work
if x != 1:
    # take the series from FRED and convert it to a ts data frame
    ser1 = fred.get_series('GDP')
    df1 = ser1.to_frame(name='GDP')
    ser2 = fred.get_series('CPIAUCSL')
    df2 = ser2.to_frame(name='CPI')

    # join that shit
    df = df1.join(df2)

    # print that shit
    print(df.tail(10))

    # regress that shit
    lm = smf.ols('GDP ~ CPI', data=df).fit()


    # a quick breusch pagan test
    bptest = sms.het_breuschpagan(lm.resid, lm.model.exog)

    if bptest[1] < .05:
        lmadj = smf.ols('GDP ~ CPI', data=df).fit(cov_type='HC0')
        # this is for hederoskedasticity

    else:
        lmadj = smf.ols('GDP ~ CPI', data=df).fit(cov_type='none')
        # this is for homoskedasticity

    print(lmadj.summary())
    coefficients = lmadj.params
    print('\nthese are the coefficients:\n', coefficients)

    i = 1    # i := independent vairables
    while i < 2:
        if lmadj.pvalues[i] < .05:
            print('\nreject the null')

        else:
            print('\nlmao nice try fa66ot')


else:
    print('\nu hav a lil pp')