# script_path = "music/detect_rhythm.py"
# log_file_path = "music/detect_rhythm_log.txt"
# command = ["python3", script_path, file_path]

# from django.shortcuts import render
# from django.core.files.storage import default_storage
# import os
# import subprocess


# def detect_rhythm(file_path):
#     script_path = "music/detect_rhythm.py"
#     log_file_path = "music/detect_rhythm_log.txt"
#     command = ["python3", script_path, file_path]

#     print(f"Running command: {command}")

#     with open(log_file_path, "w") as log_file:
#         log_file.write(f"Running command: {command}\n")
#         result = subprocess.run(
#             command, stdout=log_file, stderr=log_file, text=True, shell=False
#         )
#         log_file.write(f"Subprocess stdout:\n{result.stdout}\n")
#         log_file.write(f"Subprocess stderr:\n{result.stderr}\n")

#     with open(log_file_path, "r") as log_file:
#         output = log_file.read()

#     print("Subprocess output:")
#     print(output)

#     lines = output.splitlines()

#     print(f"Output lines: {lines}")

#     if lines:
#         for line in lines:
#             print(f"Output line: {line}")
#         if "Detected Rhythm Pattern:" in lines[-1]:
#             rhythm_label = lines[-1].split(": ")[-1]
#             image_path = lines[-2].split(" at: ")[-1]
#         else:
#             rhythm_label = "Error: No valid output from subprocess"
#             image_path = None
#     else:
#         rhythm_label = "Error: No output from subprocess"
#         image_path = None

#     print(f"rhythm_label: {rhythm_label}, image_path: {image_path}")

#     return rhythm_label, image_path


# def home(request):
#     return render(request, "music/home.html")


# def upload(request):
#     if request.method == "POST" and request.FILES["file"]:
#         file = request.FILES["file"]
#         file_path = default_storage.save("tmp/" + file.name, file)

#         file_path = os.path.join("tmp", file.name)  # Update path to tmp folder

#         print(f"File saved at: {file_path}")

#         rhythm_label, output_image_path = detect_rhythm(file_path)

#         return render(
#             request,
#             "music/result.html",
#             {
#                 "spectrogram": output_image_path,
#                 "prediction": f"Detected Rhythm Pattern: {rhythm_label}",
#             },
#         )
#     return render(request, "music/upload.html")


from django.shortcuts import render
from django.core.files.storage import default_storage
import os
import subprocess

def home(request):
    return render(request, 'music/home.html')

def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_path = default_storage.save('tmp/' + file.name, file)
        file_path = os.path.join('tmp', file.name)  # Update path to tmp folder

        print(f"File saved at: {file_path}")

        # Jalankan subprocess
        command = ['python3', 'music/detect_rhythm.py', file_path]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        # Log output subprocess
        print("Subprocess command:", command)
        print("Subprocess return code:", result.returncode)
        print("Subprocess stdout:", result.stdout)
        print("Subprocess stderr:", result.stderr)

        if result.returncode == 0:
            try:
                output_lines = result.stdout.splitlines()
                rhythm_label = None
                output_image_path = None
                for line in output_lines:
                    print(f"Processing line: {line}")
                    if line.startswith("Detected Rhythm Pattern:"):
                        rhythm_label = line.split(": ")[1]
                    elif line.startswith("Output Image Path:"):
                        output_image_path = line.split(": ")[1]
                if rhythm_label and output_image_path:
                    return render(request, 'music/result.html', {
                        'spectrogram': output_image_path,
                        'prediction': f'Detected Rhythm Pattern: {rhythm_label}'
                    })
                else:
                    print("Error: rhythm_label or output_image_path is missing.")
            except Exception as e:
                print(f"Error processing subprocess output: {e}")
        else:
            print(f"Subprocess failed with return code {result.returncode}")

        return render(request, 'music/result.html', {
            'spectrogram': None,
            'prediction': 'Error: No valid output from subprocess'
        })
    return render(request, 'music/upload.html')
