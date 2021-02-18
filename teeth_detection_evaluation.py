# This is for independent evaluation of the teeth_detection using dlib & MAR index

import sys
sys.path.append('/')
from blur_and_teeth import *

import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import os

# Collecting headshots urls
headshots_urls= ['https://images.squarespace-cdn.com/content/v1/5563967ee4b022cec2233829/1585653953623-23F70SL73OWDX8TLUN36/ke17ZwdGBToddI8pDm48kFWxnDtCdRm2WA9rXcwtIYR7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UcTSrQkGwCGRqSxozz07hWZrYGYYH8sg4qn8Lpf9k1pYMHPsat2_S1jaQY3SwdyaXg/Impactful+LinkedIn+Headshots_Berkshire.jpg',
                 'https://monteluke.com.au/wp-content/gallery/linkedin-profile-pictures/2.jpg',
                 'https://static.wixstatic.com/media/efd486_1dddb0c6a1e547048ec7c5dcc3501019~mv2.jpg/v1/fill/w_422,h_434,al_c,q_80,usm_0.66_1.00_0.01/Self%20Branding%20Portrait.webp',
                 'https://www.studio-grey.net/wp-content/uploads/2018/10/Corporate_Headshot-2653.jpg',
                 'https://i.pinimg.com/originals/f3/c6/8e/f3c68ef3a73b98a0414dd9cbd8fa696e.jpg',
                 'https://static.wixstatic.com/media/efd486_67dd45f27f8347d1b828267a5f7e04f4~mv2.jpg/v1/fill/w_422,h_434,al_c,q_80,usm_0.66_1.00_0.01/LinkedIn%20headshot%20by%20Alise%20Black.webp',
                 'https://images.squarespace-cdn.com/content/v1/512ae5eae4b099777377a98e/1411534290314-0WITW8VU21FTV3UC537Y/ke17ZwdGBToddI8pDm48kB6N0s8PWtX2k_eW8krg04V7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1URWK2DJDpV27WG7FD5VZsfFVodF6E_6KI51EW1dNf095hdyjf10zfCEVHp52s13p8g/adam-a-headshot-session-2.jpg',
                 'https://heroshotphotography.com/wp-content/uploads/2018/06/marketing-headshots-wide-1-4-534x800.jpg',
                 'https://media-exp1.licdn.com/dms/image/C5612AQEaAzUt21YTvw/article-inline_image-shrink_1500_2232/0/1520171995310?e=1614816000&v=beta&t=WOpmd5LQcRvHPESJYOhcaoDf9oCqdv4IWjRL8Pat_IQ',
                 'https://images.squarespace-cdn.com/content/v1/5aee389b3c3a531e6245ae76/1530390614536-7ZY40ZDGMLK7OXRHVY36/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/Tokyo+-+Headshot+-+Photographer+Anthony+Wood+%285%29.jpg',
                 'https://heroshotphotography.com/wp-content/uploads/2019/08/Asian-Male-actor-headshot-sydney-mobile-800x800.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5c5a48b7809d8e364b16c2bf/1596588733636-BB2IQDZKRFWOG82LARQU/ke17ZwdGBToddI8pDm48kPJXHKy2-mnvrsdpGQjlhod7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmihaE5rlzFBImxTetd_yW5btdZx37rH5fuWDtePBPDaHF5LxdCVHkNEqSYPsUQCdT/unique+linkedin+headshots.jpg?format=500w',
                 'https://i.pinimg.com/236x/46/47/78/4647784cf4071b255427e4a6b1826560--the-edge-warm.jpg',
                 'https://headshotsadelaide.com/wp-content/uploads/2018/06/Headshots_Adelaide_Professional_Portrait_Photography_W1024__0009.jpg',
                 'https://www.corporatephotographerslondon.com/wp-content/uploads/2016/06/London-LinkedIn-Headshot.jpg',
                 'https://headshots.thelightcommittee.com/wp-content/uploads/2019/12/Professional-LinkedIn-Headshot-Los-Angeles.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5aee389b3c3a531e6245ae76/1530390623762-E5L73CY3GKC6QYCA46FM/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/Tokyo+-+Headshot+-+Photographer+Anthony+Wood+%287%29.jpg',
                 'https://viverastudio.com/wp-content/uploads/2017/03/02-5220-post/IMG_13(pp_w768_h1004).jpg',
                 'https://static.wixstatic.com/media/efd486_39f745ed47704ad7bb87247a540cbc3b~mv2.jpg/v1/fill/w_560,h_546,al_c,q_80,usm_0.66_1.00_0.01/efd486_39f745ed47704ad7bb87247a540cbc3b~mv2.webp',
                 'https://lh3.googleusercontent.com/proxy/NuDyvE6wME9Lwf19KrTWG0_-XlnIEyE0hcAyKPTHXnZCECk_XfsKNJ2TLMHc1j0g_OZICbxI463AYQo_ccKnlMwalPUw7qvSEjH31NV1nac3DKbctGup3vOr-ESpnVNZsg',
                 'https://teresawaltonphotos.com/wp-content/uploads/2018/06/Business-headshot-London-W12-Anna.jpg',
                 'https://images.squarespace-cdn.com/content/v1/55bcbba5e4b09c9ffac5f9a3/1527566626234-MSLGNC3W0OV1ZH1BQK84/ke17ZwdGBToddI8pDm48kMFiMyT1nneRMhnmfuSfpxZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mlM0or4nqX7jrn5yWu0hA1QXedaIFqnAbw_tQShHbKg4-O_KAc44ak5jGzrnn7f3A/Maria-001.jpg?format=2500w',
                 'https://images.squarespace-cdn.com/content/v1/5aee389b3c3a531e6245ae76/1530390599665-CGDMN86RQRLQ8YLM515K/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/Tokyo+-+Headshot+-+Photographer+Anthony+Wood+%284%29.jpg',
                 'https://media-exp1.licdn.com/dms/image/C4E12AQGJAV4if4iN7w/article-inline_image-shrink_1000_1488/0/1520213223769?e=1617235200&v=beta&t=kKfh4Iyn4OxTXeM0v1tvxOXHM_Hn1f4IvXBzLGzU6sg',
                 'https://www.corporatephotographerslondon.com/wp-content/uploads/2016/06/Studio-Headshots-LinkedIn.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5563967ee4b022cec2233829/1585654215030-4HHG8GTKPESQWGI53HYZ/ke17ZwdGBToddI8pDm48kFWxnDtCdRm2WA9rXcwtIYR7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UcTSrQkGwCGRqSxozz07hWZrYGYYH8sg4qn8Lpf9k1pYMHPsat2_S1jaQY3SwdyaXg/LinkedIn+Profile+Headshots__Surrey.jpg',
                 'https://headshots.sydney/img/business-headshots-sydney.jpg',
                 'https://eddie-hernandez.com/wp-content/uploads/2019/09/Kavita-1227.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5aee389b3c3a531e6245ae76/1530390563144-BC9CY4N5JHKV4XFHPVBG/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/Tokyo+-+Headshot+-+Photographer+Anthony+Wood+%281%29.jpg',
                 'https://cedricpuisney.photography/wp-content/uploads/2020/11/Linkedin-headshot-brussels-European-lobbying.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5c5a48b7809d8e364b16c2bf/1596588103144-YDOUWGJ09KUD4SMJJD6A/ke17ZwdGBToddI8pDm48kPJXHKy2-mnvrsdpGQjlhod7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmihaE5rlzFBImxTetd_yW5btdZx37rH5fuWDtePBPDaHF5LxdCVHkNEqSYPsUQCdT/company+profile+picture.jpg',
                 'https://lh3.googleusercontent.com/proxy/gxs_QfTEerXUE0Srn9AY8Ndr5vNdQe017U0iFGoJwf2FH2YbRK7IIZqlM_GsXkRggS_UaWRMv3A8_UACko4NPddN6jeMuAdWJ906Vp-IJljXKgkKr-6OSDA',
                 'https://eddie-hernandez.com/wp-content/uploads/2020/05/tammi_harris_netapp-.jpg',
                 'https://www.capitolphotointeractive.com/wp-content/uploads/2018/03/LinkedInAK5A9615.jpg',
                 'https://az505806.vo.msecnd.net/cms/49bcf23b-16f2-47a8-8571-a6a360910814/91f8412f-791a-443a-a607-6316d1eb757c-lg.jpg',
                 'https://3.bp.blogspot.com/-zmdL5ijfKh8/VyyKB3YQRLI/AAAAAAAAS7s/7CjP8IhA6N8svolstIlXDK3nuXqgDB5XACLcB/s1600/natasha_headshot_web-size_linkedIn.jpg',
                 'https://i.pinimg.com/236x/27/80/c4/2780c4891c93bee2b0242679862f1e15--business-men-head-shots.jpg',
                 'https://i2.wp.com/www.petruzzo.com/wp-content/uploads/2015/02/natural-headshot-in-studio-linkedin.jpg?ssl=1',
                 'https://images.squarespace-cdn.com/content/v1/5c5a48b7809d8e364b16c2bf/1596589208564-MQ1OV75OJQ49HZR80DZL/ke17ZwdGBToddI8pDm48kPJXHKy2-mnvrsdpGQjlhod7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmihaE5rlzFBImxTetd_yW5btdZx37rH5fuWDtePBPDaHF5LxdCVHkNEqSYPsUQCdT/professional+LinkedIn+photo.jpg',
                 'https://kelicommheadshots.com/wp-content/uploads/2017/01/Jason-for-LinkedIn.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5aee389b3c3a531e6245ae76/1530390581228-TAOHR6GQ3S80I1IKR0JI/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/Tokyo+-+Headshot+-+Photographer+Anthony+Wood+%283%29.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5563967ee4b022cec2233829/1585653925803-5JRD5QROA2VJQ3YWNQIM/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/LinkedIn+Headshots_Impactful_Oxford.jpg',
                 'https://arielleexecutive.com/wp-content/uploads/2020/09/headshot-photography.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5aee389b3c3a531e6245ae76/1531792840185-RTVLO0F1CO8N7DBZX24X/ke17ZwdGBToddI8pDm48kJUlZr2Ql5GtSKWrQpjur5t7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UfNdxJhjhuaNor070w_QAc94zjGLGXCa1tSmDVMXf8RUVhMJRmnnhuU1v2M8fLFyJw/D75_2601-Edit.jpg',
                 'https://brandedcopy.com.au/wp-content/uploads/2019/10/headshots_b-1.jpg',
                 'https://www.justheadshots.photo/wp-content/uploads/2019/02/061_CAB_5D4_1636-Edit_1500px-500x383.jpg',
                 'https://i2.wp.com/www.petruzzo.com/wp-content/uploads/2015/02/linkedin-headshot-in-landscape.jpg?fit=1100%2C733&ssl=1',
                 'https://eddie-hernandez.com/wp-content/uploads/2019/07/RB-1.jpg',
                 'https://images.squarespace-cdn.com/content/v1/5747b95c8a65e22d87e2be51/1537986255228-LB7O2W7K66U5IWI99X34/ke17ZwdGBToddI8pDm48kH5vi0BLs_vpV7jqxShkv7FZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpznFJtuCYrp_0l2KCtZSSi6J3dV6rlf2aa7naZJ89pts7luoM1rDXH3MPF1ghBKR60/8C2A1740%2BGiovanni%2BThe%2BPhotographer%2BBest%2BBoston%2BHeadshots%2BBoston%2BStudio%2BProfessional%2BExecutive%2BCorporate%2BLinkedin.jpg',
                 'https://arielleexecutive.com/wp-content/uploads/2020/09/business-headshot-photography.jpg',
                ]
