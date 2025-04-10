from selenium import webdriver
from selenium.webdriver.common.by import By

class infow():
    def  __init__(self):
        # self.driver = webdriver.Chrome(executable_path = "C:\Program Files\Google\Chrome\Application\chrome.exe")
        self.driver = webdriver.Chrome()

    def get_info(self, query):
        self.query = query
        self.driver.get(url = "https://wikipedia.org")
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        search_button = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button')
        search_button.click()
        input("Press Enter to close the browser...")  # Keeps browser open until you press Enter
        self.driver.quit()
