import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf
import matplotlib.pyplot as plt

# Load your test data
# Replace 'test.csv' with the actual filename or data source.
test_file_path = os.path.join("../dataset", "test.csv")
test_data = pd.read_csv(test_file_path)

# Load the saved model
loaded_model = tf.keras.models.load_model('congestion_model.h5')



# Prepare the test data
X_test = test_data[['start_stop_id', 'end_stop_id', 'hour', 'minute']]

# Make predictions using the loaded model
predictions = loaded_model.predict(X_test)

# Print out the predictions
print(predictions)


actual_congestion = test_data['segment_congestion_level']
print(actual_congestion.values)
# Create a plot to compare actual vs. predicted congestion levels
plt.figure(figsize=(10, 6))
plt.plot(actual_congestion, label='Actual Congestion', marker='o')
plt.plot(predictions, label='Predicted Congestion', marker='x')
plt.xlabel('Data Point')
plt.ylabel('Congestion Level')
plt.legend()
plt.title('Actual vs. Predicted Congestion Levels')
plt.show()
