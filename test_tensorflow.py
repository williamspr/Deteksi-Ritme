import sys
from tensorflow.keras.models import load_model
import numpy as np


def main(file_path):
    print(f"Loading model from model/cnn_rhythm_model.h5")
    model = load_model("model/cnn_rhythm_model.h5")
    print("Model loaded successfully")

    # Buat input dummy untuk prediksi
    dummy_input = np.random.rand(1, 128, 660, 1)
    print("Running prediction on dummy input")
    prediction = model.predict(dummy_input)
    print(f"Prediction: {prediction}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_tensorflow.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)
