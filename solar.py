import numpy as np
from PIL import Image


def shadows_with_threshold(image_array, threshold):
    mask = image_array < threshold
    inverted_array = np.where(mask, 255 - image_array, image_array)
    return inverted_array


def highlights_with_threshold(image_array, threshold):
    mask = image_array > threshold
    inverted_array = np.where(mask, 255 - image_array, image_array)
    return inverted_array


def solarize(image, thresholds):
    """
    Returns: A PIL image representing the new solarized image.
    """
    image1 = Image.open(image)
    image1 = np.asarray(image1)

    if thresholds[2] != 0 or thresholds[3] != 255 or thresholds[4] != 0 or thresholds[5] != 255 or thresholds[6]!= 0 or thresholds[7] != 255:
        if image1.ndim == 3 and image1.shape[2] == 3:
            new_image = np.zeros_like(image1)
            source_img = image1
        else:
            # if image1 has a single channel, but we still want color effects on it
            height, width = image1.shape[:2]
            source_img = np.zeros((height, width, 3))
            source_img[..., 0] = image1  # Red channel from image 1
            source_img[..., 1] = image1  # Green channel from image 1
            source_img[..., 2] = image1  # Blue channel from image 1
    else:
        source_img = image1

    if thresholds[0] > 0:
        new_image = shadows_with_threshold(image_array=source_img, threshold=thresholds[0])

    if thresholds[1] < 255:
        new_image = highlights_with_threshold(image_array=source_img, threshold=thresholds[1])

    if thresholds[2] > 0:
        new_image[..., 0] = shadows_with_threshold(image_array=source_img[..., 0], threshold=thresholds[2])

    if thresholds[3] < 255:
        new_image[..., 0] = highlights_with_threshold(image_array=source_img[..., 0], threshold=thresholds[3])

    if thresholds[4] > 0:
        new_image[..., 1] = shadows_with_threshold(image_array=source_img[..., 1], threshold=thresholds[4])

    if thresholds[5] < 255:
        new_image[..., 1] = highlights_with_threshold(image_array=source_img[..., 1], threshold=thresholds[5])

    if thresholds[6] > 0:
        new_image[..., 2] = shadows_with_threshold(image_array=source_img[..., 2], threshold=thresholds[6])

    if thresholds[7] < 255:
        new_image[..., 2] = highlights_with_threshold(image_array=source_img[..., 2], threshold=thresholds[7])

    out = Image.fromarray(new_image)  # Convert NumPy array to PIL image
    return out
