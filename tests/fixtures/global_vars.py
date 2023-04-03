import os

USER_ID = 1
IMAGE_NAME = "my_image"
IMAGE_DIR = f"{USER_ID}/{IMAGE_NAME}"

USERNAME = "Tom"
ADMIN_USERNAME = "Admin"
PASSWORD = "abcd"

IMG_1_NAME = "img_1.jpeg"
IMG_2_NAME = "img_2.jpeg"
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
IMG_1_PATH = os.path.join(IMAGES_DIR, IMG_1_NAME)
IMG_2_PATH = os.path.join(IMAGES_DIR, IMG_2_NAME)
