import sys

def main(file_path):
    print(f"Processing file: {file_path}")
    print("Dummy processing complete.")
    print("Detected Rhythm Pattern: 4/4")
    print("Output Image Path: music/static/dummy_spectrogram.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 simple_test.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)
