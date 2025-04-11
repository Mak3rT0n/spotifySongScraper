import requests
import selenium
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_random_number(begin, stop):
    number = random.randrange(begin, stop)

    return number


TargetUrl = 'spotify url'
driver = webdriver.Firefox()

iteration = 0
try:
    driver.get(TargetUrl)

    playlist_name_xpath = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, 
            '//div[@class="RP2rRchy4i8TIp1CTmb7"]/span[2]'))
    )
    playlist_name = playlist_name_xpath.text

    playlist_song_amount_xpath = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, 
            '//div[@class="RP2rRchy4i8TIp1CTmb7"]/div/div[2]/span'))
    )
    playlist_song_amount = playlist_song_amount_xpath.text
   
    '''
    with open('scrapped_data.json', 'w') as json_file:
        for i in range(1, song_amount):
            iteration += 1
    '''     
      
    songs_xpath = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, 
            '//div[@class="lyVkg68L7ycnwyOcO3vj"]/following-sibling::div/div[1]/div[1]/div[2]/div[1]/a/div[1]'))
    )
    song_name = songs_xpath.text
   
    artists_xpath = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, 
            '//div[@class="lyVkg68L7ycnwyOcO3vj"]/following-sibling::div/div[1]/div[1]/div[2]/div[1]/span/div[1]/a'))
    )
    artist_name = artists_xpath.text

    song_length_xpath = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, 
            '//div[@class="lyVkg68L7ycnwyOcO3vj"]/following-sibling::div/div[1]/div[1]/div[5]/div'))
    )
    song_length = song_length_xpath.text

    print(song_name, playlist_name, playlist_song_amount, artist_name, song_length)
except Exception as fail_message:
    print(f"error occured: {fail_message}")

driver.quit()
