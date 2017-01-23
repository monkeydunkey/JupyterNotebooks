# Analyzing credit card frauds


## Source : [Kaggle.com](https://www.kaggle.com/dalpozz/creditcardfraud)

## Description
The datasets contains transactions made by credit cards in September 2013 by european cardholders. This dataset present transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. The dataset is highly unbalanced, the positive class (frauds) account for 0.172% of all transactions.

It contains only numerical input variables which are the result of a PCA transformation. Unfortunately, due to confidentiality issues, we cannot provide the original features and more background information about the data. Features V1, V2, ... V28 are the principal components obtained with PCA, the only features which have not been transformed with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first transaction in the dataset. The feature 'Amount' is the transaction Amount, this feature can be used for example-dependant cost-senstive learning. Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise.

Given the class imbalance ratio, we recommend measuring the accuracy using the Area Under the Precision-Recall Curve (AUPRC). Confusion matrix accuracy is not meaningful for unbalanced classification.

The dataset has been collected and analysed during a research collaboration of Worldline and the Machine Learning Group (http://mlg.ulb.ac.be) of ULB (Université Libre de Bruxelles) on big data mining and fraud detection. More details on current and past projects on related topics are available on http://mlg.ulb.ac.be/BruFence and http://mlg.ulb.ac.be/ARTML

Please cite: Andrea Dal Pozzolo, Olivier Caelen, Reid A. Johnson and Gianluca Bontempi. Calibrating Probability with Undersampling for Unbalanced Classification. In Symposium on Computational Intelligence and Data Mining (CIDM), IEEE, 2015

## Exploratory Analysis
The [analysis.ipynb](https://github.com/monkeydunkey/JupyterNotebooks/blob/master/CreditCardAnalysis/Analysis.ipynb) notebook contains a basic EDA and multiple hypothesis tests to check for significant differences in patterns between fraudulent transaction and valid transactions. Following were the observations

1. Fraud transaction were evenly spread out throughout the day, especially night so having a boolean feature for night might help
2. There is on an average a higher amount spent in fradulent transactions but in absolute terms valid transactions have higher transaction value
3. There are 6 columns - V13, V15, V22, V23, V25, V26 for which there is no difference in values between valid and fraudulent tranasctions

## Feature Engineering and modelling
[Fraud Detection.ipynb](https://github.com/monkeydunkey/JupyterNotebooks/blob/master/CreditCardAnalysis/Fraud%20Detection.ipynb) contains the feature engineering and statistical modelling part of the analysis. The feature engineering is done based on the properties observed during the Exploratory Analysis. Random Forest was choosed for the prediction task with the parameters tuned using Cross Validation. The accuracy of the model is 0.999074340068 and the AUC ROC is 0.976120097595
