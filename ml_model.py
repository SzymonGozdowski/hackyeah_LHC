from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas as pd

data = pd.read_csv("attractions_light.csv", header=None)

X = data["lat", "lon"]
y = data.drop(columns=["lat", "lon"])

X_train, X_test, y_train, y_test = train_test_split(X, y)

knn = KNeighborsRegressor()
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(y_pred)

r2 = r2_score(y_test, y_pred)
print(r2)
