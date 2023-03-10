# -*- coding: utf-8 -*-
"""HW_04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fKgMZLyNFz6dlk6LbOpEMxFFi_nog3YE
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pylab
import scipy.stats as stats
import sklearn as sk

from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import r2_score as R2
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

data = pd.read_csv("/content/housing.csv")
data.head()

"""#EDA

##Scatter Plot

1. LSTAT : Percentage of lower status of the population.
2. INDUS : Proportion of non-retail business acres per town.
3. NOX : Nitric Oxide concentration (parts per 10 million).
4. RM : Average number of rooms per dwelling.
5. AGE : Proportion of owner-occupied units built prior to 1940.
6. MEDV : Median value of owner occupied homes in $1000s (TARGET).
"""

data_col = ['LSTAT','INDUS','NOX','RM','AGE','MEDV']
sns.pairplot(data[data_col], size = 2.5)
plt.tight_layout()
plt.show()

"""MEDV shows some linear relationship with RM.

##Statistical Inferences
"""

labels = list(data.columns)
n_cols = len(labels)
n_rows = len(data)

print("Number of Rows    : ", n_rows)
print("Number of Columns : ", n_cols)

#Creating empty list to save the number times we observe (int or float) or string or other
n = [] #int or float
s = [] #string
o = [] #other

for label in labels:
  N = 0
  S = 0
  O = 0
  #Iterating for each columns and checking to which category among string or (int or float) or other it belongs
  for i in data[label]:
    if type(i) == str:
      S += 1
    elif (type(i) == int) or (type(i) == float):
      N += 1
    else:
      O +=1  
  n.append(N)
  s.append(S)
  o.append(O)

Output = {
    "Label" : labels,
    "Number" : n,
    "String" : s,
    "Other" : o
}
Output = pd.DataFrame(Output)
Output

"""All the columns have a numeric entry"""

#Determining the statistics for most correlated feature variable i.e., RM
x = np.array(data['RM'])

#Mean, Variance and Standard Deviation
m = x.mean()
v = x.var()
std = x.std()
print(" Mean of 'RM'               : ", m)
print(" Variance of 'RM'           : ", v)
print(" Standard Deviation of 'RM' : ", std)
print("")
#nth percentile
def p(y, n):
  result = []
  for i in range( n+1):
    result.append(np.percentile(y, i*100/n))
  return result
#Printing the quantile for 'RM'
print("The Quantile values for 'RM' :", p(x,4))

#Printing the decile for 'RM'
print("The Decile values for 'RM'   :", p(x,10))

print("")

"""##QQ Plot"""

stats.probplot(data['RM'], dist = "norm", plot = pylab)
pylab.show()

"""The QQ plot shows that 'RM' is normally distributed with slightly heavy tails.

##Summary of data
"""

summary = data.describe()
print(summary)

"""##Scatter plot

Since the 'RM' show positive correlation with our target variable 'MEDV'
"""

plt.figure(figsize=[12,5])
plt.scatter(data['RM'], data['MEDV'])
plt.title("MEDV vs RM")
plt.xlabel('RM')
plt.ylabel('MEDV')
plt.show()

"""##Correlation"""

data.corr()

corrMat = pd.DataFrame(data.corr())
plt.figure(figsize =[12,5])
plt.title("Heat-map showing the correaltion matrix")
plt.pcolor(corrMat)
plt.show()



"""#Linear Regression

##Splitting data between test and train set
"""

X = data.drop('MEDV', axis = 1).values
y = data['MEDV'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =0.2, random_state = 42)
print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)

"""##Model Fitting"""

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Coefficients: ", model.coef_)
print("Intercept   : ",model.intercept_)

"""##MSE and R^2"""

mse = MSE(y_pred, y_test)
r2 = R2(y_pred, y_test)
print("MSE: ", mse)
print("R^2: ",r2)

plt.figure(figsize= [12,5])
plt.plot(y_test, label = "Testing Set")
plt.plot(y_pred,label = "Prediction Value")
plt.legend()
plt.title("Y-predicted and Y-true value plot")
plt.xlabel("Index")
plt.ylabel("Value")
plt.show()

