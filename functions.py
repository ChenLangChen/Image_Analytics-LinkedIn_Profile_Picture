# This is for creating accessory functions

########################################
# Return face dictionary
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw

import sys
sys.path.append('credentials/')
from key_endpoint import *


# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_faceDict(img_url):
    # Return a list of face dictionaries given an img url
    image_name = os.path.basename(img_url)
    # Face Attributes : age, gender, headPose, smile, facialHair, glasses and emotion
    detected_faces = face_client.face.detect_with_url(url=img_url, detection_model='detection_01',
                                                      return_face_attributes=['emotion', 'smile'], return_face_landmarks=True)
    return detected_faces

def lip_distance(faceDictionary):
    # Function to detect the distance between upper_lip_bottom and under_lip_top
    upper_lip_bottom_y = faceDictionary.face_landmarks.upper_lip_bottom.y
    under_lip_top_y = faceDictionary.face_landmarks.under_lip_top.y
    return under_lip_top_y - upper_lip_bottom_y

def smile (faceDictionary):
    # Function to retrieve the smile index
    return faceDictionary.face_attributes.smile


def max_key (Tv):
    # Return the key with max value within a dictionary
    Keymax = max(Tv, key=Tv.get)
    return(Keymax)

def process_emotions (face_dict):
    # Process the emotions,and pick the highest one
    emotions = face_dict.face_attributes.emotion
    # Construct a dict to store the emotions
    my_emotions = {}
    my_emotions['anger'] = emotions.anger
    my_emotions['contempt'] = emotions.contempt
    my_emotions['disgust'] = emotions.disgust
    my_emotions['fear'] = emotions.fear
    my_emotions['happiness'] = emotions.happiness
    my_emotions['neutral'] = emotions.neutral
    my_emotions['sadness'] = emotions.sadness
    my_emotions['surprise'] = emotions.surprise

    return max_key(my_emotions)




#
