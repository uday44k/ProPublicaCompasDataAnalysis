# -*- coding: utf-8 -*-
"""CompasDataBiasAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1me5X-jc8iHOaTWgnx_GSPS3pMaQg5Yq2
"""

import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

dataURL = 'https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv'
dfRaw = pd.read_csv(dataURL)

dfRaw.shape

dfFiltered = (dfRaw[['age', 'c_charge_degree', 'race', 'age_cat', 'score_text', 
             'sex', 'priors_count', 'days_b_screening_arrest', 'decile_score', 
             'is_recid', 'two_year_recid', 'c_jail_in', 'c_jail_out']]
             .loc[(dfRaw['days_b_screening_arrest'] <= 45) & (dfRaw['days_b_screening_arrest'] >= -45), :]
             )
print('Number of rows: {}'.format(len(dfFiltered.index)))

dfFiltered = dfFiltered.dropna()

dfFiltered_race = (dfRaw[['age', 'c_charge_degree', 'age_cat', 'score_text', 
             'sex', 'priors_count', 'days_b_screening_arrest', 'decile_score', 
             'is_recid', 'two_year_recid', 'c_jail_in', 'c_jail_out']]
             .loc[(dfRaw['days_b_screening_arrest'] <= 30) & (dfRaw['days_b_screening_arrest'] >= -30), :]
             .loc[dfRaw['is_recid'] != -1, :]
             .loc[dfRaw['c_charge_degree'] != 'O', :]
             .loc[dfRaw['score_text'] != 'N/A', :]
             )
print('Number of rows: {}'.format(len(dfFiltered.index)))

import statsmodels.api as sm
from statsmodels.formula.api import logit
catCols = ['score_text','age_cat','sex','c_charge_degree']
dfFiltered_race.loc[:,catCols] = dfFiltered_race.loc[:,catCols].astype('category')

# dfDummies = pd.get_dummies(data = dfFiltered.loc[dfFiltered['score_text'] != 'Low',:], columns=catCols)
dfDummies_race = pd.get_dummies(data = dfFiltered_race, columns=catCols)

# Clean column names
new_column_names = [col.lstrip().rstrip().lower().replace(" ", "_").replace("-", "_") for col in dfDummies_race.columns]
dfDummies_race.columns = new_column_names

# We want another variable that combines Medium and High
dfDummies_race['score_text_medhi'] = dfDummies_race['score_text_medium'] + dfDummies_race['score_text_high']

# dfFiltered2 = (dfRaw[['age', 'c_charge_degree', 'race', 'age_cat', 'score_text', 
#              'sex', 'priors_count', 'days_b_screening_arrest', 'decile_score', 
#              'is_recid', 'two_year_recid', 'c_jail_in', 'c_jail_out']]
#              )

# dfFiltered2 = dfFiltered2.dropna()

# import statsmodels.api as sm
# from statsmodels.formula.api import logit
# catCols = ['score_text','age_cat','sex','race','c_charge_degree']
# dfFiltered2.loc[:,catCols] = dfFiltered2.loc[:,catCols].astype('category')

# # dfDummies = pd.get_dummies(data = dfFiltered.loc[dfFiltered['score_text'] != 'Low',:], columns=catCols)
# dfDummies2 = pd.get_dummies(data = dfFiltered2, columns=catCols)

# # Clean column names
# new_column_names = [col.lstrip().rstrip().lower().replace(" ", "_").replace("-", "_") for col in dfDummies2.columns]
# dfDummies2.columns = new_column_names

# # We want another variable that combines Medium and High
# dfDummies2['score_text_medhi'] = dfDummies2['score_text_medium'] + dfDummies2['score_text_high']

# dfFiltered2

pd.crosstab(dfFiltered['score_text'],dfFiltered['race'])

pd.crosstab(dfFiltered['score_text'],dfFiltered['decile_score'])

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
sns.color_palette("ch:s=.60,rot=0.25", as_cmap=True)

