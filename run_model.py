import os
import pandas as pd
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras


def run_model(route_id, direction_id, future_time):
    # Load the pre-trained model
    model = keras.models.load_model(os.path.abspath(os.path.join("model", "LSTM_1_model_saved_model")))

    # Input dataset to model
    main_data = pd.read_csv(os.path.join("dataset", "pre_processed_data.csv"))
    filter_by_route = main_data['route_id'] == route_id
    filter_by_direction = main_data['direction_id'] == direction_id
    main_data = main_data[filter_by_direction & filter_by_route]
    main_data = main_data.sort_values(by=['trip_id','stop_sequence_x'])


    # Update the first row of 'arrival_time' with the provided future_time
    main_data.loc[main_data.index[0], 'arrival_time'] = pd.to_datetime(future_time)

    calculated_arrival_times = []

    for idx in range(len(main_data)):
        if idx < 1:
            # For the first row, we've already updated it, so use the provided future_time
            calculated_arrival_times.append(pd.to_datetime(future_time))
        else:
            # For subsequent rows, calculate the 'arrival_time' based on the two previous rows
            previous_arrival_time = calculated_arrival_times[idx - 1]
            previous_runtime = main_data['runtime_sec'].iloc[idx - 1]
            new_arrival_time = previous_arrival_time + pd.to_timedelta(previous_runtime, unit='s')
            calculated_arrival_times.append(new_arrival_time)

    # Update the 'arrival_time' column with the calculated values
    main_data['arrival_time'] = calculated_arrival_times

    # -- Create 'arrival_hour' and 'arrival_minute' --
    main_data['arrival_hour'] = main_data['arrival_time'].dt.hour
    main_data['arrival_minute'] = main_data['arrival_time'].dt.minute



    # Ensure the new data is preprocessed in the same way as the training data
    scaler = MinMaxScaler()
    X_new = main_data[['arrival_hour', 'arrival_minute', 'stop_lat', 'stop_lon', 'next_lat', 'next_lon', 'direction_id']]
    X_new = scaler.fit_transform(X_new)


    # Define the sequence length (seq_length) used during training
    seq_length = 64

    # Generate sequences from the new data
    X_seq_new = []
    num_objects = len(X_new)

    for i in range(num_objects):
        start = max(0, i - seq_length + 1)
        sequence = X_new[start:i + 1]
        X_seq_new.append(sequence)

    # Pad sequences to ensure consistent length
    X_seq_new = pad_sequences(X_seq_new, maxlen=seq_length, dtype='float32', padding='post', truncating='post')

    # Assuming 'arrival_time' is the column in the 'test' DataFrame representing the time steps
    timestamps = main_data['arrival_time'].iloc[seq_length - 1:num_objects]

    # Make predictions
    predicted_congestion = model.predict(X_seq_new)

    main_data["congestion_level"] = predicted_congestion

    return main_data[['arrival_hour', 'arrival_minute', 'stop_lat', 'stop_lon', 'next_lat', 'next_lon', 'direction_id', 'congestion_level']]


# run_model(300025, 0, "2023-10-25 23:50:00")
