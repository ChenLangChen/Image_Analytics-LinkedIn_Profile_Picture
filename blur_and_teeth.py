
################For Blurring the background
# Dlib: facial feature detection & tracking 💦✨☄️🌪
# Step A: Detect facial landmarks with Dlib
# Step B: Calculate Convex Hull with OpenCV's convexHull function, the convexHull gives landmarks ranging from forehead to chin.
# How to install Dlib: https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/
# Reference: https://sefiks.com/2020/11/20/facial-landmarks-for-face-recognition-with-dlib/
# Reference: https://github.com/codeniko/shape_predictor_81_face_landmarks

import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt

import requests
from io import BytesIO
from PIL import Image

from scipy.spatial import distance as dist
from math import pi

face_detector = dlib.get_frontal_face_detector()
landmark_detector = dlib.shape_predictor("shape_predictor_81_face_landmarks.dat") # With shape_predictor_81_face_landmarks.dat, it also tracks forehead landmarks

def load_img(img_path):
    img = dlib.load_rgb_image(img_path)
    return img

def get_face_landmarks(landmark_detector, faces, img):
    # Assume that the linkedIn profile has only one face
    landmark_tuple = []
    landmarks = landmark_detector(img, faces[0])
    for n in range(0, 81):
       x = landmarks.part(n).x
       y = landmarks.part(n).y
       landmark_tuple.append((x, y))
       #cv2.circle(img, (x, y), 1, (255, 255, 0), -1)
    return landmark_tuple


def get_boundary_dots(landmark_tuple):
    # Function to return an array including all boundary dots
    jawline_landmarks = landmark_tuple[0:17]

    sorted_landmarks = []
    # Appending the jawline landmarks
    for i in jawline_landmarks:
        sorted_landmarks.append(i)
    # Appending the forehead landmarks
    forehead_indexes = [78,74,79,73,72,80,71,70,69,68,76,75,77]
    for n in forehead_indexes:
        sorted_landmarks.append(landmark_tuple[n])

    return sorted_landmarks


def get_mask(img, routes):
    mask = np.zeros((img.shape[0], img.shape[1]))
    mask = cv2.fillConvexPoly(mask, np.array(routes), 1)
    mask = mask.astype(np.bool)
    return mask

def blur_img(img, factor = 20):
   kW = int(img.shape[1] / factor)
   kH = int(img.shape[0] / factor)
   # Instead of a box filter, a Gaussian kernel is used. Good for reducing image noise.
   # Ensure the shape of the kernel is odd
   if kW % 2 == 0: kW = kW - 1
   if kH % 2 == 0: kH = kH - 1

   blurred_img = cv2.GaussianBlur(img, (kW, kH), 0)
   return blurred_img


def blur_background(img, blur_factor, mask):
    blurred_img = blur_img(img, factor = blur_factor)
    blurred_img[mask] = img[mask]
    plt.imshow(blurred_img)


def blur_it(img, blur_factor, face_detector, landmark_detector):
    faces = face_detector(img, 1)
    landmark_tuple = get_face_landmarks(landmark_detector, faces, img)
    sorted_landmarks = get_boundary_dots(landmark_tuple)
    mask = get_mask(img, sorted_landmarks)
    blur_background(img, blur_factor, mask)


def face_big_enough(face_detector, img, landmark_detector):
    faces = face_detector(img, 1)
    landmark_tuple = get_face_landmarks(landmark_detector, faces, img)
    sorted_landmarks = get_boundary_dots(landmark_tuple)
    # Calculating the area of the contour
    contour_area = cv2.contourArea(np.array(sorted_landmarks))
    # Calculating the area of the whole image, usually on a LinedIn profile, the picture is cropped into a circle, so we calculate the area of the cropped picture.
    circle_r = min([img.shape[0], img.shape[1]])/2
    img_area = pi * circle_r * circle_r

    face_percent = contour_area/img_area
    face_percent_str = str(face_percent*100)+'%'
    return [face_percent_str, face_percent >= 0.5]


################################### For teeth detection
def smile_MAR (face_detector, img, landmark_detector):
    faces = face_detector(img, 1)
    landmark_tuple = get_face_landmarks(landmark_detector, faces, img)
    len(landmark_tuple)
    smile_width = dist.euclidean(landmark_tuple[48], landmark_tuple[54])

    smile_height = (dist.euclidean(landmark_tuple[61], landmark_tuple[67]) +
                   dist.euclidean(landmark_tuple[62], landmark_tuple[66]) +
                   dist.euclidean(landmark_tuple[63], landmark_tuple[65]))/3

    MAR = smile_height/smile_width
    # For debugging
    # lips_dots_indexes = [48, 54, 61, 67, 62, 66, 63, 65]
    # for i in lips_dots_indexes:
    #     cv2.circle(img, landmark_tuple[i], 1, (0, 100, 0), -1)
    plt.imshow(img)
    return MAR

def detect_teeth(face_detector, img, landmark_detector):
    # If mar >= 0.09, teeth detected
    my_mar = smile_MAR (face_detector, img, landmark_detector)
    return my_mar >= 0.09






###########
