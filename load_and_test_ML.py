"""
    TEST MODEL AGAINST TEST DATASET
"""
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from pandas import DataFrame

# -- Load the pre-trained model --
model = keras.models.load_model(os.path.abspath(os.path.join("model", "LSTM_1_model_saved_model")))

# -- Load the test dataset --
test = pd.read_csv(os.path.join("dataset", "test.csv"))

# -- Ensure the new data is preprocessed in the same way as the training data --
scaler = MinMaxScaler()
# X_new = test[['arrival_hour', 'arrival_minute', 'stop_lat', 'stop_lon', 'next_lat', 'next_lon']]
X_new = test[['arrival_hour', 'arrival_minute', 'stop_lat', 'stop_lon', 'next_lat', 'next_lon', 'speed_kmh',
              'segment_max_speed_kmh', 'runtime_sec', 'direction_id', 'distance_m']]
X_new = scaler.fit_transform(X_new)

# -- Define the sequence length (seq_length) used during training --
seq_length = 64

# -- Generate sequences from the new data --
X_seq_new = []

for i in range(len(X_new) - seq_length + 1):
    sequence = X_new[i:i + seq_length]
    X_seq_new.append(sequence)

X_seq_new = np.array(X_seq_new)
print("Shape of X_seq_new:", X_seq_new.shape)

# -- Assuming 'arrival_time' is the column in the 'test' DataFrame representing the time steps --
timestamps = test['arrival_time'].iloc[seq_length - 1:]

# -- Make predictions --
predicted_congestion = model.predict(X_seq_new)
print(predicted_congestion[:15])
# predict = predicted_congestion[:15]
location = test[["stop_lat", "stop_lon", "next_lat", "next_lon", "arrival_hour", "arrival_minute"]][:15]

print(location)
# -- Plot the predicted and actual / previous congestion levels --
plt.figure(figsize=(12, 6))
plt.plot(test['congestion_level'][:15], label="Actual / Previous Congestion")
plt.plot(predicted_congestion[:15], label="Predicted Congestion")
plt.legend()
plt.xlabel("Time Steps - Location")
plt.ylabel("Congestion Level")
plt.title("Actual/Previous vs. Predicted Congestion Levels")
plt.show()