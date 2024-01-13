import time
import json
import random
import pyautogui
from datetime import datetime as dt
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class InstagramBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        # chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window
        # Use webdriver_manager to automatically download and manage the ChromeDriver
        # add undetected_chromedriver here 
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self):
        # static login / password
        email = "dopxthoughts" 
        password = "SmailA97/"
        # Open Instagram
        self.driver.get("https://www.instagram.com/")
        # Wait for the login elements to become available
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Find the login elements and enter email and password
        email_field.send_keys(email)
        time.sleep(3)
        password_field.send_keys(password)
        time.sleep(1)
        # Submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for the login process to complete (you may need to adjust the delay based on your internet speed)
        time.sleep(10)  # Wait for 5 seconds (adjust as needed)
    
    def createPost(self,generated_content):
        
        try:
            # Go to the Instagram Direct Inbox
            self.driver.get("https://www.instagram.com/")
            time.sleep(8)

            try:
                notification_popup = self.driver.find_element(By.XPATH, '//div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
                
                if notification_popup.is_displayed():
                    notification_popup.click()
                    time.sleep(2)
            except:
                pass
                
            posts = [r".\posts\img0.png", r".\posts\img0.png", r".\posts\img0.png"]

            for post_path in posts:
                try :
                    # Click the 'New Message' button        
                    create_button = self.driver.find_element(By.XPATH, "//div//*[contains(text(),'Create')]")
                    create_button.click()
                    time.sleep(2)
                    # Wait for the recipient input field to become available
                    wait = WebDriverWait(self.driver, 10)
                    post_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div/div//div[7]//span[contains(text(),'Post')]")))
                    post_button.click()
                    
                    upload_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Select from computer']")))
                    upload_button.click()

                    pyautogui.typewrite(post_path)
                    pyautogui.press('enter')

                    next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Next']")))
                    next_button.click()
                    time.sleep(4)
                    next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Next']")))
                    next_button.click()
                    time.sleep(4)
                    caption = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Write a caption...']")))
                    caption.send_keys(f'{generated_content["theme"]}\n.\n.\n.\n#quotes #viral {generated_content["hastags"]} #follow #followforfollowback #photooftheday #bhfyp #beautiful #likeforlike #followback #followforfollow #art')
                    time.sleep(4)
                    share_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Share']")))
                    share_button.click()
                    time.sleep(4)
                    

                except Exception as e:
                    print("ERROR fel send dm : "+str(e))
        except:
            pass

    def quit(self):
        self.driver.quit()