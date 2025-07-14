from tools.base_tool import BaseTool
from tools.bases.base_scraper import BaseScraper
import os
import re
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    RoundRobinProxyStrategy,
)


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

    async def fetch_page(self, url: str):

        # load proxies and create rotation strategy
        proxy_strategy = RoundRobinProxyStrategy(proxies)

        browser_config = BrowserConfig(
            verbose=True,
            headless=True,
            user_agent="--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )

        config = CrawlerRunConfig(
            proxy_strategy=proxy_strategy,
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=config)

            if result.success:
                print(result.markdown)
            if result.error_message:
                print(result.error_message)


