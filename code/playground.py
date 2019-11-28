import sklearn
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import numpy as np

x = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y = [1, 3, 2, 0, -2]

model = linear_model.LinearRegression()
poly = PolynomialFeatures(degree=4)
x = poly.fit_transform(x)

model.fit(x, y)

sample = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
result = model.predict(poly.transform(sample))

print(result)
print(model.coef_, model.intercept_)
