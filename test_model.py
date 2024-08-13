# test_model.py

import os
import numpy as np
import tensorflow as tf

# Tentukan path absolut ke file model
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "model", "cnn_rhythm_model.h5")

# Debugging: Cek path model
print("Model path:", model_path)

# Load the trained model once
try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")

    # Dummy input for model prediction
    dummy_input = np.random.rand(1, 128, 660, 1)
    prediction = model.predict(dummy_input)
    print("Prediction:", prediction)
except Exception as e:
    print("Error loading model or making prediction:", e)
