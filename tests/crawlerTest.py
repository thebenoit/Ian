print("importing")
import sys
import os
import re
import asyncio
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from tools.onePage import OnePage

print("import finished")

print("import finished")
facebook_url = "https://www.facebook.com/marketplace/item/720324280355650/"
moveout_url = "https://www.moveout.ai"


async def test4():
    one_page = OnePage()
    await one_page.fetch_page(facebook_url)


async def test3():
    browser_config = BrowserConfig(verbose=True)  # Default browser configuration

    run_config = CrawlerRunConfig(
        remove_overlay_elements=True,
        process_iframes=True,
        exclude_external_links=True,
        delay_before_return_html=10,  # Attend 10 secondes avant de récupérer le HTML
        wait_for_images=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.facebook.com/marketplace/item/1783373245898279/",
            config=run_config,
        )

        if result.success:
            # Print clean content
            print("markdown:", result.markdown[:500])  # First 500 chars
            print("html:", result.html[:500])  # First 500 chars
            print("url: ", result.url)
            # print("clean html:", result.html)

            # Process images
            for image in result.media["images"]:
                print(f"Found image: {image['src']}")

            # Process links
            for link in result.links["internal"]:
                print(f"Internal link: {link['href']}")

        else:
            print(f"Crawl failed: {result.error_message}")


async def test2():
    browser_config = BrowserConfig(verbose=True)  # Default browser configuration
    run_config = CrawlerRunConfig()  # Default crawl run configuration

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url="https://www.moveout.ai", config=run_config)
        print(result.markdown)  # Print clean markdown content


async def main():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        tasks = [
            crawler.arun(url="https://langchain-ai.github.io/langgraph/agents/agents/"),
            crawler.arun(url="https://crawl4ai.com"),
            crawler.arun(url="https://www.twilio.com/docs"),
        ]
        results = await asyncio.gather(*tasks)

        # Print the extracted content
        for result in results:
            print(result.markdown)


# Run the async main function
asyncio.run(test4())
