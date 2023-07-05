import cv2
import numpy as np
import math

def crop(image, top_ratio, bottom_ratio, left_ratio, right_ratio):
    h, w, _ = image.shape
    top_pixels = int(h * top_ratio)
    bottom_pixels = int(h * bottom_ratio)
    left_pixels = int(w * left_ratio)
    right_pixels = int(w * right_ratio)
    cropped_image = image[top_pixels:h-bottom_pixels, left_pixels:w-right_pixels]
    return cropped_image

def resize(image, width, height):
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def grayscale(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return grayscale_image

def apply_blur(image, kernel_size):
    blurred_image = cv2.blur(image, (kernel_size, kernel_size))
    return blurred_image

def add_noise(image, proportion):
    height, width = image.shape[:2]
    noisy_image = np.copy(image)

    # Calculate the number of pixels to be noised
    num_noisy_pixels = int(proportion * height * width)

    # Generate random coordinates for the noisy pixels
    pixel_indices = np.random.choice(range(height * width), num_noisy_pixels, replace=False)
    row_indices = pixel_indices // width
    col_indices = pixel_indices % width

    # Apply salt and pepper noise to the selected pixels
    noisy_image[row_indices, col_indices] = [0, 0, 0]  # Black noise (salt)
    noisy_image[row_indices, col_indices] = [255, 255, 255]  # White noise (pepper)

    return noisy_image


def apply_cutout(image, num_cutout, cutout_ratio):
    if len(image.shape) == 2:
        h, w = image.shape
    else:
        h, w, _ = image.shape
    
    h_size = int(h * cutout_ratio)
    w_size = int(w * cutout_ratio)
    
    masked_image = image.copy()
    
    for _ in range(num_cutout):
        x = np.random.randint(0, w - w_size)
        y = np.random.randint(0, h - h_size)
        
        masked_image[y:y+h_size, x:x+w_size] = 0
    
    return masked_image

def rotate_image(image, angle):
    rows, cols, _ = image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, M, (cols, rows))
    return rotated_image

def preprocess_image(image, pp_operations, width, height, top_ratio, bottom_ratio, left_ratio, right_ratio):
    # Effectuer ici les opérations de prétraitement souhaitées sur l'image
    pp_image = image.copy()
    for operation in pp_operations:
        if operation == 'crop':
            pp_image = crop(pp_image, top_ratio, bottom_ratio, left_ratio, right_ratio)
        elif operation == 'resize':
            pp_image = resize(pp_image, width, height)
        elif operation == 'grayscale':
            pp_image = grayscale(pp_image)
    
    return pp_image