sns.catplot(x='decile_score',palette='ch:.25',col="race", kind='count', hue='race', data=dfFiltered.loc[
                (dfFiltered['race'] == 'African-American') | (dfFiltered['race'] == 'Caucasian'),:
            ])



plt.ylabel('Count')

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
sns.color_palette("ch:s=.60,rot=0.25", as_cmap=True)

sns.catplot(x='decile_score',palette='ch:.25',col="race", kind='count', hue='race', data=dfFiltered.loc[
                (dfFiltered['race'] == 'African-American') | (dfFiltered['race'] == 'Caucasian'),:
            ])



plt.ylabel('Count')

# Commented out IPython magic to ensure Python compatibility.
from numpy.ma.core import count
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)

sns.catplot(x='two_year_recid',palette='ch:s=.25,rot=-.25',kind = 'count', hue='race', data=dfFiltered.loc[
                (dfFiltered['race'] == 'African-American') | (dfFiltered['race'] == 'Caucasian'),:
            ])

plt.title("Distribution of two_year_recid by Race")
plt.xlabel('Two Year Recid')
plt.ylabel('Count')

sns.pairplot(data=dfFiltered.loc[
                (dfFiltered['race'] == 'African-American') | (dfFiltered['race'] == 'Caucasian'),:
            ], hue='race', size=2.5);

import statsmodels.api as sm
from statsmodels.formula.api import logit
catCols = ['score_text','age_cat','sex','race','c_charge_degree']
dfFiltered.loc[:,catCols] = dfFiltered.loc[:,catCols].astype('category')

# dfDummies = pd.get_dummies(data = dfFiltered.loc[dfFiltered['score_text'] != 'Low',:], columns=catCols)
dfDummies = pd.get_dummies(data = dfFiltered, columns=catCols)

# Clean column names
new_column_names = [col.lstrip().rstrip().lower().replace(" ", "_").replace("-", "_") for col in dfDummies.columns]
dfDummies.columns = new_column_names

# We want another variable that combines Medium and High
dfDummies['score_text_medhi'] = dfDummies['score_text_medium'] + dfDummies['score_text_high']

# R-style specification
formula = 'two_year_recid ~ sex_female + age_cat_greater_than_45 + age_cat_less_than_25 + race_african_american + race_asian + race_hispanic + race_native_american + race_other + priors_count + c_charge_degree_m + score_text_medhi'

score_mod = logit(formula, data = dfDummies).fit()
print(score_mod.summary())

control = np.exp(-0.7934) / (1 + np.exp(-0.7934))
np.exp(-0.4566) / (1 - control + (control * np.exp(-0.4566)))

y= dfDummies.two_year_recid.values
x_data = dfDummies.drop(['two_year_recid'], axis = 1)

pd.to_datetime(x_data.c_jail_out)
pd.to_datetime(x_data.c_jail_in)

x_data["days_in_jail"] = (pd.to_datetime(x_data.c_jail_out) - pd.to_datetime(x_data.c_jail_in)).dt.days

x_data = x_data.drop(['c_jail_out','c_jail_in'], axis = 1)

# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# # transform data
# x = scaler.fit_transform(x_data)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data,y,test_size = 0.33)
#transpose matrices
x_train = x_train.T
y_train = y_train.T
x_test = x_test.T
y_test = y_test.T

print(x_train)
print(x_test)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# transform data
x_train = scaler.fit_transform(x_train)
lr = LogisticRegression(solver='lbfgs')
lr.fit(x_train.T,y_train.T)
y_pred = lr.predict(x_test.T)

print("Test Accuracy {:.2f}%".format(lr.score(x_test.T,y_test.T)*100))
tn, fp, fn, tp = confusion_matrix(y_test,y_pred).ravel()
print(confusion_matrix(y_test,y_pred))
sns.heatmap(confusion_matrix(y_test,y_pred),annot=True, cmap="Blues",fmt='d')
print("no of test",x_test.shape)
(tn, fp, fn, tp )

