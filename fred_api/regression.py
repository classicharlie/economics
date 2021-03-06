import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from fredapi import Fred
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms


# convert pandas ts to an mpl readable ts only for graphing
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# this is a very rudimentary login system so we can each use our own api keys
answer = str(input('do you have an api key?'))

yay = ['y']
nay = ['n']

# still unsure about the login system since it does hinder usability
for response in range(0, len(yay)):
    if answer.lower() == yay[response]:
        key = str(input('api key: '))
        fred = Fred(api_key=key)
        x = 1
        break

    elif answer.lower() == nay[response]:
        print('get one using the link in the instructions')
        x = 0
        break

    else:
        x = 0


# this conditional houses our work
if x == 1:
    txt_init = str(input('which datasets do you want? ')).upper()
    txt = txt_init.replace(' ', '')
    datasets = txt.split(',')

    ser = fred.get_series(datasets[0])
    df = ser.to_frame(name=str(datasets[0]))

    for set in datasets:
        if datasets.index(set) == 0:
            continue
        ser1 = fred.get_series(set)
        df1 = ser1.to_frame(name=set)
        df = pd.concat([df, df1], axis=1)

    print(df.tail(10))

    # splits the known list items into dependent and indepentent variables
    print('choose your dependent variable:')
    count = 0

    for options in datasets:
        count += 1
        print('[%d] %s' % (count, options))

    # this creates a string for our dependent variable
    dependent = str(input('which one do you want to test? '))
    lmd = dependent + ' ~ '
    lm2 = []

    # this identifies the non dependent variables using the conditional
    for z in datasets:
        if dependent != z:
            lm2.append(z)

    # the desired output is a string we can reuse for more post hoc tests
    sep = ' + '
    lmi = sep.join(lm2)
    formula = str(lmd + lmi)
    lm = smf.ols(formula, data=df).fit()

    # a quick breusch pagan test for hedero/homoskedasticity
    bptest = sms.het_breuschpagan(lm.resid, lm.model.exog)

    if bptest[1] < .05:
        lmadj = smf.ols(formula, data=df).fit(cov_type='HC0')
        # this is for hederoskedasticity

    else:
        lmadj = smf.ols(formula, data=df).fit(cov_type=None)
        # this is for homoskedasticity

    print(lmadj.summary())
    coefficients = lmadj.params
    print('\nthese are the coefficients:\n', coefficients)

    i = len(datasets)  # i := independent vairables

    if i < 2:
        if lmadj.pvalues[i] < .05:
            print('reject the null')

        else:
            print('lmao u thought')

    # matplotlib functionality finally is starting to work
    plt.plot(df)
    plt.show()


elif x == 0:
    print('that ain\'t it cheif\nu prolly derive smallest')
    x = 0