len(headshots_urls)
# There're 25 teeth-detected headshots, and 25 no-teeth-detected headshots


# Create a dataframe
column_names = ['img_name', 'predict_teeth_label']
df = pd.DataFrame(columns = column_names)

def save_img (img_url):
    # Storing the imgs locally into folder 'evaluation_imgs' & perform teeth detection for each img saved

    # Saving and naming a file in ascending order
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    image_folder_path = 'evaluation_imgs'
    image_list = os.listdir(image_folder_path)
    count = len(image_list)
    img_name = str(count+1) + '.jpg'
    img_path = image_folder_path + '/' + img_name
    img.save(img_path)

    # Process the img from the img_path
    loaded_img = load_img(img_path)
    the_face_detector = face_detector
    the_landmark_detector = landmark_detector
    predicted_teeth_label = detect_teeth(the_face_detector, loaded_img, the_landmark_detector)
    if(predicted_teeth_label):
        predicted_label = 1
    else:
        predicted_label = 0

    # Adding the new row into the dataframe, (0 is teeth )
    row = [img_name, predicted_label]
    df.loc[len(df)] = row

for item in headshots_urls:
    print("Processing: ", headshots_urls.index(item))
    save_img(item)
df

# Creating true labels 
labels = []
for i in range(25):
    #labels.append(0)
    labels.append(1)

df['true_label'] = labels
df.head()

from sklearn.metrics import accuracy_score
# General accuracy
y_true = df['true_label'].tolist()
y_pred = df['predict_teeth_label'].tolist()
accuracy_score(y_true, y_pred)

# Accuracy within Positive (teeth_detected)
true_df =df[df['true_label']==1]
y_true = true_df['true_label'].tolist()
y_pred = true_df['predict_teeth_label'].tolist()
accuracy_score(y_true, y_pred)
# False negative: 1-0.96 = 0.04

# Accuracy within Negative (No_teeth_detected)
false_df =df[df['true_label']==0]
y_true = false_df['true_label'].tolist()
y_pred = false_df['predict_teeth_label'].tolist()
accuracy_score(y_true, y_pred)
# False positive: 1-0.84= 0.16
# There's a higher false positive than false negative, so we can say that the model tends to mistakenly predict 'teeth_detected' when teeth are not shown.

# Have a look at the wrong predicted pictures
wrong_df = df[df['predict_teeth_label'] != df['true_label']]
wrong_df

# After investigating each mis-classified picture, we can see that 2 out of 5 have mustache. However, we don't have enough data points to prove this assumption.
