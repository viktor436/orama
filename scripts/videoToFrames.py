import cv2
import os

video_file_path = 'C:/Users/vikto/Desktop/vid4.mp4'
output_dir = 'C:/Users/vikto/Desktop/screenShot4'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

video = cv2.VideoCapture(video_file_path)

fps = video.get(cv2.CAP_PROP_FPS)

frame_interval = int(fps * 2)

frame_count = 217
extracted_frame_count = 217

while video.isOpened():
    ret, frame = video.read()
    
    if not ret:
        break
    
    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_dir, f'frame_{extracted_frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        extracted_frame_count += 1
    
    frame_count += 1

video.release()

output_dir
