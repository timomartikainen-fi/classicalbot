import re
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
    
class MusicBrainzEditing():
             
    def __init__(self, config):
    
        self.useragent = config['bot']['user_agent']
        self.contact = config['bot']['user_agent']
        
        self.server = config['musicbrainz']['host']
        self.username = config['musicbrainz']['user']
        self.password = config['musicbrainz']['password']
        
        self.session = None
        
        self.login(self.server, self.username, self.password)
        
    def __del__(self):
    
        self.session.close()
        
    def login(self, server, username, password):
    
        login_url = server + "/login"
        
        self.session = requests.Session()
        
        # setting default header
        self.session.headers = {
            "User-Agent": self.useragent,
            "From": self.contact
        }

        get_login_html = self.session.get(login_url)
        
        login_html = BeautifulSoup(get_login_html.content, 'html5lib')
        
        login_form_html = login_html.body.find('form', attrs = {'action': '/login'})
        
        # mandatory fields for the login form
        login_data = {
            "username": username,
            "password": password,
            "csrf_session_key": login_form_html.find('input', attrs = {'name': 'csrf_session_key'})['value'],
            "csrf_token": login_form_html.find('input', attrs = {'name': 'csrf_token'})['value'],
        }
        
        post_login = self.session.post(login_url, data = login_data)
        
        if post_login.url == server + "/user/" + username:
            logger.info(f'User \'{username}\' logged in at \'{server}\'')
        else:
            logger.info(f'User \'{username}\' failed to login at \'{server}\'')
            exit()
    
    def open_edits_count(self):        
       
        url = self.server + "/user/" + self.username + "/edits/open"
        
        get_open_edits_html = self.session.get(url)
        
        open_edits_html = BeautifulSoup(get_open_edits_html.content, 'html5lib')

        results_div = open_edits_html.find('div', attrs = {'class': 'search-toggle'})
        
        result_text = results_div.find('strong').string
             
        m = re.search(r"Found (?:at least )?([0-9]+) edits?", result_text)
        
        return int(m.group(1))
