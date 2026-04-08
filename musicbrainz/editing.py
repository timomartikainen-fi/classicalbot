import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging

logger = logging.getLogger(__name__)
   
class MusicBrainzEditing():
             
    def __init__(self, config):
        
        self.server = config['musicbrainz']['host']
        self.username = config['musicbrainz']['user']
        self.password = config['musicbrainz']['password']
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={config['bot']['user_agent']} ( {config['bot']['user_agent']} )")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)    
               
        self.login(self.server, self.username, self.password)
        
    def login(self, server, username, password):
          
        self.driver.get(server + "/login")
        
        login_form = self.driver.find_element(By.XPATH, "//form[contains(@action, '/login')]")
        
        login_form.find_element(By.NAME, "username").send_keys(username)
        login_form.find_element(By.NAME, "password").send_keys(password)
        login_form.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.driver, 10).until(EC.url_changes(server + "/login"))

        if self.driver.current_url == server + "/user/" + username:
            logger.info(f'User \'{username}\' logged in at \'{server}\'')
        else:
            logger.info(f'User \'{username}\' failed to login at \'{server}\'')
            exit()

    def open_edits_count(self):
        
        self.driver.get(self.server + "/user/" + self.username + "/edits/open")
        
        try:
        
            results_div = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-toggle"))
            )
            
            result_text = results_div.find_element(By.TAG_NAME, "strong").text
            
            m = re.search(r"Found (?:at least )?([0-9]+) edits?", result_text)
            
            if m:
                count = int(m.group(1))
                logger.info(f"Found {count} open edits.")
                return count
            else:
                logger.warning("Could not find edit count.")
                return 0
            
        except TimeoutException:
            logger.error("Timed out waiting for the edits page to load.")
            return 0