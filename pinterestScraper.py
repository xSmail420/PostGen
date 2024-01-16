import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ImgScraper :
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window
        # Use webdriver_manager to automatically download and manage the ChromeDriver
        # add undetected_chromedriver here 
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def getBgUrlByTheme(self, link, options):
        try:
        
            # Go to the Instagram Direct Inbox
            self.driver.get(f"{link}%20aesthetic%20background%20image")

            time.sleep(10)
            # Wait for the recipient input field to become available
            pin = self.driver.find_elements(By.CSS_SELECTOR, 'img')
            
            if options != 0:
                for nb in range(options) :
                    print(f"bg {nb} : {pin[nb].get_attribute('src')}")
                choice = input("choose prefered bg index:")
                image_url = pin[int(choice)].get_attribute('src')
            else :
                image_url = pin[0].get_attribute('src')
            time.sleep(3)
            
            url = image_url.replace("236x", "736x")
            return url

        except Exception as e:
	        print("ERROR: "+str(e))

    def quit(self):
        self.driver.quit()