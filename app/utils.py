import cv2
import numpy as np
import pandas as pd
import sys
import scipy
from scipy.interpolate import UnivariateSpline

# Put the Following
# Warm
# Cold
# Invert
# Binary
# Blurred
# Grayscale
# Sepia
# Vignette
# Sketch
# Stylization
# Sharpen
# HDR


def get_filtered_image(image, action):
    def LookupTable(x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    
    
    filtered = None
    
    # COLD FILTER
    if action == 'COLD':
        # We are giving y values for a set of x values.
        # And calculating y for [0-255] x values accordingly to the given range.
        increase_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 75, 155, 255])(range(256))
    
        # Similarly construct a lookuptable for decreasing pixel values.
        decrease_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 45, 95, 255])(range(256))
        # Split the blue, green, and red channel of the image.
        blue_channel, green_channel, red_channel, alpha_channel = cv2.split(img)
        
        # Decrease red channel intensity using the constructed lookuptable.
        red_channel = cv2.LUT(red_channel, decrease_table).astype(np.uint8)
        
        # Increase blue channel intensity using the constructed lookuptable.
        blue_channel = cv2.LUT(blue_channel, increase_table).astype(np.uint8)
        
        # Merge the blue, green, and red channel. 
        filtered = cv2.merge((red_channel, green_channel, blue_channel, alpha_channel))
        
    
    # COLORIZED FILTER
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # WARM FILTER
    elif action == 'WARM':
        # We are giving y values for a set of x values.
        # And calculating y for [0-255] x values accordingly to the given range.
        increase_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 75, 155, 255])(range(256))
    
        # Similarly construct a lookuptable for decreasing pixel values.
        decrease_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 45, 95, 255])(range(256))
        # Split the blue, green, and red channel of the image.
        blue_channel, green_channel, red_channel, alpha_channel = cv2.split(img)
        
        # Increase red channel intensity using the constructed lookuptable.
        red_channel = cv2.LUT(red_channel, increase_table).astype(np.uint8)
        
        # Decrease blue channel intensity using the constructed lookuptable.
        blue_channel = cv2.LUT(blue_channel, decrease_table).astype(np.uint8)
        
        # Merge the blue, green, and red channel. 
        filtered = cv2.merge((red_channel, green_channel, blue_channel, alpha_channel))
        
    # BLURRED FILTER
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (50,50)
        
        elif width > 200 and width <= 500:
            k = (25,25)
            
        else:
            k = (10, 10)
            
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
        
    # BINARY FILTER
    elif action == 'BINARY':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
    # INVERT FILTER
    elif action == 'INVERT':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)

    # GRAYSCALE FILTER
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

    # SEPIA FILTER
    elif action == 'SEPIA':
        # Define the sepia transformation matrix
        sepia_matrix = np.array([[0.393, 0.769, 0.189],
                                [0.349, 0.686, 0.168],
                                [0.272, 0.534, 0.131]])

        # Split the RGBA channels
        red_channel, green_channel, blue_channel, alpha_channel = cv2.split(img)

        # Apply the sepia transformation to the RGB channels
        img_sepia = np.dot(img[..., :3], sepia_matrix.T)

        # Clip values to the range [0, 255]
        img_sepia = np.clip(img_sepia, 0, 255).astype(np.uint8)

        # Merge the sepia RGB channels with the original alpha channel
        filtered = cv2.merge((img_sepia[:, :, 0], img_sepia[:, :, 1], img_sepia[:, :, 2], alpha_channel))
        
    # VIGNETTE FILTER
    elif action == 'VIGNETTE':
        level = 2
        height, width = img.shape[:2]  
        
        # Generate vignette mask using Gaussian kernels.
        X_resultant_kernel = cv2.getGaussianKernel(width, width/level)
        Y_resultant_kernel = cv2.getGaussianKernel(height, height/level)
            
        # Generating resultant_kernel matrix.
        kernel = Y_resultant_kernel * X_resultant_kernel.T 
        mask = kernel / kernel.max()
        
        filtered = np.copy(img)
            
        # Applying the mask to each channel in the input image.
        for i in range(4):
            filtered[:,:,i] = filtered[:,:,i] * mask

    # Sketch
    elif action == 'SKETCH':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inverted_gray = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted_gray, (21, 21), 0)
        inverted_blurred = cv2.bitwise_not(blurred)
        filtered = cv2.divide(gray, inverted_blurred, scale=256.0)

    # Stylization
    elif action == 'STYLIZATION':
# Ensure the image is in the correct format (8-bit, 3-channel)
        if img.dtype != np.uint8:
            img = cv2.convertScaleAbs(img)

        # Convert to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Apply median blur
        gray = cv2.medianBlur(gray, 7)
        
        # Detect edges using adaptive threshold
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        
        # Apply bilateral filter to remove noise, use BGR format for bilateral filter
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        color = cv2.bilateralFilter(img_bgr, 9, 75, 75)
        
        # Combine edges and color
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        filtered = cv2.bitwise_and(color, edges)
        filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)  # Convert back to RGB for consistency

    # Sharpen
    elif action == 'SHARPEN':
        # Ensure image is in RGBA format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        # Define the sharpening kernel
        sharpening_kernel = np.array([[-1, -1, -1],
                                    [-1, 9, -1],
                                    [-1, -1, -1]])

        # Split the RGBA channels
        red_channel, green_channel, blue_channel, alpha_channel = cv2.split(img)

        # Apply the sharpening kernel to each RGB channel separately
        red_channel_sharpened = cv2.filter2D(red_channel, -1, sharpening_kernel)
        green_channel_sharpened = cv2.filter2D(green_channel, -1, sharpening_kernel)
        blue_channel_sharpened = cv2.filter2D(blue_channel, -1, sharpening_kernel)

        # Clip values to the range [0, 255]
        red_channel_sharpened = np.clip(red_channel_sharpened, 0, 255).astype(np.uint8)
        green_channel_sharpened = np.clip(green_channel_sharpened, 0, 255).astype(np.uint8)
        blue_channel_sharpened = np.clip(blue_channel_sharpened, 0, 255).astype(np.uint8)

        # Merge the sharpened RGB channels with the original alpha channel
        filtered = cv2.merge((red_channel_sharpened, green_channel_sharpened, blue_channel_sharpened, alpha_channel))

    # HDR
    elif action == 'HDR':
        # Using edgePreservingFilter for a more balanced HDR effect
        filtered = cv2.edgePreservingFilter(img, flags=1, sigma_s=64, sigma_r=0.25)

            
    return filtered