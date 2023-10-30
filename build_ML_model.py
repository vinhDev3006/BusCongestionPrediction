"""
    BUILD MACHINE LEARNING MODEL (LSTM)
"""
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

# -- Load file --
FILE_PATH = os.path.join("dataset", "pre_processed_data.csv")
df = pd.read_csv(FILE_PATH)

# -- sort by arrival_time for the ML LSTM model --
df['arrival_time'] = pd.to_datetime(df['arrival_time'])
df = df.sort_values(by=['arrival_time'])

# -- Select features and target --
X = df[
    ['arrival_hour', 'arrival_minute', 'stop_lat', 'stop_lon', 'next_lat', 'next_lon', 'direction_id']]
Y = df['congestion_level']

# -- Normalize feature data --
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# -- Define the sequence length --
seq_length = 320

X_seq, Y_seq = [], []

# -- Generate sequences --
for i in range(len(X) - seq_length):
    X_seq.append(X[i:i + seq_length])
    Y_seq.append(Y[i + seq_length])

X_seq = np.array(X_seq)
Y_seq = np.array(Y_seq)

# -- Split the data into training and testing sets --
X_train, X_test, Y_train, Y_test = train_test_split(X_seq, Y_seq, test_size=0.4, random_state=42)

# -- Build Simple LSTM model (tanh vs relu) --
model = keras.Sequential([
    keras.layers.LSTM(50, activation='tanh', return_sequences=True, input_shape=(seq_length, X_seq.shape[2])),
    keras.layers.LSTM(50, activation='tanh', return_sequences=True),
    keras.layers.LSTM(50, activation='tanh'),
    keras.layers.Dense(1)
])

# -- Using 'adam' optimizer and 'mean_squared_error' --
model.compile(optimizer='adam', loss='mean_squared_error')

# -- Train the model, batch size = 64 is due to the times appearance of each bus trip is from 50 to 85 --
model.fit(X_train, Y_train, epochs=1000, batch_size=64)

# -- Evaluate the model on the test set --
Y_pred = model.predict(X_test)
Y_test_1d = Y_test.reshape(-1)  # Reshape to a 1D array
Y_pred_1d = Y_pred.reshape(-1)  # Reshape to a 1D array
mse = mean_squared_error(Y_test_1d, Y_pred_1d)
print(f"Mean Squared Error: {mse}")

# -- Save the trained model to a file --
model.save(os.path.join("model", "LSTM_1_model_saved_model"))

# -- Example for making predictions --
input_data = X_test[10:40]  # Adjust the slice as needed
predicted_congestion = model.predict(input_data)

print("Predicted Congestion Level:", predicted_congestion)

# -- Plot the predicted and actual congestion levels --
plt.figure(figsize=(24, 6))
plt.plot(Y_test[10:40], label="Actual Congestion")
plt.plot(predicted_congestion, label="Predicted Congestion")
plt.legend()
plt.xlabel("Time Steps")
plt.ylabel("Congestion Level")
plt.title("Actual vs. Predicted Congestion Levels")
plt.show()
