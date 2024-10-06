import cv2
from PIL import Image
import os
from flask import Flask, send_file
import threading
import time

app = Flask(__name__)

# Directory to store frames
FRAME_DIR = "frames"
if not os.path.exists(FRAME_DIR):
    os.makedirs(FRAME_DIR)

# Global variable to store the latest frame filename
latest_frame = None


def process_video():
    global latest_frame
    cap = cv2.VideoCapture("./vid-test-2.mp4")  # Replace with your video file
    frame_count = 0
    frame_interval = 200  # Process every 120th frame

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image_filename = f"frame_{frame_count}.jpg"
            image_path = os.path.join(FRAME_DIR, image_filename)
            image.save(image_path)
            latest_frame = image_filename

        frame_count += 1

    cap.release()


@app.route("/latest_frame")
def get_latest_frame():
    if latest_frame:
        return send_file(os.path.join(FRAME_DIR, latest_frame), mimetype="image/jpeg")
    else:
        return "No frame available", 404


@app.route("/frame/<int:frame_number>")
def get_frame(frame_number):
    frame_filename = f"frame_{frame_number}.jpg"
    frame_path = os.path.join(FRAME_DIR, frame_filename)
    if os.path.exists(frame_path):
        return send_file(frame_path, mimetype="image/jpeg")
    else:
        return "Frame not found", 404


if __name__ == "__main__":
    # Start video processing in a separate thread
    video_thread = threading.Thread(target=process_video)
    video_thread.start()

    # Start the Flask server
    app.run(host="0.0.0.0", port=8000)
