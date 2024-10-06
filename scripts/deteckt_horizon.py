
#from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import cv2
from transformers import pipeline
from PIL import Image
import requests

# Load the depth image
# image_path = "/content/frame_0199.jpg"#'/content/frame_0232.jpg'  
# depth_image = io.imread(image_path)



# load pipe
pipe = pipeline(task="depth-estimation",
                model="depth-anything/Depth-Anything-V2-Base-hf",
                device = "cuda")

#depth_alk = pipe(image)["depth"]

def show_img(img):
  plt.imshow(img)
  plt.axis('off')
  plt.show()

def depth_image(path,pipe):
  image = Image.open(path)
  depth = pipe(image)["depth"]
  return depth

#depth_map = depth_image(input_path)

def get_image_with_average_depth(depth_image):
  avg_depth_per_row = np.mean(depth_image, axis=1)
  scaled_depth_image = np.uint8(255 * (avg_depth_per_row - avg_depth_per_row.min()) / (avg_depth_per_row.max() - avg_depth_per_row.min()))
  scaled_depth_image_full = np.tile(scaled_depth_image[:, np.newaxis], (1, depth_image.shape[1]))
  return scaled_depth_image_full  


def indentify_y(image):
  
  height, _ = image.shape

  y_coordinate = -1  

  for y in range(height-1, -1, -1):
      if np.mean(image[y, :]) == 0:
          y_coordinate = y
          break
  return y_coordinate

def vertical_buffer_average(image, buffer_height=10):

    depth_image = get_image_with_average_depth(image)
    #show_img(depth_image)

    height, _ = depth_image.shape
    averaged_image = np.zeros_like(depth_image)

    for i in range(0, height, buffer_height):
        buffer_end = min(i + buffer_height, height)
        buffer = depth_image[i:buffer_end, :]
        
        buffer_average = np.mean(buffer)
        #averaged_image[i:i+3, :]
        averaged_image[i:buffer_end, :] = buffer_average
    
    
    #show_img(averaged_image)
    
    averaged_image = averaged_image > 25 #hard coded
    #show_img(averaged_image)


    y = indentify_y(averaged_image)
    return y


def draw_line(path,pipe):
  d_image = depth_image(path,pipe)
  #show_img(d_image)
  img_array = np.array(d_image)
  
  y_coor = vertical_buffer_average(img_array, buffer_height=90)
  img = Image.open(path)
  print(y_coor)
  plt.imshow(img)
  # Draw the horizontal red line
  plt.axhline(y=y_coor, color='red', linestyle='--', linewidth=2)
  # Hide the axes and show the image with the red line
  plt.axis('off')
  plt.show()


if __name__ == "__main__":
    path = "/content/frame_0149.jpg"#"/content/frame_0044.jpg"
    scaled_depth_image_full = draw_line(path,pipe)
    # fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    # plt.title("1")

    # axes[0].imshow(depth_image, cmap='gray')
    # axes[0].set_title('2')
    # axes[0].axis('off')

    # axes[1].imshow(scaled_depth_image_full, cmap='gray')
    # axes[1].set_title('3')
    # axes[1].axis('off')
    # plt.show()
