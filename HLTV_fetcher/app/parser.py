import datetime
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from typing import List, Tuple
from schemas import Article
from config import HLTV_URL, DATE_FORMAT
from utils import extract_id_from_url
import logging



class Parser:
    def __init__(self) -> None:
        self.enable_webdriver()
        self.enable_stealth()
        self.last_article_id: int = 0
        
        
    def enable_webdriver(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless=new')
        options.add_argument("--auto-open-devtools-for-tabs")
        options.add_argument("user-agent={}".format(user_agent)) 
        self.driver = uc.Chrome(
            use_subprocess=True,
            driver_executable_path='/usr/lib/chromium/chromedriver',
            options=options
        )
        self.driver.implicitly_wait(10)
        logging.debug('Connected to webdriver')  
    
    
    def enable_stealth(self):
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
        )
        logging.debug('Stealth enabled')
        
        
    def check_connection(self) -> bool:
        self.get_url_with_captcha(HLTV_URL)
        logging.info(self.driver.title)
        return "Counter-Strike" in self.driver.title
    
    
    def get_url_with_captcha(self, url: str):
        self.driver.get(url)
        while "Just a moment..." in self.driver.title:
            logging.info('Captcha! Re-enabling driver')
            self.enable_webdriver()
            self.enable_stealth()
            self.driver.get(url)
    
    
    def accept_cookies(self) -> None:
        try:     
            accept_cookies_button = self.driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
            accept_cookies_button.click()
        except NoSuchElementException:
            pass
    
        
    def get_news(self) -> List[str]:
        
        news_panel = self.driver.find_element(By.CLASS_NAME, "index")
        source_html = news_panel.get_attribute('innerHTML')
        if source_html is None:
            return []
        
        soup = BeautifulSoup(source_html, features="html.parser")
        todays_news = soup.find('h2', {'class' : 'newsheader'})
        if todays_news is None:
            return []
        news = todays_news.find_all_next('a', {'class' : 'article'})
        urls = [item.get('href') for item in news if item is not None]  # type: ignore
        
        return urls
            

    def parse_article(self, rel_url: str) -> Tuple[Article, List[str]]:
        url = f'{HLTV_URL}{rel_url}'
        self.get_url_with_captcha(url)
        
        panel = self.driver.find_element(By.CLASS_NAME, "newsitem")
        source_html = panel.get_attribute('innerHTML')
        if source_html is None:
            raise Exception('Got no html to parse!')
        
        id = extract_id_from_url(rel_url)
        
        soup = BeautifulSoup(source_html, features="html.parser")
        
        headline = soup.find('h1').text.strip() # type: ignore
        
        author = soup.find('span', {'class' : 'author'}).text.strip() # type: ignore
        
        date_str = soup.find('div', {'class' : 'date'}).text.strip() # type: ignore
        date = datetime.datetime.strptime(date_str, DATE_FORMAT)
        
        headertext = soup.find('p', {'class' : 'headertext'}).text.strip() # type: ignore
        
        paragraphs = soup.find_all('p', {'class' : 'news-block'})
        text = '\n\n'.join(p.text.strip() for p in paragraphs)
        
        images = soup.find_all('img', {'class' : 'image'})
        img_links = [img['src'] for img in images]
        
        return Article(id=id, 
                       title=headline, 
                       author=author, 
                       timestamp=date, 
                       url=url,
                       description=headertext,
                       content=text
                       ), img_links
        
        
            
            