x_whole_test = x_test.T

x_whole_test['two_year_recid'] = y_test.T

x_whole_test.race_african_american.values

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
lr = LogisticRegression()
lr.fit(x_train.T,y_train.T)
y_pred = lr.predict(x_test.T)

print("Test Accuracy {:.2f}%".format(lr.score(x_test.T,y_test.T)*100))
tn, fp, fn, tp = confusion_matrix(x_whole_test['two_year_recid'].T,y_pred).ravel()
print(confusion_matrix(y_test,y_pred))
sns.heatmap(confusion_matrix(y_test,y_pred),annot=True, cmap="Blues")
print("no of test",x_test.shape)
(tn, fp, fn, tp )

from sklearn.metrics import det_curve

x_whole_test_afr = x_whole_test.loc[x_whole_test['race_african_american'] != 0, :]

x_whole_test_afr

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
x_test_afr = x_whole_test_afr.drop(['two_year_recid'], axis = 1)
y_test_afr = x_whole_test_afr.two_year_recid
y_pred_af = lr.predict(x_test_afr)
print(y_test_afr.shape, "udaa")
print(y_pred_af.shape, "kumarr")
from sklearn.metrics import accuracy_score
print("Accuracy of african:",accuracy_score(y_test_afr.T, y_pred_af))
# print("Test Accuracy {:.2f}%".format(lr.score(y_test_afr.reshape(-1, 1),y_pred_af.reshape(-1, 1))*100))
tn, fp, fn, tp = confusion_matrix(y_test_afr,y_pred_af).ravel()
print(confusion_matrix(y_test_afr,y_pred_af))
sns.heatmap(confusion_matrix(y_test_afr,y_pred_af),annot=True, cmap="Blues",fmt='d')
print("no of test",x_test_afr.shape)
(tn, fp, fn, tp )

x_whole_test_causian = x_whole_test.loc[x_whole_test['race_caucasian'] != 0, :]
x_whole_test_causian

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
x_test_cau = x_whole_test_causian.drop(['two_year_recid'], axis = 1)
y_test_cau = x_whole_test_causian.two_year_recid
y_pred_cau = lr.predict(x_test_cau)
print(y_test_cau.shape, "udaa")
print(y_pred_cau.shape, "kumarr")
from sklearn.metrics import accuracy_score
print("Accuracy:",accuracy_score(y_test_cau.T, y_pred_cau))
# ``print("Test Accuracy {:.2f}%".format(lr.score(y_test_afr.reshape(-1, 1),y_pred_af.reshape(-1, 1))*100))
tn, fp, fn, tp = confusion_matrix(y_test_cau,y_pred_cau).ravel()
print(confusion_matrix(y_test_cau,y_pred_cau))
sns.heatmap(confusion_matrix(y_test_cau,y_pred_cau),annot=True, cmap="Blues",fmt='d')
print("no of test",x_test_cau.shape)
(tn, fp, fn, tp )

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
lr = RandomForestClassifier()

lr.fit(x_train.T,y_train.T)
y_pred = lr.predict(x_test.T)

