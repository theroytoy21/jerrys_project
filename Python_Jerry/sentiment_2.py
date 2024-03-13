import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# This will update CSV file 'training_data' with information based on TODAY's tweets
# main()

df = pd.read_csv("training_data.csv", encoding='unicode_escape')
print(df.head())

# Encode the string columns to numerical values
le = LabelEncoder()

company_encoded = le.fit_transform(df['Company Name'])
df['Company Name Encoded'] = company_encoded

sentiment_e = le.fit_transform(df["Sentiment"])
df['Sentiment_Encoded'] = sentiment_e

X = df[['Tweet Count',
        'Sentiment_Encoded',
        'Positive',
        'Negative',
        'Neutral',
        # 'Date(UTC)',
        'Company Name Encoded',
        ]]

y = le.fit_transform(df['ESG'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# Calculate the coefficient of determination (R-squared)
# r2 = r2_score(y_test, y_pred)

# Print the results
print("Mean Squared Error:", mse)
# print("R-squared:", r2)
for test, pred in zip(y_test, y_pred):
    print(test,"|", pred)

def prediction(data):
    company = data[5]
    sentiment = data[1]
    a = le.fit_transform([company])
    b = le.fit_transform([sentiment])
    print("Encoded company:", a, "\nEncoded sentiment:",b)
    data[5] = a[0]
    data[1] = b[0]
    predicted_value = model.predict([data])
    return predicted_value[0]

x = [10, "neutral", 1, 1, 8, "AAPL"]
pred = prediction(x)
print('prediction:', pred)