plt.figure(figsize= [12,5])
plt.plot(y_pred - y_test, label = "Residual")
plt.plot(np.zeros_like(y_pred), c = 'black')
plt.xlabel("Index")
plt.ylabel("Residual")
plt.title("Residual Plot")
plt.legend()
plt.show()

"""#Ridge Regression

Testing values of alphas [0.1,0.5, 1, 5, 10,50, 100, 500, 1000, 5000, 10000]

Checking R^2 and MSE for each alpha
"""

alphas =[0.0001, 0.001, 0.005, 0.01, 0.05, 0.1,0.5, 1, 5, 10,50, 100, 500, 1000, 5000, 10000]
r2_r = 0
mse_r = 999999
alpha_r2 = 0
alpha_mse = 0

for alpha in alphas:
  ridge = Ridge(alpha = alpha)
  ridge.fit(X_train, y_train)

  y_pred = ridge.predict(X_test)

  r2 = R2(y_pred, y_test)
  mse = MSE(y_pred, y_test)

  if r2_r < r2:
    r2_r = r2
    alpha_r2 = alpha

  if mse_r > mse:
    mse_r = mse
    alpha_mse = alpha
  print("alpha = ", alpha," R2 = ", r2," MSE = ",mse)
print("###########################################################")
print("Alpha for highest R2 = ",alpha_r2," corresponding R2 = ",r2_r)
print("Alpha for lowest MSE = ",alpha_mse," corresponding MSE = ",mse_r)
print("###########################################################")

"""Highest R2 is for alpha = 0.001

Lowest MSE is for alpha = 100

###Plotting for best R2
"""

ridge_r2 = Ridge(alpha = alpha_r2)
ridge_r2.fit(X_train, y_train)
y_pred_r2_ridge = ridge_r2.predict(X_test)

plt.figure(figsize = [12,5])
plt.plot(y_pred_r2_ridge, label = 'Fitted Value with highest R2')
plt.plot(y_test, label = 'y test')
plt.title("Ridge Regression with alpha = "+str(alpha_r2))
plt.legend()
plt.xlabel('Index')
plt.ylabel('Value')
plt.show()

"""Plotting Residues"""

plt.figure(figsize=[12,5])
plt.plot(y_pred_r2_ridge - y_test, label = "Residual of best R2 model")
plt.plot(np.zeros_like(y_pred_r2_ridge), c = 'black')
plt.xlabel("Index")
plt.ylabel("Residual")
plt.title("Ridge: Residual Plot")
plt.legend()
plt.show()

"""###Plotting for best MSE"""

ridge_mse = Ridge(alpha = alpha_mse)
ridge_mse.fit(X_train, y_train)
y_pred_mse_ridge = ridge_mse.predict(X_test)

plt.figure(figsize = [12,5])
plt.plot(y_pred_mse_ridge, label = 'Fitted Value with lowest MSE')
plt.plot(y_test, label = 'y test')
plt.title("Ridge Regression with alpha = "+str(alpha_mse))
plt.legend()
plt.xlabel('Index')
plt.ylabel('Value')
plt.show()

"""Plotting Residue

"""

plt.figure(figsize=[12,5])
plt.plot(y_pred_mse_ridge - y_test, label = "Residual of best MSE model")
plt.plot(np.zeros_like(y_pred_mse_ridge), c = 'black')
plt.xlabel("Index")
plt.ylabel("Residual")
plt.title("Ridge: Residual Plot")
plt.legend()
plt.show()

"""#LASSO Regression"""

alphas =[0.0001, 0.001, 0.005, 0.01, 0.05, 0.1,0.5, 1, 5, 10,50, 100, 500, 1000, 5000, 10000]
r2_l = 0
mse_l = 999999
alpha_r2 = 0
alpha_mse = 0

for alpha in alphas:
  lasso = Lasso(alpha = alpha)
  lasso.fit(X_train, y_train)

  y_pred = lasso.predict(X_test)

  r2 = R2(y_pred, y_test)
  mse = MSE(y_pred, y_test)

  if r2_l < r2:
    r2_l = r2
    alpha_r2 = alpha

  if mse_l > mse:
    mse_l = mse
    alpha_mse = alpha
  print("alpha = ", alpha," R2 = ", r2," MSE = ",mse)
