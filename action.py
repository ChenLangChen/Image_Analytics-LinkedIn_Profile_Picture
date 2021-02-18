# This is for combining the features I created. (Updated version of quick_start.py)
import sys
sys.path.append('scrape')
from scrape_linkedIn import *

# Unimport a module
#sys.modules.pop('blur_and_teeth')

import sys
sys.path.append('/')
from functions import *
from blur_and_teeth import *


# Given the LinedIn profile url, retrieve the img url
def save_img(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img_file_path = 'Saved_images/profile_pic.jpg'
    img.save(img_file_path)


# Creating functions to process a profile url
def process_profileURL(sample_url):
    returned_info = dict()
    # If the profile picture is empty, then catch the Exception
    try:
        img_url = get_img_url(driver, sample_url)
    except:
        print("Oops! No profile picture...")
        return returned_info

    # Save the img for later process in blur
    save_img(img_url)

    # Return the detected face
    detected_faces = get_faceDict(img_url)

    try:
        assert(len(detected_faces)>0)
    except:
        print('Oops...No face detected from image!')
        return returned_info

    # Assume that there's only one face detected in a linkIn profile
    face_dict = detected_faces[0]

    # Load the img from local disk
    img_path = "Saved_images/profile_pic.jpg"
    img = load_img(img_path)

    # Teeth detection
    teeth = detect_teeth(face_detector, img, landmark_detector)
    returned_info['teeth'] = teeth
    print('Teeth detected: ', teeth)

    # Face big enough?
    face_big = face_big_enough(face_detector, img, landmark_detector)
    returned_info['face_big'] = face_big
    print("Face big enough? ", face_big)

    # Detect emotion
    my_emotion = process_emotions(face_dict)
    returned_info['emotion'] = my_emotion
    print("Emotion: ", my_emotion)

    # Blur the background from the face
    blur_it(img, 8, face_detector, landmark_detector)
    return returned_info

# Set up the driver and login
DRIVER_PATH = '/Users/chenlang/Documents/ChromeDriver/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
sign_in(driver)

################ Change the sample_url here
no_teeth = 'https://www.linkedin.com/in/alexcsmith/'
teeth = "https://www.linkedin.com/in/linda-jia-3062324a/"
mustache = 'https://www.linkedin.com/in/scott-davidsen-619852168/'
neutral ='https://www.linkedin.com/in/trista-xun-wang/'
no_photo = 'https://www.linkedin.com/in/aaron-smith-ba251b3/'
sample_url ="https://www.linkedin.com/in/ryan-rogers-b7a14b203/"

pic_info = process_profileURL(sample_url)


















#
