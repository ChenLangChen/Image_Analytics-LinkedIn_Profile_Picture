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


#########################################
# # This section is fore testing the sentiment analysis from Azure API, below are image addresses
# disgust_img = 'https://www.whitman.edu/images/Newsroom/News/Magazine/2017/Summer/TOM_ARMSTRONG_DISGUST-400.jpg'
# anger_img = 'https://miro.medium.com/max/3840/1*cD8nIooIkIrLoHKBOGnj9A.jpeg'
# surprise_img = 'https://us.123rf.com/450wm/avemario/avemario1510/avemario151000125/46788327-surprise-astonished-beautiful-mixed-race-woman-closeup-portrait-woman-surprised-in-full-disbelief-op.jpg?ver=6'
# fear_img = 'https://www.practicalheartskills.com/wp-content/uploads/home-alone.jpg'
#
#
# import matplotlib.pyplot as plt
#
# def print_img (img_url):
#     response = requests.get(img_url)
#     img = Image.open(BytesIO(response.content))
#     plt.imshow(img)
#
# def sentiment_detection(img_url):
#     # Function to print the img and the detected sentiment
#     print_img (img_url)
#     face_dicts = get_faceDict(img_url)
#     my_emotion = process_emotions(face_dicts[0])
#     print('Emotion: ' + my_emotion)
#
# sentiment_detection(fear_img)
