import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import random
import time

def generate_random_number(begin, stop):
    number = random.randrange(begin, stop)

    return number


#Any Spotify playlist or radio as long as it's public
#will be scraped if added here
TargetUrl = 'https://open.spotify.com/playlist/4TI52y8ILsaz1ae9DjS9ns'
'''TargetUrl = 'spotify url' '''

driver = webdriver.Firefox()

iteration = 0

SCROLL_PAUSE_TIME = 1.5


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
        '//div[@class="RP2rRchy4i8TIp1CTmb7"]/div/div[2]/span[1]'))
    )
    playlist_song_amount = playlist_song_amount_xpath.text

    #resolved having the original comma and "songs" in the number 
    num_string = playlist_song_amount.split()[0]
    cleaned_num = num_string.replace(",", "")
    cleaned_playlist_song_amount = int(cleaned_num)
    
    total_songs_expected = cleaned_playlist_song_amount

    playlist_data = {
            "Playlist Name" : uncleaned_playlist_name,
            "Playlist Song Amount" : playlist_song_amount,
            }
    
    #creates the json file, all song scraping code is here
    with open(f'{cleaned_playlist_name}.json', 'w') as json_file:
        
        json_file.write(json.dumps(playlist_data) + "\n"*2)    
        

        song_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="row"]'))
            )
        driver.execute_script("arguments[0].scrollIntoView()", 
                              driver.find_element(By.XPATH, '//div[@aria-rowindex="2"]'))
        
        iteration += 2

        for row in song_rows:
            try:
                iteration += 1

                driver.execute_script("arguments[0].scrollIntoView()", 
                              driver.find_element(By.XPATH, f'//div[@aria-rowindex="{iteration}"]'))

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//div[@aria-rowindex="{iteration}"]'))
                )

                song_name = row.find_element(By.XPATH, './/a/div').text
                artist_name = row.find_element(By.XPATH, './/a/following-sibling::span/div/a').text
                song_length = row.find_element(By.XPATH, './div/div[5]/div').text
            
                song_data = {
                    "Song Name": song_name,
                    "Artist Name": artist_name,
                    "Song Length": song_length,         
                    }

                # Scroll until enough songs are loaded
                
            
                json_file.write(json.dumps(song_data) + "\n")

                if iteration >= 100:
                    driver.quit()

            except Exception as message:
                print(f"[!] Skipped a row due to error: {message}")

except Exception as e:
    print(f"Everything broke: {e}")

driver.quit()
