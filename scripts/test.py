from dotenv import load_dotenv
import cv2
from PIL import Image
import os
import subprocess
import time
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading

load_dotenv()

import os
import azure.cognitiveservices.speech as speechsdk

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION")
)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"
import threading


# Function to speak in a separate thread
def speak_in_background(text, speech_config, audio_config):
    def speak(text, speech_config, audio_config):
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if (
            speech_synthesis_result.reason
            == speechsdk.ResultReason.SynthesizingAudioCompleted
        ):
            print(f"Speech synthesized for text [{text}]")
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if (
                cancellation_details.reason == speechsdk.CancellationReason.Error
                and cancellation_details.error_details
            ):
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region values?")

    # Run speak() in a separate thread to avoid blocking video playback
    threading.Thread(target=speak, args=(text, speech_config, audio_config)).start()


import cv2
from PIL import Image
import numpy as np

# from google.colab.patches import cv2_imshow
from IPython.display import display

# Open the video file
video_file = "./vid_1.mp4"
cap = cv2.VideoCapture(video_file)

frame_count = 0
frame_interval = 120  # Show every 120th frame
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = 120  # Process every 120th frame
frame_count = 0


# Directory to store images
output_dir = "./images/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Function to start the local HTTP server
def start_http_server():
    os.chdir(output_dir)  # Change directory to the folder where images are stored
    handler = SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 8080), handler)
    print("Serving at port 8080")
    httpd.serve_forever()


# Function to start Ngrok and expose the server
def start_ngrok():
    print("Starting Ngrok...")
    # Start ngrok process to tunnel port 8080
    ngrok_process = subprocess.Popen(["ngrok", "http", "8080"], stdout=subprocess.PIPE)
    time.sleep(2)  # Give it a couple of seconds to initialize

    # Fetch the public URL
    ngrok_url = subprocess.check_output(
        ["curl", "-s", "http://localhost:4040/api/tunnels"]
    )
    return ngrok_url.decode()


# Start the HTTP server in a new thread
server_thread = threading.Thread(target=start_http_server)
server_thread.daemon = True
server_thread.start()

# Start ngrok and expose the HTTP server
ngrok_response = start_ngrok()
print(f"Ngrok tunnel established: {ngrok_response}")


# # Directory to store images
# output_dir = './images/'
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# Calculate the wait time between frames in milliseconds
frame_delay = int(1000 / fps)
# Loop over the video frames
while cap.isOpened():
    ret, frame = cap.read()

    # Break the loop if there are no frames left
    if not ret:
        break

    # Process only every 120th frame
    if frame_count % frame_interval == 0:
        # Convert the frame (NumPy array) to a PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # Save the image locally
        image_filename = f"frame_{frame_count}.jpg"
        image_path = f"{image_filename}"
        image.save(image_path)

        # Generate the public URL for the image
        public_image_url = f"{ngrok_response}/images/{image_filename}"
        print(f"Public Image URL: {public_image_url}")
        # image.show()  # This will open the frame as an image on Mac

        speak_in_background("go straight ahead", speech_config, audio_config)

    cv2.imshow("Video", frame)
    if cv2.waitKey(frame_delay) & 0xFF == ord("q"):
        break
    # Increment frame count
    frame_count += 1

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
