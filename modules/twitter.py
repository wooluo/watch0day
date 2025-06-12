from typing import List
from playwright.sync_api import sync_playwright
from .fetcher import Fetcher
from datetime import datetime
import time

class TwitterFetcher(Fetcher):
    def fetch(self) -> List[dict]:
        results = []
        urls = [
            "https://twitter.com/search?q=0day&f=live",
            "https://twitter.com/search?q=zeroday&f=live"
        ]
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(user_agent="Mozilla/5.0")
                page = context.new_page()
                for url in urls:
                    page.goto(url, timeout=60000)
                    page.wait_for_selector('article', timeout=30000)
                    for _ in range(3):
                        page.evaluate("window.scrollBy(0, window.innerHeight)")
                        time.sleep(2)
                    tweets = page.query_selector_all('article')
                    for tweet in tweets[:20]:
                        content = tweet.inner_text()
                        if any(kw in content.lower() for kw in self.config["keywords"]):
                            link = tweet.query_selector('a[href*="/status/"]')
                            tweet_url = "https://twitter.com" + link.get_attribute('href') if link else ""
                            results.append({
                                "source": "Twitter",
                                "title": content.split('\n')[0][:100],
                                "link": tweet_url,
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "type": "social",
                                "summary": content[:200] + "..."
                            })
                browser.close()
        except Exception as e:
            print(f"[Twitter] 抓取失败: {e}")
        return results
