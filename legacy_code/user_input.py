import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf

# Load the saved model
loaded_model = tf.keras.models.load_model('congestion_model.h5')

# Create a label encoder for categorical features
label_encoder = LabelEncoder()

# Load your dataset (assuming you have already loaded it as a DataFrame)
FILE_PATH = os.path.join("../dataset", "data_with_segment_congestion_level.csv")
df = pd.read_csv(FILE_PATH)

# Fit the label encoder with the data
label_encoder.fit(df['trip_id'])  # Replace 'df' with your actual DataFrame

# Define a function to preprocess user input and make predictions
def predict_congestion():
    # Get user input for the compulsory features
    route_id = input("Enter Route ID (compulsory): ")
    direction_id = input("Enter Direction ID (compulsory): ")
    start_stop_id = input("Enter Start Stop ID (compulsory): ")
    arrival_time = input("Enter Arrival Time (HH:MM:SS, compulsory): ")

    # Check if compulsory fields are provided, exit if not
    if not route_id or not direction_id or not start_stop_id or not arrival_time:
        print("Route ID, Direction ID, Start Stop ID, and Arrival Time are compulsory.")
        return

    # Get user input for the optional features
    end_stop_id = input("Enter End Stop ID (optional, press Enter to skip): ")
    speed_m_s = input("Enter Speed (m/s) (optional, press Enter to skip): ")
    avg_route_speed_m_s = input("Enter Average Route Speed (m/s) (optional, press Enter to skip): ")
    segment_max_speed_m_s = input("Enter Segment Max Speed (m/s) (optional, press Enter to skip): ")
    trip_id = input("Enter Trip ID (optional, press Enter to skip): ")
    departure_time = input("Enter Departure Time (HH:MM:SS, optional, press Enter to skip): ")

    # Encode categorical features and parse timestamps if provided
    trip_id_encoded = label_encoder.transform([trip_id]) if trip_id in label_encoder.classes_ else [0]
    arrival_time_encoded = label_encoder.transform([arrival_time]) if arrival_time in label_encoder.classes_ else [0]
    departure_time_encoded = label_encoder.transform([departure_time]) if departure_time in label_encoder.classes_ else [0]

    # Normalize numerical features using StandardScaler
    input_features = [
        int(route_id), int(direction_id), int(start_stop_id),
        int(end_stop_id) if end_stop_id else 0,
        float(speed_m_s) if speed_m_s else 0.0,
        float(avg_route_speed_m_s) if avg_route_speed_m_s else 0.0,
        float(segment_max_speed_m_s) if segment_max_speed_m_s else 0.0,
        trip_id_encoded[0],
        arrival_time_encoded[0],
        departure_time_encoded[0]
    ]

    # Make predictions using the loaded model
    predictions = loaded_model.predict([input_features])

    # Print the predicted congestion level
    print(f"Predicted Congestion Level: {predictions[0][0]}")

if __name__ == "__main__":
    while True:
        predict_congestion()
        another_prediction = input("Do you want to make another prediction? (yes/no): ").lower()
        if another_prediction != "yes":
            break
