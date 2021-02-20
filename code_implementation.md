
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

### How to run the code
Run *'action.ipynb'*, you can pick the profile url you want.
![alt](screenshots/change_profile_url.png)
