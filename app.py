from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

#TODO Add GUI to paste in links
#TODO Add progress bar into GUI
#TODO Funcionize code
#TODO DRY code
#TODO Switch to CSV and convert file type from the GUI into what ever file type selected
#TODO Add ability to auto download a zip with all of the songs (aiming for functionality will add higher quality like FLAC after functional)

#Any Spotify playlist or radio as long as it's public
#will be scraped if added here
print("Paste or type your playlist: ")
TargetUrl = str(input())
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
    print("got playlist name")
    #Cleans the playlist name for the creation of the json file
    cleaned_playlist_name = ''
    for i in uncleaned_playlist_name:
        if i in "!@#$%^&*\\/\'<>.,:;{[]}|+=-":
            cleaned_playlist_name += "_"
        else:
            cleaned_playlist_name += i
    print("cleaned playlist name")
    playlist_song_amount_xpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
        '//span[@data-testid="entityTitle"]/following-sibling::*[last()]/div[last()]/span'))
    )
    playlist_song_amount = playlist_song_amount_xpath.text
    print("got song amount")
    #resolved having the original comma and "songs" in the number 
    num_string = playlist_song_amount.split()[0]
    cleaned_num = num_string.replace(",", "")
    cleaned_playlist_song_amount = int(cleaned_num)
    
    total_songs_expected = cleaned_playlist_song_amount
    print(total_songs_expected)
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

        #the html row has the first song at row 2, we add 2 since the end is excluded
        #Eg. song 1 is located on row 2 so we need a range of 3
        for i in range(1, (total_songs_expected + 2)):
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
                artist_name = current_row.find_element(By.XPATH, './/div[@role="gridcell" and @aria-colindex="2"]//span[last()]//a').text
                song_length = current_row.find_element(By.XPATH, './/div[@role="gridcell"][last()]/div[@data-encore-id="text"]').text
            
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
