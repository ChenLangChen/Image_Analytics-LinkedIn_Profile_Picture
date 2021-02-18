from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

import sys
sys.path.append('scrape')
from linkedIn_credentials import *
# Unimport a module
# sys.modules.pop('linkedIn_cookie')

def sign_in (driver):
    # Function to sign in to LinkedIn
    driver.get('https://au.linkedin.com/')
    # Wait here :)
    time.sleep(3)
    email = driver.find_element_by_id('session_key')
    password = driver.find_element_by_id('session_password')
    sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

    email.send_keys(my_email)
    password.send_keys(linkedIn_password)
    sign_in_button.send_keys(Keys.RETURN)


def get_img_url(driver, profile_url):
    # Given an profile url, return the profile img url
    # Driver setup
    driver.get(profile_url)
    driver.add_cookie({'name' : "li_at", 'value' : cookie_value})
    print(driver.title)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    img_class = "pv-top-card__photo presence-entity__image EntityPhoto-circle-9 lazy-image ember-view"
    img_element = soup.find('img',{'class':img_class} )
    return img_element['src']



# # Testing
# # Set up the driver
# DRIVER_PATH = '/Users/chenlang/Documents/ChromeDriver/chromedriver'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
# sample_url = "https://www.linkedin.com/in/megan-smith-11704435/"
# my_img_url = scrape_img_url(sample_url)















#
