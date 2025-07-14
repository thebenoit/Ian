from tools.base_tool import BaseTool
from tools.bases.base_scraper import BaseScraper
import os
from crawl4ai.async_configs import BrowserConfig




class OnePage(BaseTool, BaseScraper):
    def __init__(self):
        super().__init__()
        
        proxies = {"http": os.getenv("PROXIES_URL"), "https": os.getenv("PROXIES_URL")}
        
        
        

    @property
    def name(self):
        return "one_page"
    
    @property
    def description(self):
        return "fetch deeply one page(or multiple in a concurrent way)"
    
    def fetch_page(self,url:str):
        
        
        
        browser_config = BrowserConfig(
            verbose=True)
             
        
        