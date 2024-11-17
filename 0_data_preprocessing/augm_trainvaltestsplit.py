import os
from PIL import Image
import random

# folder where the images should be saved
folder = r""

# create a function that rotates every image 90° to the right, 90° to the left and then stores the original image and the other two images in the folder
def rotate_images(folder, save_folder):
    # iterate over all images in the folder
    for filename in os.listdir(folder):
        # open the image
        img = Image.open(os.path.join(folder, filename))
        # rotate the image 90° to the right
        img_right = img.rotate(-90)
        # rotate the image 90° to the left
        img_left = img.rotate(90)
        # save the original image
        img.save(os.path.join(save_folder, filename))
        # save the image rotated 90° to the right
        img_right.save(os.path.join(save_folder, filename[:-4] + "_right.png"))
        # save the image rotated 90° to the left
        img_left.save(os.path.join(save_folder, filename[:-4] + "_left.png"))


constr_folder = r""
no_constr_folder = r""

rotate_images(constr_folder, f"{folder}/test_constr")
rotate_images(no_constr_folder, f"{folder}/test_no_constr")

# Write a function that moves a certain share of images from one folder to another
def move_images(folder, save_folder, share):
    # iterate over all images in the folder
    for filename in os.listdir(folder):
        # move the image with the given share
        if random.random() < share:
            # Create random number from 1 to 100 and add it to the filename
            random_number = random.randint(1, 100)
            filename_rand = f"{random_number}_{filename}"
            os.rename(os.path.join(folder, filename), os.path.join(save_folder, filename_rand))

move_images(f"{folder}/test_constr", f"{folder}/data/train/constr", 0.6)
move_images(f"{folder}/test_constr", f"{folder}/data/val/constr", 0.75)

move_images(f"{folder}/test_no_constr", f"{folder}/data/train/no_constr", 0.6)
move_images(f"{folder}/test_no_constr", f"{folder}/data/val/no_constr", 0.75)
