from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

fd = pd.read_csv('WithoutGrossFinal.csv', index_col=0)

# split genres and add

genre = fd['genres']
count = 0
genre_num = pd.DataFrame()
for i in genre:
    s = i.split('|')

    for j in s:
        genre_num.at[count, j] = 1
    count = count + 1
del fd['genres']
genre_num = genre_num.fillna('0')

fd = fd.reset_index(drop=True)
#encode
x_list_encode = fd.select_dtypes(include=['object']).copy()
encode_data = pd.get_dummies(x_list_encode)
fd = fd.join(encode_data)
fd = fd.join(genre_num)

#removing currently unaffecting column (include later)
del fd['language']
del fd['color']
del fd['content_rating']

b = fd.gross_class
a = fd.drop('gross_class', axis=1)

A_train, A_test, b_train, b_test = train_test_split(a, b, test_size=0.2)

n_folds = 5

kfolds = KFold(n_splits=n_folds)
kfolds = kfolds.get_n_splits(A_train)

print('Proceed with training the random forest ')

# classifier accuracy score
clf_rf = RandomForestRegressor(n_estimators=1000, max_depth=10)
clf_rf = clf_rf.fit(A_train, b_train)
classifier_score = clf_rf.score(A_test, b_test)
print('the classifier accuracy scoreis {:.2f}'.format(classifier_score))

# average of cross-validation
score = cross_val_score(clf_rf, A_test, b_test, cv=kfolds)
print('The {}-fold cross-validation accuracy score for this classifier is {:.2f}'.format(n_folds, score.mean()))

x_1 = A_test['budget']
y_1 = clf_rf.predict(A_test)

plt.figure()
plt.scatter(x_1, y_1, color="green", label="max_depth=5")
plt.scatter(x_1, b_test, c="blue", label="data")
plt.ylabel("target")
plt.xlabel("data")
plt.title("Random Forest Regression")
plt.legend()
plt.show()
