import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random


TargetUrl = 'https://open.spotify.com/playlist/4TI52y8ILsaz1ae9DjS9ns'
'''TargetUrl = 'spotify url' '''

driver = webdriver.Firefox()

driver.get(TargetUrl)

print(driver.page_source)