from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import urllib
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip, afx
import os
from datetime import date, datetime

dt = datetime.now()
weekd = dt.weekday()

if weekd == 6:
  #selenium stuff
  driver = webdriver.Chrome()


  driver.get("https://www.twitch.tv/directory/game/Albion%20Online/clips?range=7d")
  driver.maximize_window()

  #focus scroll area
  driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div').click()

  #scroll
  for x in range(4):
    actions = ActionChains(driver)
    actions.send_keys(Keys.END)
    actions.perform()
    time.sleep(1)

  #get clip List
  allClips = driver.find_elements(By.XPATH, '//a[@data-a-target="preview-card-image-link"]')
  links = [allClips.get_attribute('href') for allClips in allClips]

  vidElemList = []
  vidCounter = 0
  totalClipDuration = 0

  #clip pointer
  currentclip = 0

  #minimum video lenght from all clips
  videolenght = 360


  vidDirectories = []
  #show clip and wait for response
  while totalClipDuration<= videolenght:
    driver.get(links[currentclip])
    currentclip = currentclip + 1
    print("Klip nr " , currentclip)
    vidElem = driver.find_element(By.TAG_NAME, 'video')
    print('Czy git klip jest?  y/n')
    aswer = input()


    #if response yes then donwload and add to totalclipduration
    if aswer == 'y':
      vidElemList.append(vidElem.get_attribute('src'))
      vidCounter = vidCounter + 1
      vidName = "vid"+str(vidCounter)+".mp4"

      fullvidname = os.path.join(os.getcwd(),'videos',str( date.today()),vidName)

      #create folder
      if not os.path.exists(os.path.join(os.getcwd(),'videos',str(date.today()))):
        os.makedirs(os.path.join(os.getcwd(),'videos',str(date.today())))

      #downlaod
      urllib.request.urlretrieve(vidElem.get_attribute('src'), fullvidname)
      Vclip = VideoFileClip(fullvidname).fx(vfx.fadein, 0.3).fx(vfx.fadeout, 0.3)
      Alip = AudioFileClip(fullvidname).fx(afx.audio_fadein, 0.3).fx(afx.audio_fadeout, 0.3)

      Vclip.set_audio(Alip)
      print("Całkowita długość " , totalClipDuration)
      totalClipDuration = totalClipDuration + Vclip.duration
      vidDirectories.append(Vclip)



  driver.quit()


  #moviepy
  final_clip = concatenate_videoclips(vidDirectories)
  final_clip.write_videofile(os.path.join(os.getcwd(),'videos',str( date.today()),"finalVid.mp4"))




