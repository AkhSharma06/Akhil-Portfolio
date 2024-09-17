# Regression Models Comparison

This project compares several regression models ranging from simple (such as Linear Regression) to advanced models (such as CatBoost) on the Boston Housing dataset.

## Models Included

- Linear Regression
- Ridge
- Lasso
- Elastic Net
- Decision Tree
- Random Forest
- Extra Trees
- K Nearest Neighbors
- Bagging Regressor
- Gradient Boosting
- XGBoost
- CatBoost
- AdaBoost

## Getting Started

### Prerequisites

Make sure you have Python and pip installed. You can create a virtual environment to manage dependencies.

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/repo-name.git
   cd repo-name
   ```

2. Create and activate a virtual environment:

   ```sh
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

### Running the Code

To run the regression models comparison:

```sh
python3 regression_models.py
```

## Visualization

The script includes several visualizations:

- Correlation Matrix Heatmap
- Pairplot of selected features
- Boxplots of all features
- Histogram of the target variable (medv)
- PCA scatter plot

## Notes

- The best model currently alternates between Bagging Regressor and Gradient Boosting, depending on the dataset. Further improvements are needed.
- Consider adding Neural Network Regressors to the comparison. Due to time constraints, these might be best run in a separate script, and the results can be transferred.
- Any additional improvements or suggestions are welcome!

## Authors

- Corbin Warmbier
- Akhil Sharma

## File Structure

```
├── regression_models.py
├── requirements.txt
└── README.md
```

### regression_models.py

The main script that includes:

- Loading and preprocessing the dataset
- Visualizing the data
- Splitting the data into training and testing sets
- Defining and training various regression models
- Evaluating model performance
- Visualizing model performance

### requirements.txt

List of required Python packages:

```
numpy
pandas
matplotlib
seaborn
tabulate
scikit-learn
xgboost
catboost
```

## Example Output

### Best Model Performance

After running the script, you will see an output similar to the following for the best model:

```
Best Model:
+-------------------+----------+---------+---------+---------+
| Model             |       R² |     MAE |     MSE |    RMSE |
|-------------------+----------+---------+---------+---------|
| Bagging Regressor | 0.916357 | 1.95422 | 6.13389 | 2.47667 |
+-------------------+----------+---------+---------+---------+
```

### All Model Performances

The script will also display a comparison of all models:

```
All Model Performances:
+----+---------------------+----------+---------+----------+---------+
|    | Model               |       R² |     MAE |      MSE |    RMSE |
|----+---------------------+----------+---------+----------+---------|
|  0 | Linear Regression   | 0.668759 | 3.18909 | 24.2911  | 4.9286  |
|  1 | Ridge               | 0.668624 | 3.17886 | 24.301   | 4.92961 |
|  2 | Lasso               | 0.656971 | 3.14524 | 25.1556  | 5.01554 |
|  3 | Elastic Net         | 0.671038 | 3.13986 | 24.1241  | 4.91162 |
|  4 | Decision Tree       | 0.847464 | 2.49804 | 11.1861  | 3.34456 |
|  5 | Random Forest       | 0.895402 | 2.03418 |  7.67056 | 2.76958 |
|  6 | Extra Trees         | 0.866612 | 1.87553 |  9.78187 | 3.1276  |
|  7 | K Nearest Neighbors | 0.704644 | 3.34477 | 21.6596  | 4.65398 |
|  8 | Bagging Regressor   | 0.916357 | 1.95422 |  6.13389 | 2.47667 |
|  9 | Gradient Boosting   | 0.915632 | 1.91671 |  6.18701 | 2.48737 |
| 10 | XGBoost             | 0.906658 | 1.8315  |  6.84512 | 2.61632 |
| 11 | CatBoost            | 0.88813  | 1.87468 |  8.20384 | 2.86423 |
| 12 | AdaBoost            | 0.813217 | 2.51944 | 13.6975  | 3.70101 |
+----+---------------------+----------+---------+----------+---------+
```
