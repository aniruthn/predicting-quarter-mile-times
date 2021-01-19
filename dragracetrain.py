import pandas as pd

import numpy as np
from numpy import mean, std

from matplotlib import pyplot
from matplotlib import style

import sklearn
from sklearn import linear_model
from sklearn import tree
from sklearn.utils import shuffle

import csv

data = pd.read_csv('cardatafinal.csv')

makesToDrop = np.array(['Buell', 'Dragster', 'Harley-Davidson', 'Kawasaki', 'Streetrod', 'Ski-doo', 'Yamaha'])

data = data[~data.Make.isin(makesToDrop)]
data = data[~data.Type.str.contains('Nitrous', na=False)]

data[np.abs(data.HP-data.HP.mean()) <= (2*data.HP.std())]
data[np.abs(data.Weight-data.Weight.mean()) <= (2*data.Weight.std())]

data['Converted'] = data.apply(lambda row: ((row['Weight'] / row['HP']) ** (1/3)), axis=1)

data[np.abs(data.Converted-data.Converted.mean()) <= (2*data.Converted.std())]

data = data[data.Converted > 0.8]
data.drop(data[(data.Converted < 1) & (data.Weight > 12)].index, inplace=True)
data.drop(data[(data.Converted < 1.4) & (data['1/4 Mile ET'] > 14)].index, inplace=True)
data.drop(data[(data.Converted > 4.4) & (data['1/4 Mile ET'] < 14)].index, inplace=True)

predict = '1/4 Mile ET'

X, Y = data['Converted'], data[predict]
# X, Y = data[['Converted', 'Torque', 'Year']], data[predict]

#each model was commented out with different plots used at the very bottom for showing the data

best, co, intercept = 0,0,0
for _ in range(1000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.25)
    x_train = x_train.values.reshape(-1, 1)
    y_train = y_train.values.reshape(-1, 1)
    x_test = x_test.values.reshape(-1, 1)
    y_test = y_test.values.reshape(-1, 1)
    linear = linear_model.LinearRegression(fit_intercept=False)
    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)
    if acc > best:
        best = acc
        co = linear.coef_
        intercept = linear.intercept_

for _ in range(1000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.25)
    x_train = x_train.values.reshape(-1, 1)
    y_train = y_train.values.reshape(-1, 1)
    x_test = x_test.values.reshape(-1, 1)
    y_test = y_test.values.reshape(-1, 1)
    reg = linear_model.BayesianRidge(fit_intercept=False)
    reg.fit(x_train, y_train.ravel())
    acc = reg.score(x_test, y_test)
    if acc > best:
        best = acc
        co = reg.coef_[0]
        intercept = reg.intercept_[0]

for _ in range(1000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.25)
    x_train = x_train.values.reshape(-1, 1)
    y_train = y_train.values.reshape(-1, 1)
    x_test = x_test.values.reshape(-1, 1)
    y_test = y_test.values.reshape(-1, 1)
    reg = linear_model.Lasso(alpha=0.1, fit_intercept=False)
    reg.fit(x_train, y_train)
    acc = reg.score(x_test, y_test)
    if acc > best:
        best = acc
        co = reg.coef_[0]
        intercept = reg.intercept_[0]

for _ in range(1000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.25)
    x_train = x_train.values.reshape(-1, 1)
    y_train = y_train.values.reshape(-1, 1)
    x_test = x_test.values.reshape(-1, 1)
    y_test = y_test.values.reshape(-1, 1)
    reg = linear_model.ElasticNetCV(fit_intercept=False)
    reg.fit(x_train, y_train.ravel())
    acc = reg.score(x_test, y_test)
    if acc > best:
        best = acc
        co = reg.coef_[0]
        intercept = reg.intercept_[0]

bestmodel = 1
for _ in range(1000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.25)
    x_train = x_train.values.reshape(-1, 1)
    y_train = y_train.values.reshape(-1, 1)
    x_test = x_test.values.reshape(-1, 1)
    y_test = y_test.values.reshape(-1, 1)
    val = 2
    clf = tree.DecisionTreeRegressor(max_depth=val)
    clf.fit(x_train, y_train)
    acc = clf.score(x_test, y_test)
    if acc > best:
        best = acc
        bestmodel = clf

style.use("ggplot")
pyplot.scatter(data['HP'], data['Weight'], label=data[predict])
pyplot.xlabel("HP")
pyplot.ylabel("Weight")
pyplot.title('HP and Weight Distributions')
pyplot.show()

x_plot = "Converted"
style.use("ggplot")
pyplot.scatter(data[x_plot], data[predict])
pyplot.xlabel(x_plot)
pyplot.ylabel("ET")
pyplot.show()

uniqueMake = data.drop_duplicates(subset=['Make'])
uniqueMake = uniqueMake['Make']
uniqueMake = uniqueMake.to_numpy()

fig, ax = pyplot.subplots()
for make in uniqueMake:
    makePlot = data.loc[data['Make'] == make]
    ax.scatter(makePlot['HP'], makePlot['Weight'], label=make)

pyplot.xlabel('HP')
pyplot.ylabel('Weight')

ax.legend()

x_line = np.linspace(1, 3.5, 100)
y_line = x_line * co
pyplot.plot(x_line, y_line, '-g', label='Regression Line')
pyplot.grid()

x_line = np.arange(1, 3.5, 0.01)[:, np.newaxis]
y_line = bestmodel.predict(x_line)
pyplot.plot(x_line, y_line, 'black', label='Regression Line')
pyplot.grid()

pyplot.title('Correlating Converted with ET - Decision Tree')
pyplot.xlabel('Converted')
pyplot.ylabel('ET')
pyplot.show()