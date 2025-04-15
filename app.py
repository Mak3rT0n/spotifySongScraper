import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

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
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="row"]'))
            )
        
        json_file.write(json.dumps(playlist_data) + "\n"*2)    
        
        print("Started Scraping")

        # +1 is needed because the first song of the row starts at row 2
        for i in range(1, (total_songs_expected + 1)):
            try:                
                iteration += 1
                
                #scrolls into view the element, then makes sure its loaded
                driver.execute_script("arguments[0].scrollIntoView()", 
                              driver.find_element(By.XPATH, f'//div[@aria-rowindex="{iteration}"]'))

                current_row = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//div[@aria-rowindex="{iteration}"]'))
                )
                
                song_number = str(iteration - 1)
                song_name = current_row.find_element(By.XPATH, './/a/div').text
                artist_name = current_row.find_element(By.XPATH, './/a/following-sibling::span/div/a').text
                song_length = current_row.find_element(By.XPATH, './div/div[5]/div').text
            
                song_data = {
                    "No." : song_number,
                    "Song Name": song_name,
                    "Artist Name": artist_name,
                    "Song Length": song_length,         
                    }
            
                json_file.write(json.dumps(song_data) + "\n")


            except Exception as message:
                print(f"[!] Skipped a row due to error: {message}")

except Exception as e:
    print(f"Everything broke: {e}")

driver.quit()
