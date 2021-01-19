import pandas as pd

import numpy as np
from numpy import mean, std

from matplotlib import pyplot

import sklearn
from sklearn import preprocessing
from sklearn.decomposition import PCA

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

X, Y = data[['Converted', 'Torque', 'Year']], data[predict]

scaler = preprocessing.StandardScaler().fit(X)
X = scaler.transform(X)

pca = PCA().fit(X)

data=X[0:,0:]
index=[i for i in range(len(X))]
columns=['Converted', 'Torque', 'Year']
X = pd.DataFrame(data=data, index=index, columns=columns)

loadings = pd.DataFrame(data=pca.components_.T * np.sqrt(pca.explained_variance_), columns=[f'PC{i}' for i in range(1, len(X.columns) + 1)], index=X.columns)
print(loadings.head())

pc1_loadings = loadings.sort_values(by='PC1', ascending=False)[['PC1']]
pc1_loadings = pc1_loadings.reset_index()
pc1_loadings.columns = ['Feature', 'Correlation']

pyplot.bar(x=pc1_loadings['Feature'], height=pc1_loadings['Correlation'])
pyplot.title('PCA PC1 Loading Scores')
pyplot.show()