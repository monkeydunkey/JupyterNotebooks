## approach.py
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LassoCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
import xgboost as xgb


train = pd.read_csv('Data/train.csv')
## Removing high leverage points
##train = train[(train['loss'] <= 40000) & (train.cont7 > 0.1)]
test = pd.read_csv('Data/test.csv')

test['loss'] = np.nan
joined = pd.concat([train, test])

def evalerror(preds, dtrain):
    labels = dtrain.get_label()
    return 'mae', mean_absolute_error(np.exp(preds), np.exp(labels))

def logregobj(preds, dtrain):
    labels = dtrain.get_label()
    con =2
    x =preds-labels
    grad =con*x / (np.abs(x)+con)
    hess =con**2 / (np.abs(x)+con)**2
    return grad, hess

def split_cont6(val):
    if(val >= 0.158):
        return 1
    else:
        return 0

if __name__ == '__main__':
    rows = joined.shape[0]
    for column in list(train.select_dtypes(include=['object']).columns):
        if train[column].nunique() != test[column].nunique():
            set_train = set(train[column].unique())
            set_test = set(test[column].unique())
            remove_train = set_train - set_test
            remove_test = set_test - set_train

            remove = remove_train.union(remove_test)
            def filter_cat(x):
                if x in remove:
                    return np.nan
                return x

            joined[column] = joined[column].apply(lambda x: filter_cat(x), 1)
        '''
        temp = joined.groupby(column).count()['id']
        mapObj = {}
        data = temp.values.astype(float)/rows
        ind = 0
        for d in data:
            if d < .02:
                mapObj[temp.index[ind]] = 'Other'
            else:
                mapObj[temp.index[ind]] = temp.index[ind]
                ind+=1
        print column, 'Before Map'
        joined[column] = joined[column].map(mapObj)
        '''
        joined[column] = pd.factorize(joined[column].values, sort=True)[0]
    joined['cont6_split'] = joined['cont6'].apply(split_cont6)
    #joined = pd.get_dummies(joined)
    train = joined[joined['loss'].notnull()]
    test = joined[joined['loss'].isnull()]

    shift = 200
    y = np.log(train['loss'] + shift)
    ids = test['id']
    X = train.drop(['loss', 'id'], 1)
    X_test = test.drop(['loss', 'id'], 1)

    RANDOM_STATE = 2016
    params = {
        'min_child_weight': 1,
        'eta': 0.01,
        'colsample_bytree': 0.5,
        'max_depth': 12,
        'subsample': 0.8,
        'alpha': 1,
        'gamma': 1,
        'silent': 1,
        'verbose_eval': True,
        'seed': RANDOM_STATE
    }

    xgtrain = xgb.DMatrix(X, label=y)
    xgtest = xgb.DMatrix(X_test)

    model = xgb.train(params, xgtrain, int(2012 / 0.9), feval=evalerror, obj=logregobj)

    prediction = np.exp(model.predict(xgtest)) - shift

    submission = pd.DataFrame()
    submission['loss'] = prediction
    submission['id'] = ids
    submission.to_csv('attempt.csv', index=False)
