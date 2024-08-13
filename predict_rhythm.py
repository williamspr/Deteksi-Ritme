import os
import sys
import librosa
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import time


def detect_rhythm(file_path, model_path="model/cnn_rhythm_model.h5", max_length=660):
    log_file = open("music/detect_rhythm_log.txt", "a")
    try:
        log_file.write(f"Starting detection for {file_path}\n")
        log_file.flush()

        print(f"Loading model from {model_path}")
        log_file.write(f"Loading model from {model_path}\n")
        log_file.flush()
        model = load_model(model_path)
        print("Model loaded successfully")
        log_file.write("Model loaded successfully\n")
        log_file.flush()

        # Load audio file
        print(f"Loading audio file from {file_path}")
        log_file.write(f"Loading audio file from {file_path}\n")
        log_file.flush()
        y, sr = librosa.load(file_path, sr=None)
        print(f"Audio file loaded, sample rate: {sr}, length: {len(y)}")
        log_file.write(f"Audio file loaded, sample rate: {sr}, length: {len(y)}\n")
        log_file.flush()

        # Convert to spectrogram
        print(f"Converting to spectrogram")
        log_file.write(f"Converting to spectrogram\n")
        log_file.flush()
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_DB = librosa.power_to_db(spectrogram, ref=np.max)
        print(f"Spectrogram created, shape: {S_DB.shape}")
        log_file.write(f"Spectrogram created, shape: {S_DB.shape}\n")
        log_file.flush()

        # Ensure fixed length
        print(f"Ensuring fixed length")
        log_file.write(f"Ensuring fixed length\n")
        log_file.flush()
        if S_DB.shape[1] > max_length:
            S_DB = S_DB[:, :max_length]
        else:
            pad_width = max_length - S_DB.shape[1]
            S_DB = np.pad(S_DB, ((0, 0), (0, pad_width)), mode="constant")
        print(f"Spectrogram resized, new shape: {S_DB.shape}")
        log_file.write(f"Spectrogram resized, new shape: {S_DB.shape}\n")
        log_file.flush()

        # Preprocess spectrogram for prediction
        print(f"Preprocessing spectrogram for prediction")
        log_file.write(f"Preprocessing spectrogram for prediction\n")
        log_file.flush()
        S_DB = S_DB[np.newaxis, ..., np.newaxis]  # Add batch and channel dimensions
        print(f"Spectrogram preprocessed for prediction, shape: {S_DB.shape}")
        log_file.write(
            f"Spectrogram preprocessed for prediction, shape: {S_DB.shape}\n"
        )
        log_file.flush()

        # Predict the rhythm
        print(f"Predicting the rhythm")
        log_file.write(f"Predicting the rhythm\n")
        log_file.flush()
        prediction = model.predict(S_DB)
        rhythm_class = int(
            prediction[0][0] > 0.5
        )  # Adjust this based on your binary classification
        rhythm_label = "4/4" if rhythm_class == 0 else "3/4"
        print(
            f"Prediction made, rhythm class: {rhythm_class}, rhythm label: {rhythm_label}"
        )
        log_file.write(
            f"Prediction made, rhythm class: {rhythm_class}, rhythm label: {rhythm_label}\n"
        )
        log_file.flush()

        # Generate a unique filename for the output image
        timestamp = int(time.time())
        output_image = f"music/static/spectrogram_{timestamp}.png"

        # Plot the spectrogram
        print(f"Plotting the spectrogram")
        log_file.write(f"Plotting the spectrogram\n")
        log_file.flush()
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_DB[0, :, :, 0], sr=sr, x_axis="time", y_axis="mel")
        plt.colorbar(format="%+2.0f dB")
        plt.title("Mel-frequency spectrogram")
        plt.tight_layout()
        plt.savefig(output_image)
        plt.close()
        print(f"Spectrogram plot saved successfully at: {output_image}")
        log_file.write(f"Spectrogram plot saved successfully at: {output_image}\n")
        log_file.flush()

        log_file.write(
            f"Returning rhythm_label: {rhythm_label}, output_image: {output_image}\n"
        )
        log_file.close()

        return rhythm_label, output_image
    except Exception as e:
        log_file.write(f"Error: {e}\n")
        log_file.flush()
        log_file.close()
        print(f"Error: {e}")
        return "Error", None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_rhythm.py <file_path>")
    else:
        file_path = sys.argv[1]
        rhythm_label, output_image_path = detect_rhythm(file_path)
        print(f"Detected Rhythm Pattern: {rhythm_label}")
        print(f"Output Image Path: {output_image_path}")