print("###########################################################")
print("Alpha for highest R2 = ",alpha_r2," corresponding R2 = ",r2_l)
print("Alpha for lowest MSE = ",alpha_mse," corresponding MSE = ",mse_l)
print("###########################################################")

"""###Plotting for best R2"""

lasso_r2 = Lasso(alpha = alpha_r2)
lasso_r2.fit(X_train, y_train)
y_pred_r2_lasso = lasso_r2.predict(X_test)

plt.figure(figsize = [12,5])
plt.plot(y_pred_r2_lasso, label = 'Fitted Value with highest R2')
plt.plot(y_test, label = 'y test')
plt.title("Lasso Regression with alpha = "+str(alpha_r2))
plt.legend()
plt.xlabel('Index')
plt.ylabel('Value')
plt.show()

"""Plotting Residue"""

plt.figure(figsize=[12,5])
plt.plot(y_pred_r2_lasso - y_test, label = "Residual of best R2 model")
plt.plot(np.zeros_like(y_pred_r2_lasso), c = 'black')
plt.xlabel("Index")
plt.ylabel("Residual")
plt.title("Lasso: Residual Plot")
plt.legend()
plt.show()

"""###Plotting best MSE model"""

lasso_mse = Lasso(alpha = alpha_mse)
lasso_mse.fit(X_train, y_train)
y_pred_mse_lasso = lasso_mse.predict(X_test)

plt.figure(figsize = [12,5])
plt.plot(y_pred_mse_lasso, label = 'Fitted Value with lowest MSE')
plt.plot(y_test, label = 'y test')
plt.title("Lasso Regression with alpha = "+str(alpha_mse))
plt.legend()
plt.xlabel('Index')
plt.ylabel('Value')
plt.show()

"""Plotting Residue"""

plt.figure(figsize=[12,5])
plt.plot(y_pred_mse_lasso - y_test, label = "Residual of best MSE model")
plt.plot(np.zeros_like(y_pred_mse_lasso), c = 'black')
plt.xlabel("Index")
plt.ylabel("Residual")
plt.title("Lasso: Residual Plot")
plt.legend()
plt.show()

"""#CONCLUSION

From EDA : 
1. We can see that MEDV is positively and almost linearly related to RM. Other features don't show a strong relationship with our target variable MEDV.
2. Therefore we investigate the statistics of RM calculating mean and variance and percentiles.
3. From the QQ plot we observe that RM is almost normally distributed with heavy tails.
4. From the Correlation matrix we observe the highest correlation of MEDV is with RM.

From Linear Regression:
1. We observe that after fitting simple linear regression considering all the features variable we get MSE:  24.291119474973616
R^2:  0.6333247469014329.
2. Since there are many features variable, we land up 'Overfitting'.

From Ridge and LASSO regression:
1. From Ridge regression we R2 = 0.6333247312799677 and MSE =  23.465902589086472. We try out different values of alpha to get lowest MSE and R2 value closet to 1.

  Alpha for highest R2 =  0.0001  
  Alpha for lowest MSE =  100 

2.  From LASSO regression we R2 = 0.633322658748273 and MSE = 24.287374337568103. We try out different values of alpha to get lowest MSE and R2 value closet to 1.

  Alpha for highest R2 =  0.0001  
  Alpha for lowest MSE =  0.005

3. We observe Ridge regression brought down MSE better than LASSO and R2 values are closer to one for LASSO regression. 
4. LASSO is used for feature selection and when we have many features it heavily penalizes the least significant features and removes it from our model and leading to better expression of target variable in terms of feature variable. This leads to improved R2 values.
5. Whereas Ridge regression penalizes but not removes the least significant features. Leading to comparable R2 values with linear regression but an improved MSE.


All of the modelling shows how regularization is helpful in cases where we have many features and when not all of them show a strong relationship with target variable.

#Signing
"""

print("My name is Ananya Singh")
print("My NetID is: as133")
print("I hereby certify that I have read the University policy on Academic Integrity and that I am not in violation.")

##Colab Link : https://colab.research.google.com/drive/1fKgMZLyNFz6dlk6LbOpEMxFFi_nog3YE?usp=sharing
