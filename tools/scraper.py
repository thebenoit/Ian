from tools.base_tool import BaseTool
from tools.bases.base_scraper import BaseScraper


class Scraper(BaseTool, BaseScraper):
    def __init__(self):
        super().__init__()

    def run(self, url: str):
        pass