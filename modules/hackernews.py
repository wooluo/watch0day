from typing import List
import feedparser
from .fetcher import Fetcher
from datetime import datetime
import pytz

class HackerNewsFetcher(Fetcher):
    def fetch(self) -> List[dict]:
        results = []
        url = "https://feeds.feedburner.com/TheHackersNews" 
        try:
            feed = feedparser.parse(url)
            if feed.bozo and feed.bozo_exception:
                raise Exception(f"RSS解析错误: {feed.bozo_exception}")
            for entry in feed.entries[:50]:  # 只检查最新50条
                title = entry.title.lower()
                desc = entry.description.lower()
                if any(kw in title or kw in desc for kw in self.config["keywords"]):
                    date = datetime(*entry.published_parsed[:6]).astimezone(pytz.timezone("Asia/Shanghai"))
                    results.append({
                        "source": "The Hacker News",
                        "title": entry.title,
                        "link": entry.link,
                        "date": date.strftime("%Y-%m-%d %H:%M"),
                        "type": "news",
                        "summary": entry.description[:250] + "..."
                    })
        except Exception as e:
            print(f"[HackerNews] 抓取失败: {e}")
        return results