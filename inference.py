import queue
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
video_file = "./vid-test-2.mp4"
cap = cv2.VideoCapture(video_file)

frame_count = 0
frame_interval = 200  # Show every 120th frame
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps: ", fps)
frame_interval = 200  # Process every 120th frame

# Directory to store images
output_dir = "./images/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def get_prediction(url):
    result_queue = queue.Queue()  # Create a queue to store the result

    def pred(url):
        from openai import OpenAI

        client = OpenAI()
        prompt = "Role: You are a helpfull guide for blind person. You identify potential hazards and guide the blind person around them or inform him. You are his eyes, cause he can't see. Data: You receive an image. The image shows the direction the blind person walks. Task: Guide the blind person in the safest way during his walk. Tell me where should I go along the road. You should find, identify and inform about hazards like: potholes, poles, bins, roads, crossings, pedestrian traffic lights and its colors, any obstacles on the sidewalk and so on. You should aim to keep the person on the side walk, guide him around obstacles and dangers. Don't forget that the person can't see anything and where it is on the sidewalk. Answer with 1 sentences max."
        completion = client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:personal:orama:AFAUMDfh",
            temperature=0.01,
            messages=[
                {
                    "role": "system",
                    "content": "You are an helpful assistant that helps blind people.",
                },
                {"role": "user", "content": prompt},
                {
                    "role": "user",
                    "content": [{"type": "image_url", "image_url": {"url": url}}],
                },
            ],
        )
        result_queue.put(completion.choices[0].message)

        # return completion.choices[0].message

    thread = threading.Thread(target=pred, args=(url,))
    thread.start()

    # Retrieve the result from the queue
    result = result_queue.get()
    print("result: ", result)
    return result


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
# ngrok_response = start_ngrok()
# print(f"Ngrok tunnel established: {ngrok_response}")


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
        url = f"https://tkv0kr26-8000.euw.devtunnels.ms/frame/{frame_count}"
        print("url: ", url)
        res = get_prediction(url)
        print(res.content)
        # Save the image locally
        # image_filename = f"frame_{frame_count}.jpg"
        # image_path = f"{image_filename}"
        # image.save(image_path)

        # image.show()  # This will open the frame as an image on Mac

        speak_in_background(res.content, speech_config, audio_config)

    cv2.imshow("Video", frame)
    if cv2.waitKey(frame_delay) & 0xFF == ord("q"):
        break
    # Increment frame count
    frame_count += 1

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
