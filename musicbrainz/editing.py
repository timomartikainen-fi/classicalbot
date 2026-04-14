import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import logging

logger = logging.getLogger(__name__)

class MusicBrainzEditing():

    def __init__(self, config):

        self.server = config["musicbrainz"]["host"]
        self.username = config["musicbrainz"]["user"]
        self.password = config["musicbrainz"]["password"]

        self.useragent = config["bot"]["user_agent"]
        self.contact = config["bot"]["contact"]

        self.driver = None

    def __enter__(self):

        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={self.useragent} ( {self.contact} )")

        self.driver = webdriver.Chrome(options = options)

        self.login(self.server, self.username, self.password)

        return self

    def login(self, server, username, password):

        self.driver.get(server + "/login")

        login_form = self.driver.find_element(By.XPATH, "//form[contains(@action, '/login')]")

        login_form.find_element(By.NAME, "username").send_keys(username)
        login_form.find_element(By.NAME, "password").send_keys(password)
        login_form.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(self.driver, 10).until(EC.url_changes(server + "/login"))

        if self.driver.current_url == server + "/user/" + username:
            logger.info(f"User '{username}' logged in at '{server}'")
        else:
            logger.info(f"User '{username}' failed to login at '{server}'")
            exit()

    def open_edits_count(self):

        self.driver.get(self.server + "/user/" + self.username + "/edits/open")
        wait = WebDriverWait(self.driver, 10)

        try:

            results_div = wait.until(
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

    # Sets a musical key for a work, but only if no key is previously selected (= supports only 1 key per work)
    def set_work_key(self, mbid):

        try:

            self.driver.get(self.server + "/work/" + mbid + "/edit")
            wait = WebDriverWait(self.driver, 10)

            ##type_dropdown_xpath = "//tr[contains(., 'Key')]//select[contains(@name, 'edit-work.attributes')]"

            # checking if there's a key already set
            key_value_xpath = "//tr[contains(., 'Key')]//select[contains(@name, '.value')]"
            value_element = wait.until(EC.presence_of_element_located((By.XPATH, key_value_xpath)))

            key_select = Select(value_element)

            #wait.until(lambda d: len(key_select.options) > 1) # waiting for options to populate
            # current_key = key_select.first_selected_option.text.strip()

            curren_key = ""

            if not current_key:

                print("ei avainta!")

            else:

                print(current_key)
            '''
            wait = WebDriverWait(self.driver, 10)

            type_element = wait.until(EC.presence_of_element_located((By.XPATH, type_dropdown_xpath)))
            type_select = Select(type_element)

            wait.until(lambda d: len(type_select.options) > 1) # waiting for options to populate

            # if some count is 0?

            type_select.select_by_visible_text("Key")

            key_value_xpath = "//tr[contains(., 'Key')]//select[contains(@name, '.value')]"
            value_element = wait.until(EC.visibility_of_element_located((By.XPATH, key_value_xpath)))

            key_value_select = Select(value_element)

            wait.until(lambda d: len(key_value_select.options) > 1) # waiting for options to populate

            key_value_select.select_by_visible_text("G major")

            total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
            total_width = self.driver.execute_script("return document.body.parentNode.scrollWidth")

            current_text = type_select.first_selected_option.text.strip()

            print(current_text)

            self.driver.set_window_size(total_width, total_height)

            self.driver.save_screenshot("element.png")
            '''
            #current_option = key_select.first_selected_option
            #current_text = current_option.text.strip()
            #current_value = current_option.get_attribute("value")

            #if not current_value or current_text == "":
            #    print("No key is currently set. Proceeding to select one...")
            #    key_select.select_by_visible_text("G major")
            #else:
            #    print(f"A key is already set: {current_text}")

        except Exception as e:

            print(f"Error: {e}")

    def __exit__(self, exc_type, exc_value, exc_traceback):

        if self.driver:
            self.driver.quit()