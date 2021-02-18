# This is for deciding the mar index in teeth detection.

from scipy.spatial import distance as dist
import pandas as pd
# Create a dataframe
column_names = ['img_name', 'smile', 'under lip thickness', 'lips distance']
df = pd.DataFrame(columns = column_names)

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
    lips_dots_indexes = [48, 54, 61, 67, 62, 66, 63, 65]
    for i in lips_dots_indexes:
        cv2.circle(img, landmark_tuple[i], 1, (0, 0, 0), -1)
    plt.imshow(img)
    #######
    return MAR

# Create a function to loop through the whole folder and return a list of MAR
import os
import re
# Sort the file_names in the folder
def sort_fimenames(dir_name):
    fn_list = os.listdir(dir_name)
    fn_list.sort(key=lambda f: int(re.sub('\D', '', f)))

    sorted_list=[]
    for item in fn_list:
        new_name = dir_name+item
        sorted_list.append(new_name)
    return sorted_list

sorted_names = sort_fimenames('face_images/')

def get_mars(img_names):
    MARS = []
    for item in img_names:
        print('Processing index: ' + str(img_names.index(item)))
        print(item)
        img = load_img(item)
        mar = smile_MAR (face_detector, img, landmark_detector)
        MARS.append(mar)
    return MARS

mars = get_mars(sorted_names)

df = pd.read_csv("./img_info.csv")
df['mar'] = mars

teeth_df = df[df['teeth']==1]
no_teeth_df = df[df['teeth']==0]

teeth_anomaly = teeth_df[teeth_df['mar']<=0.09]
teeth_anomaly
no_teeth_anomaly = no_teeth_df[no_teeth_df['mar']>0.09]
no_teeth_anomaly
# Threshhold: 0.09
# Saving the dataframe
df.to_csv(r'img_info.csv', index = False)

######## Debug
img_path = "face_images/271.jpg"
img = load_img(img_path)
smile_MAR (face_detector, img, landmark_detector)

def detect_teeth(face_detector, img, landmark_detector):
    # If mar >= 0.09, teeth detected
    my_mar = smile_MAR (face_detector, img, landmark_detector)
    return my_mar >= 0.09
