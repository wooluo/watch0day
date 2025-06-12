import concurrent.futures
import json
from modules.hackernews import HackerNewsFetcher
from modules.nvd import NVDFetcher
from modules.exploitdb import ExploitDBFetcher
from modules.twitter import TwitterFetcher
from reporter.markdown_reporter import MarkdownReporter
import logging
import logging.handlers
import os
import pytz

# 设置日志
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/0day_monitor.log'),
        logging.StreamHandler()
    ]
)

def load_config():
    with open("config/keywords.json") as f:
        return json.load(f)

def main():
    config = load_config()

    fetchers = [
        HackerNewsFetcher(config),
        NVDFetcher(config),
        ExploitDBFetcher(config),
        TwitterFetcher(config)
    ]

    all_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetcher.fetch) for fetcher in fetchers]
        for future in concurrent.futures.as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                logging.error(f"抓取失败: {e}")

    reporter = MarkdownReporter(all_results)
    reporter.generate()

if __name__ == "__main__":
    main()
