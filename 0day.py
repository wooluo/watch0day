import concurrent.futures
import json
from modules.hackernews import RSSFetcher
from reporter.markdown_reporter import MarkdownReporter
import logging
import logging.handlers
import os

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
        RSSFetcher(config),


    ]

    all_results = []

    total_fetchers = len(fetchers)
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetcher.fetch) for fetcher in fetchers]
        for future in concurrent.futures.as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
                completed += 1
                logging.info(f"进度: {completed}/{total_fetchers} 数据源已完成")
            except Exception as e:
                logging.error(f"抓取失败: {e}")
                completed += 1

    reporter = MarkdownReporter(all_results)
    reporter.generate()

if __name__ == "__main__":
    main()
