# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nsm_3lUvHDwEqiyeKnxNTlSrWmRqC-r8
"""

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df = sns.load_dataset('mpg')
df.head()

df.isnull().sum()

df.describe()

df.shape

sns.boxplot(df['horsepower'])

sns.boxplot(df['weight'])

sns.boxplot(df['acceleration'])

sns.boxplot(df['displacement'])

def remove_outlier(df, col):
  lower_limit = df[col].quantile(0.05)
  upper_limit = df[col].quantile(0.95)
  df = df[(df[col] > lower_limit) & (df[col] < upper_limit)]
  return df

df = remove_outlier(df, 'horsepower')
df = remove_outlier(df, 'weight')
df.shape

sns.boxplot(df['horsepower'])

sns.boxplot(df['acceleration'])

sns.histplot(df['acceleration'], kde=True)
sns.histplot(df['displacement'], kde=True)

sns.histplot(df['horsepower'], kde=True)


sns.histplot(df['weight'], kde=True)

df['log_displacement'] = np.log(df['displacement'] + 1)  # +1 to avoid log(0)
sns.histplot(df['log_displacement'], kde=True)

df['log_horsepower'] = np.log(df['horsepower'] + 1)
sns.histplot(df['log_horsepower'], kde=True)


df['log_weight'] = np.log(df['weight'] + 1)
sns.histplot(df['log_weight'], kde=True)

from scipy.stats import zscore
df['acceleration'] = zscore(df['acceleration'])

sns.histplot(df['acceleration'], kde=True)
plt.show()

df.head()

"""# Linear Regression"""

numerical_features = ['cylinders', 'acceleration', 'log_displacement', 'log_horsepower', 'log_weight']
X = df[numerical_features]
y = df['mpg']

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import mlflow
# Function to log model and metrics with MLflow
def log_model_with_mlflow(model, model_name):
    with mlflow.start_run():
        # Train the model
        model.fit(X_train, y_train)

        # Predict on test data
        y_pred = model.predict(X_test)

        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Log metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)

        # Log the model
        mlflow.sklearn.log_model(model, model_name)
        
        print(f"{model_name} logged with MSE: {mse} and R2: {r2}")
        
    mlflow.end_run()

"""# Linear Regression"""
lr=LinearRegression()
log_model_with_mlflow(lr, "Linear Regression")

"""# Random Forest"""

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
log_model_with_mlflow(rf, "Random Forest")
