import hashlib

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)  # Read in 64k chunks
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()

# Usage
file_path = "D:\PycharmProjects\BusCongestionPrediction\model\LSTM_1_model_saved_model\keras_metadata.pb"
calculated_hash = calculate_sha256(file_path)
print("SHA-256 hash:", calculated_hash)
