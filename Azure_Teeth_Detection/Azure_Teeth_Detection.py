# This is for storing image info to create a predictive model for teeth detection
import random
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

import sys
sys.path.append('scrape')
from scrape_linkedIn import *

import sys
sys.path.append('/')
from functions import *

# Unimport a module
# sys.modules.pop('scrape_linkedIn')
# sys.modules.pop('functions')

sample_url = "https://www.linkedin.com/in/megan-smith-11704435/"
# Set up the driver
DRIVER_PATH = '/Users/chenlang/Documents/ChromeDriver/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

sign_in(driver)
get_img_url(driver, sample_url)

# Now I need to collect a bunch of img urls, so that I can process them later.
profile_urls = [] # Collect it manually

def extract_img_urls (profile_urls):
    img_urls = []
    for profile_url in profile_urls:
        time.sleep(random.randint(1, 8))
        img_url = get_img_url(profile_url)
        img_urls.append(img_url)
    return img_urls
#################################################
# Already had all of the imgs urls needed

# Create a dataframe
column_names = ['img_name', 'smile', 'under lip thickness', 'lips distance']
df = pd.DataFrame(columns = column_names)

def store_img_info(face_dict, img_name):
    # Store img info for teeth detection processing into CSV table
    # Info: smile index, under lip thickness, lips distance
    smile_index = smile(face_dict)
    under_lip_thickness = face_dict.face_landmarks.under_lip_bottom.y - face_dict.face_landmarks.under_lip_top.y
    lips_distance = lip_distance(face_dict)
    # Adding the new row into the dataframe, (0 is teeth )
    row = [img_name, smile_index, under_lip_thickness, lips_distance, 0]
    df.loc[len(df)] = row

def save_img (img_url):
    # Saving and naming a file in ascending order
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    image_path = 'face_images'
    image_list = os.listdir(image_path)
    count = len(image_list)
    img_name = str(count+1) + '.jpg'
    img.save(image_path + '/' + img_name)

    # Saving img info needed for teeth detection in dataframe
    face_dict = get_faceDict(img_url)[0]
    store_img_info(face_dict, img_name)

# Now I need to test save_img(img_url), shows up in face_images, and df 
sample_img_url = 'https://media-exp1.licdn.com/dms/image/C5603AQHHUuOSlRVA1w/profile-displayphoto-shrink_400_400/0/1579726624860?e=1616630400&v=beta&t=C0R4i3eK3kckjMrg9LkpmHQJrtpMSsGFAXOtLWNiTew'
save_img(sample_img_url)

# Ready to process all of the img_urls, after that I need to create the model with Notebook. 
import sys
sys.path.append('/')
from img_urls import *

# Unimport a module
#sys.modules.pop('img_urls')

for img_url in urls_google[57:]:
    # The limit is 20calls/min
    time.sleep(4)
    print(urls_google.index(img_url))
    save_img(img_url)

# Saving the dataframe as csv file
df.to_csv(r'img_info.csv', index = False)
# Loading the csv file
df = pd.read_csv("./img_info.csv")

#####################################
# Loading the pre-made model
# import pickle
# filename = 'saved_model.sav'
# loaded_model = pickle.load(open(filename, 'rb'))

def predict_teeth(my_model, smile, percent):
  # Given 'smile' and 'percent', predict whether teeth is detected.
  my_array = [[smile, percent]]
  result = my_model.predict(my_array)
  return result[0]

# For final use
def detect_teeth(face_dict, my_model):
    # Teeth detection 0:No 1:Yes
    under_lip_thickness = face_dict.face_landmarks.under_lip_bottom.y - face_dict.face_landmarks.under_lip_top.y
    lips_distance = lip_distance(face_dict)
    percent = lips_distance/under_lip_thickness

    smile_index = smile(face_dict)

    return predict_teeth(my_model, smile_index, percent)

#########################################################

# This is for using the loaded teeth detection model
import sys
sys.path.append('/')
from functions import *

def predict_teeth(my_model, smile, percent):
  # Given 'smile' and 'percent', predict whether teeth is detected.
  my_array = [[smile, percent]]
  result = my_model.predict(my_array)
  return result[0]

# For final use
def detect_teeth(face_dict, my_model):
    # Teeth detection 0:No 1:Yes
    under_lip_thickness = face_dict.face_landmarks.under_lip_bottom.y - face_dict.face_landmarks.under_lip_top.y
    lips_distance = lip_distance(face_dict)
    percent = lips_distance/under_lip_thickness

    smile_index = smile(face_dict)

    return predict_teeth(my_model, smile_index, percent)
