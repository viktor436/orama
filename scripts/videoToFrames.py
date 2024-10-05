import cv2
import os

# Define the input video file path and output directory
video_file_path = 'C:/Users/vikto/Desktop/vid4.mp4'
output_dir = 'C:/Users/vikto/Desktop/screenShot4'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the video file using OpenCV
video = cv2.VideoCapture(video_file_path)

# Get the video's frame rate (fps)
fps = video.get(cv2.CAP_PROP_FPS)

# Calculate the interval between frames in terms of the video frame index (every 2 seconds)
frame_interval = int(fps * 2)

frame_count = 217
extracted_frame_count = 217

# Loop through the video and save every 2-second frame as an image
while video.isOpened():
    ret, frame = video.read()
    
    if not ret:
        break
    
    if frame_count % frame_interval == 0:
        # Save the current frame as an image file
        frame_filename = os.path.join(output_dir, f'frame_{extracted_frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        extracted_frame_count += 1
    
    frame_count += 1

# Release the video object
video.release()

# Return the path to the folder with the extracted frames
output_dir
