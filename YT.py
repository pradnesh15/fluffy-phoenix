from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


class youtubeVideo():
    def  __init__(self):
        # self.driver = webdriver.Chrome(executable_path = "C:\Program Files\Google\Chrome\Application\chrome.exe")
        self.driver = webdriver.Chrome()

    def get_info(self, query):
        self.query = query
        self.driver.get(url = "https://www.youtube.com/results?search_query=" + query)
        search = self.driver.find_element(By.XPATH, '//*[@id="search"]')
        # search.send_keys(query)
        video = self.driver.find_element(By.XPATH, '//*[@id="video-title"]')
        video.click()
        video_player = self.driver.find_element(By.TAG_NAME, 'body')
        video_player.send_keys('f')
        # search_button = self.driver.find_element(By.XPATH, '//*[@id="search-icon-legacy"]/yt-icon/span/div')
        # search_button.click()
        input("Press Enter to close the browser...")  # Keeps browser open until you press Enter
        self.driver.quit()

# assist = youtubeVideo()
# assist.get_info("valorant")
