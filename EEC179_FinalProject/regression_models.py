"""
\file    regression_models.py
\brief   Comparison of several regression models ranging from simple, such as Linear, to 
         advanced models, such as CatBoost, on the Boston Housing Data set.
         List of all models:
            "Linear Regression"
            "Ridge"
            "Lasso"
            "Elastic Net"
            "Decision Tree"
            "Random Forest"
            "Extra Trees"
            "K Nearest Neighbors"
            "Bagging Regressor"
            "Gradient Boosting",
            "XGBoost"
            "CatBoost"
            "AdaBoost"
\author  Corbin Warmbier
         Akhil Sharma
\date    06/13/2024
"""

""" === [Imports] === """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate 

# Sklearn and ML Imports #
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split,   \
                                    GridSearchCV,       \
                                    learning_curve
from sklearn.linear_model import LinearRegression,      \
                                 Ridge,                 \
                                 Lasso,                 \
                                 ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor,         \
                             GradientBoostingRegressor, \
                             RandomForestRegressor,     \
                             ExtraTreesRegressor,       \
                             BaggingRegressor
from sklearn.metrics import r2_score,                   \
                            mean_absolute_error,        \
                            mean_squared_error
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

""" Main """
print("=== [Starting Program] ===")
df = pd.read_csv('BostonHousing.csv')  # Load the dataset
df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric
df.fillna(df.mean(), inplace=True)  # Handle missing values, if any

# Correlation Matrix and Visualizations #
corr_matrix = df.corr()

# Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix Heatmap')
plt.show()

# Pairplot of a few selected features
selected_features = ['lstat', 'rm', 'ptratio', 'medv']
sns.pairplot(df[selected_features])
plt.show()

# Boxplots
plt.figure(figsize=(20, 10))
sns.boxplot(data=df)
plt.xticks(rotation=90)
plt.title('Boxplot of all features')
plt.show()

# Histogram to check the distribution of medv (target variable)
plt.figure(figsize=(8, 6))
sns.histplot(df['medv'], bins=20, kde=True)
plt.title('Distribution of medv')
plt.show()

# Feature Scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop('medv', axis=1))
scaled_df = pd.DataFrame(scaled_features, columns=df.columns[:-1])

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_df)
pca_df = pd.DataFrame(data=pca_result, columns=['Principal Component 1', 'Principal Component 2'])
pca_df['medv'] = df['medv']

# Scatter plot of PC1 and PC2
plt.figure(figsize=(10, 8))
sns.scatterplot(x='Principal Component 1', y='Principal Component 2', hue='medv', palette='coolwarm', data=pca_df)
plt.title('PCA Result')
plt.show()

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop('medv', axis=1), df['medv'], test_size=0.2, random_state=42)

# Dict of models to evaluate
models = {
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "Elastic Net": ElasticNet(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor(),
    "Extra Trees": ExtraTreesRegressor(),
    "K Nearest Neighbors": KNeighborsRegressor(),
    "Bagging Regressor": BaggingRegressor(),
    "Gradient Boosting": GradientBoostingRegressor(),
    "XGBoost": XGBRegressor(),
    "CatBoost": CatBoostRegressor(verbose=0),
    "AdaBoost": AdaBoostRegressor()
}
performance = {}  # Dict of performance metrics for each model

# Function to calculate and print evaluation metrics
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    return r2, mae, mse, rmse

# Grid Search CV for hyperparameter tuning
param_grid = {
    "Ridge": {"alpha": [0.1, 1.0, 10.0]},
    "Lasso": {"alpha": [0.1, 1.0, 10.0]},
    "Elastic Net": {"alpha": [0.1, 1.0, 10.0], "l1_ratio": [0.2, 0.5, 0.8]},
    "Decision Tree": {"max_depth": [5, 10, 20]},
    "Random Forest": {"n_estimators": [50, 100, 200], "max_depth": [5, 10, 20]},
    "Extra Trees": {"n_estimators": [50, 100, 200], "max_depth": [5, 10, 20]},
    "K Nearest Neighbors": {"n_neighbors": [3, 5, 7]},
    "Bagging Regressor": {"n_estimators": [10, 50, 100]},
    "Gradient Boosting": {"n_estimators": [50, 100, 200], "learning_rate": [0.01, 0.1, 0.2]},
    "XGBoost": {"n_estimators": [50, 100, 200], "learning_rate": [0.01, 0.1, 0.2]},
    "CatBoost": {"iterations": [50, 100, 200], "learning_rate": [0.01, 0.1, 0.2]},
    "AdaBoost": {"n_estimators": [50, 100, 200], "learning_rate": [0.01, 0.1, 0.2]}
}

# Train and evaluate each model
for name, model in models.items():
    print(f"Training {name}...")
    if name in param_grid:
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid[name], cv=5, scoring='r2', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        print(f"Best parameters for {name}: {grid_search.best_params_}")
    else:
        best_model = model
        best_model.fit(X_train, y_train)
    
    r2, mae, mse, rmse = evaluate_model(best_model, X_test, y_test)
    performance[name] = {"R²": r2, "MAE": mae, "MSE": mse, "RMSE": rmse}
    print(f"{name} performance: R²={r2:.4f}, MAE={mae:.4f}, MSE={mse:.4f}, RMSE={rmse:.4f}")

# Convert performance dictionary to DataFrame for easier handling
performance_df = pd.DataFrame.from_dict(performance, orient='index')

# Determine the best model based on RMSE
best_model_name = performance_df['RMSE'].idxmin()
best_model_metrics = performance_df.loc[best_model_name]

# Print best model stats in a table
print("\nBest Model:")
print(tabulate([[best_model_name, best_model_metrics['R²'], best_model_metrics['MAE'], best_model_metrics['MSE'], best_model_metrics['RMSE']]], 
               headers=["Model", "R²", "MAE", "MSE", "RMSE"], tablefmt='psql'))

# Print all model performances for comparison in a table
print("\nAll Model Performances:")
print(tabulate(performance_df.reset_index(), headers=["Model", "R²", "MAE", "MSE", "RMSE"], tablefmt='psql'))

# Visualizations for the best model

# Residual Plot
def plot_residuals(y_test, y_pred, model_name):
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_pred, y=residuals)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title(f'Residual Plot for {model_name}')
    plt.show()

# Predicted vs Actual Plot
def plot_predicted_vs_actual(y_test, y_pred, model_name):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title(f'Predicted vs Actual for {model_name}')
    plt.show()

# Feature Importance Plot
def plot_feature_importance(model, model_name, feature_names):
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        feature_importance = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
        feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importance)
        plt.title(f'Feature Importance for {model_name}')
        plt.show()

# Learning Curve
def plot_learning_curve(model, X, y, model_name):
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=5, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10), scoring='r2')
    train_scores_mean = np.mean(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='Training score')
    plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='Cross-validation score')
    plt.xlabel('Training Size')
    plt.ylabel('Score')
    plt.title(f'Learning Curve for {model_name}')
    plt.legend(loc='best')
    plt.show()

# Visualizing best model performance
best_model = models[best_model_name]
best_model.fit(X_train, y_train)
y_pred_best = best_model.predict(X_test)

# Residual Plot
plot_residuals(y_test, y_pred_best, best_model_name)
plot_predicted_vs_actual(y_test, y_pred_best, best_model_name)
plot_feature_importance(best_model, best_model_name, X_train.columns)
plot_learning_curve(best_model, X_train, y_train, best_model_name)
