import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random

def generate_random_number(begin, stop):
    number = random.randrange(begin, stop)

    return number

#Any Spotify playlist or radio as long as it's public
#will be scraped if added here
TargetUrl = 'https://open.spotify.com/playlist/4TI52y8ILsaz1ae9DjS9ns'
'''TargetUrl = 'spotify url' '''

driver = webdriver.Firefox()

iteration = 0

#Try block holds all code for scraping the data and adding it to a json file
try:
    driver.get(TargetUrl)

    playlist_name_xpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
        '//div[@class="RP2rRchy4i8TIp1CTmb7"]/span[2]'))
    )
    uncleaned_playlist_name = playlist_name_xpath.text

    #Cleans the playlist name for the creation of the json file
    cleaned_playlist_name = ''
    for i in uncleaned_playlist_name:
        if i in "!@#$%^&*\\/\'<>.,:;{[]}|+=-":
            cleaned_playlist_name += "_"
        else:
            cleaned_playlist_name += i

    playlist_song_amount_xpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
        '//div[@class="RP2rRchy4i8TIp1CTmb7"]/div/div[2]/span'))
    )
    playlist_song_amount = playlist_song_amount_xpath.text

    #resolved having the original comma and "songs" in the number 
    num_string = playlist_song_amount.split()[0]
    cleaned_num = num_string.replace(",", "")
    cleaned_playlist_song_amount = int(cleaned_num)
    
    playlist_data = {
            "Playlist Name" : uncleaned_playlist_name,
            "Playlist Song Amount" : playlist_song_amount,
            }
    
    with open(f'{cleaned_playlist_name}.json', 'w') as json_file:
        
        json_file.write(json.dumps(playlist_data) + "\n"*2)    
        

        for i in range(1, int(cleaned_playlist_song_amount) + 1):
            iteration += 1
            
            songs_xpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
            f'//div[@class="lyVkg68L7ycnwyOcO3vj"]/following-sibling::div/div[{iteration}]/div[1]/div[2]/div[1]/a/div[1]'))
            )
            song_name = songs_xpath.text

            artists_xpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
            f'//div[@class="lyVkg68L7ycnwyOcO3vj"]/following-sibling::div/div[{iteration}]/div[1]/div[2]/div[1]/span/div[1]/a'))
            )
            artist_name = artists_xpath.text

            song_length_xpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
            f'//div[@class="lyVkg68L7ycnwyOcO3vj"]/following-sibling::div/div[{iteration}]/div[1]/div[5]/div'))
            )
            song_length = song_length_xpath.text
            
            if (iteration % 5) == 0:
                driver.execute_script("window.scrollBy(0, 500);")

            song_data = {
                "Song Name": song_name,
                "Artist Name": artist_name,
                "Song Length": song_length,         
                }
            
            json_file.write(json.dumps(song_data) + "\n")
    

    print(song_name, uncleaned_playlist_name, playlist_song_amount, artist_name, song_length)
except Exception as fail_message:
    print(f"error occured: {fail_message}")

driver.quit()
