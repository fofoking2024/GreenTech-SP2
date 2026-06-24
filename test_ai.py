
from sklearn.linear_model import LinearRegression
import numpy as np

# بيانات الشهور
months = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
requests = np.array([10, 15, 18, 22, 25, 30])

# إنشاء النموذج
model = LinearRegression()
model.fit(months, requests)

# التنبؤ بالشهر 7
prediction = model.predict([[7]])

print("Predicted requests for month 7:", int(prediction[0]))