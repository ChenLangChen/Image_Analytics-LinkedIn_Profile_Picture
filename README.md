![alt](screenshots/my_LinkedIn.png)
# Tasks
This project aims at creating an image analytics bot to conduct image analytics tasks on any LinkedIn profile picture in an automatic way. 

Given a linkedIn profile url, perform the following tasks on the profile picture making use of the [Azure Face API](https://azure.microsoft.com/en-us/services/cognitive-services/face/#demo) and [Dlib](http://dlib.net/python/index.html).
- Blur the background from the face.
- Identify profiles where the face is at least 50-60% of the overall photo. If it’s less than 50%, then score of face quality being too small.
- Identify if teeth are visible. If so, mention teeth is shown.
- Identity sentiment on face. E.g. smiling / happy, or neutral, sad.

--------------------------------------------------------------------------------------------

# How I approached the 4 tasks
## Blurring the background from the face
- Blurring the background is useful in video chat when you don't want others to see your messy room. It provides privacy in this 'work from home is the new norm' era. 
- In order to blur the background from the face, we need to locate the facial landmarks on the face boundaries, such as forehead and chin. Unfortunately, in Azure face API, the facial landmarks given only involve eyes, nose and lips, which are not helpful in this case. Therefore, I decided to use Dlib[1], which detect 81 facial landmarks, including the boundary landmarks we need.[2] 

![alt](screenshots/81_facial_landmarks.jpg)

- In terms of blurring, we simply blur what's outside of the facial boundary. OpenCV.GaussianBlur() is used, which is useful in reducing image noise.

## Identify profiles where the face is at least 50-60% of the overall photo
- This is useful for a recruiter who wants to filter out profiles with bad quality pictures. 
- When calculating the area of the overall image, instead of simply using width * height, I use the area of the cropped image. This is because that on a LinedIn profile, the picture is cropped into a circle.
- As for calculating the area of the face, I used cv2.contourArea(), passing the face boundary landmarks detected by Dlib previously as a numpy array.
```python
contour_area = cv2.contourArea(np.array(sorted_landmarks))
```

## Identify if teeth are visible.
- Imagine when you're taking a selfie, instead of setting a timer, it would be great if your camera can detect your most genuine smile 😬 and snap a picture automatically. 🤳🏼 📸   That's when teeth detection can come into use. 
- My first reaction to this task was to build a computer vision neural network to detect teeth, but it requires a great amount of data. Therefore, I need to make use of something more accessible. 
- Inspired by blink detection, where EAR is used to decide if a person blinks. EAR refers to the average distance of P2 - P6 and P3 - P5 divided by the distance from P1 to P4. 
- The larger EAR, the more likely that the person' eyes are open, not blinking. When the eye is closed, the EAR is close to 0. Similarly, I apply MAR to teeth detected. MAR = lips gap / lips width.[3] MAR over a certain point would indicate that teeth is detected. We need to find the suitable MAR. 

**MAR**: Mouth Aspect Ratio
**EAR** : Eye Aspect Ratio

![EAR](screenshots/EAR.jpg)
```shell
EAR = (|P2 - P6|+|P3 - P5|) / (2 * |P1 - P4|)
```


![MAR](screenshots/MAR.png)
```shell
MAR = (|P61 - P67|+|P62 - P66|+||P63 - P65|) / (3 * |P48 - P54|)
```
### MAR decision
After testing on 282 pictures, **0.09** was decided to be the dividing point. Any picture with an **MAR >= 0.09** is predicted to have teeth detected 😬 and vice versa 😐.

### Independent evaluation
- In order to figure our how MAR works in real life, I performed an independent evaluation on 50 LinkedIn headshots (25 teeth-detected & 25 no-teeth-detected). It turned out that there was a **false negative** rate of 0.04 and a **false positive** rate of 0.16. It works well in general, with a accuracy of 90%, but tend to predict a person without showing teeth to be showing teeth.

- Besides, I also found out that it doesn't do well in pictures with mustache and teeth visible. For a debugging purpose, plotting the lower lip bottom landmarks detected by Dlib shows that it tends to mistakenly detect the upper lip bottom landmarks on the teeth. The mistake gives a narrower lips gap and thus a smaller MAR.
For example, please take a closer look to the green dots between lips.

![alt](screenshots/mustache_example.png)


## Identity sentiment on face
**Azure Face client library** has a very convenient interface for detection on a wide range of emotions, such as 'anger', 'contempt', 'disgust', and 'happiness'. Therefore, Azure Face client library is used for sentiment detection here.

## Challenges I encountered
### Scraping picture from LinkedIn profile
LinkedIn has a robust anti-scraping mechanism, so I had to turn to Selenium. Usually I use request, a python library, for web scraping. However, the scraping bot can be easily detected by LinkIn. With Selenium, we can simulate the human interaction with a website, which can fool the LinkedIn server. If you're interested in how I scrape a LinkedIn profile, please check out the source code 'scrape/scrape_linkedIn.py'.

### Teeth detection
Teeth detection was also quite challenging. Before coming up with the MAR method, I created a predictive model based on the **percentage of smile** and the **ratio between lips gap and thickness of lower lip** which can be both found with Azure Face client library. Upper lip thickness was omitted because sometimes the upper lip is covered when thick and long mustache is present. However, my attempt was not successful, as it gave an accuracy rate around 65%. The code for teeth detection using Azure is in 'Azure_Teeth_Detection' folder.

----------------------------------------------------------------------------------------

# How to implement the code
## Dependencies download
### Creating Python virtual environment
[env](https://docs.python.org/3/library/venv.html)
### Install the packages needed
- requirements.txt
```shell
install -r requirements.txt
```
[Install Dlib](https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/)

## Credentials setup
### Azure credential
In '*credentials/key_endpoint.py*', replace **KEY** and **ENDPOINT** of Azure Face API.
[Azure Tutorial](https://docs.microsoft.com/en-au/azure/cognitive-services/face/quickstarts/client-libraries?tabs=visual-studio&pivots=programming-language-python)
### LinkedIn Credential
- I recommend creating a dummy LinkedIn account for this project, as in the process of mining profile pictures, you might exceed the number of people you can view with your account (Not a problem if you use Premium :D).
- In '*scrape/linkedIn_credentials.py*', replace **cookie_value**, **linkedIn_password**, **my_email** with yours.
#### How to access cookie_value
The session cookie is required when we use selenium for scraping LinkedIn profiles.
- Inspect the web page when you're logged in. ("option+command+i" for Mac)
- **Application** -> **Cookies** -> Pick the **www.linkedIn.com** option. -> Copy **li_at** value.

### Manual
Run *'action.ipynb'*, you can change **sample_url** to the profile url you want.
![alt](screenshots/change_profile_url.png)

-------------------------------------------------------------------------------------------------

# References:
[1] https://sefiks.com/2020/11/20/facial-landmarks-for-face-recognition-with-dlib/
[2] https://github.com/codeniko/shape_predictor_81_face_landmarks
[3] https://www.freecodecamp.org/news/smilfie-auto-capture-selfies-by-detecting-a-smile-using-opencv-and-python-8c5cfb6ec197/