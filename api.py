# Import necessary libraries
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error
from flask import Flask, request, jsonify

# Load and preprocess data
data = pd.read_csv('charging_data.csv')

# Convert 'month' column to datetime format and set it as index
data['month'] = pd.to_datetime(data['month'])
data.set_index('month', inplace=True)

# Ensure 'kWhDelivered' is numeric
data['kWhDelivered'] = pd.to_numeric(data['kWhDelivered'])

# Drop any rows with missing values
data.dropna(inplace=True)

# Define features (X) and target (y)
features = ['MinTemp', 'MaxTemp', 'AvgTemp', 'AvgPrecipitation', 'AvgHumidity', 'AvgWindSpeed']
target = 'kWhDelivered'

X = data[features]
y = data[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the neural network model
model = Sequential([
    Dense(64, activation='relu', input_shape=(len(features),)),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1)
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

# Train the model
model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Root Mean Squared Error: {rmse}")

# Create Flask API
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    month = request.args.get('month')
    year = int(request.args.get('year'))

    # Convert month and year to datetime
    input_date = pd.to_datetime(f'{year}-{month}-01')

    # Prepare input features for prediction (assuming historical averages for weather data)
    avg_weather = data.loc[input_date.strftime('%Y-%m')].mean()

    # Scale input data using the same scaler used for training
    scaled_input = scaler.transform([avg_weather[features]])

    # Predict using the model
    prediction = model.predict(scaled_input)

    return jsonify({'predicted_kWh': prediction[0][0]})

if __name__ == '__main__':
    app.run(debug=True)