print("Test Accuracy {:.2f}%".format(lr.score(x_test.T,y_test.T)*100))
tn, fp, fn, tp = confusion_matrix(x_whole_test['two_year_recid'].T,y_pred).ravel()
print(confusion_matrix(y_test,y_pred))
sns.heatmap(confusion_matrix(y_test,y_pred),annot=True, cmap="Blues")
print("no of test",x_test.shape)
(tn, fp, fn, tp )

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
x_test_afr = x_whole_test_afr.drop(['two_year_recid'], axis = 1)
y_test_afr = x_whole_test_afr.two_year_recid
y_pred_af = lr.predict(x_test_afr)
print(y_test_afr.shape, "udaa")
print(y_pred_af.shape, "kumarr")
from sklearn.metrics import accuracy_score
print("Accuracy of african:",accuracy_score(y_test_afr.T, y_pred_af))
# print("Test Accuracy {:.2f}%".format(lr.score(y_test_afr.reshape(-1, 1),y_pred_af.reshape(-1, 1))*100))
tn, fp, fn, tp = confusion_matrix(y_test_afr,y_pred_af).ravel()
print(confusion_matrix(y_test_afr,y_pred_af))
sns.heatmap(confusion_matrix(y_test_afr,y_pred_af),annot=True, cmap="Blues")
print("no of test",x_test_afr.shape)
(tn, fp, fn, tp )

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
x_test_cau = x_whole_test_causian.drop(['two_year_recid'], axis = 1)
y_test_cau = x_whole_test_causian.two_year_recid
y_pred_cau = lr.predict(x_test_cau)
print(y_test_cau.shape, "udaa")
print(y_pred_cau.shape, "kumarr")
from sklearn.metrics import accuracy_score
print("Accuracy:",accuracy_score(y_test_cau.T, y_pred_cau))
# ``print("Test Accuracy {:.2f}%".format(lr.score(y_test_afr.reshape(-1, 1),y_pred_af.reshape(-1, 1))*100))
tn, fp, fn, tp = confusion_matrix(y_test_cau,y_pred_cau).ravel()
print(confusion_matrix(y_test_cau,y_pred_cau))
sns.heatmap(confusion_matrix(y_test_cau,y_pred_cau),annot=True, cmap="Blues")
print("no of test",x_test_cau.shape)
( tn, fp, fn, tp )

y_race= dfDummies_race.two_year_recid.values
x_data_raec = dfDummies_race.drop(['two_year_recid'], axis = 1)
x_data_raec["days_in_jail"] = (pd.to_datetime(x_data_raec.c_jail_out) - pd.to_datetime(x_data_raec.c_jail_in)).dt.days

x_data_raec = x_data_raec.drop(['c_jail_out','c_jail_in'], axis = 1)

from sklearn.model_selection import train_test_split
x_train_r, x_test_r, y_train_r, y_test_r = train_test_split(x_data_raec,y_race,test_size = 0.33)
#transpose matrices
x_train_r = x_train_r.T
y_train_r = y_train_r.T
x_test_r = x_test_r.T
y_test_r = y_test_r.T

print(x_train_r)
print(x_test_r)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
lr_r = LogisticRegression()
lr_r.fit(x_train_r.T,y_train_r.T)
y_pred_r = lr_r.predict(x_test_r.T)

print("Test Accuracy {:.2f}%".format(lr_r.score(x_test_r.T,y_test_r.T)*100))
tn, fp, fn, tp = confusion_matrix(y_test_r,y_pred_r).ravel()
print(confusion_matrix(y_test_r,y_pred_r))
sns.heatmap(confusion_matrix(y_test_r,y_pred_r),annot=True, cmap="Blues")
print("no of test",x_test_r.shape)
(tn, fp, fn, tp )

x_train = x_train.T

x_test = x_test.T

x_train_rr = x_train.drop(['race_caucasian','race_african_american','race_asian','race_hispanic','race_native_american','race_other'], axis = 1)
x_test_rr = x_test.drop(['race_caucasian','race_african_american','race_asian','race_hispanic','race_native_american','race_other'], axis = 1)

x_train = x_train.T
x_test = x_test.T

print(x_train)
print(x_test)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sns
lr_rr = LogisticRegression()
lr_rr.fit(x_train_rr,y_train.T)
y_pred_rr = lr_rr.predict(x_test_rr)

print("Test Accuracy {:.2f}%".format(lr_rr.score(x_test_rr,y_test.T)*100))
tn, fp, fn, tp = confusion_matrix(y_test,y_pred_rr).ravel()
print(confusion_matrix(y_test,y_pred_rr))
sns.heatmap(confusion_matrix(y_test,y_pred_rr),annot=True, cmap="Blues")
print("no of test",x_test_rr.shape)
(tn, fp, fn, tp )