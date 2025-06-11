import requests
import re
from datetime import datetime, timedelta
import pytz
from .fetcher import Fetcher

class NVDFetcher(Fetcher):
    def fetch(self) -> List[dict]:
        results = []
        base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0" 
        now = datetime.now(pytz.timezone("Asia/Shanghai"))
        start_date = (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000")
        params = {
            "keywordSearch": " ".join(self.config["keywords"]),
            "pubStartDate": start_date,
            "resultsPerPage": 50
        }
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            for vuln in data.get("vulnerabilities", [])[:100]:
                cve = vuln["cve"]
                published = datetime.strptime(cve["published"], "%Y-%m-%dT%H:%M:%S.%f").astimezone(pytz.timezone("Asia/Shanghai"))
                description = next((desc["value"] for desc in cve["descriptions"] if desc["lang"] == "en"), "")
                if not any(kw in description.lower() for kw in self.config["keywords"]):
                    continue
                metrics = vuln.get("impact", {}).get("baseMetricV3", {})
                cvss = metrics.get("cvssV3", {})
                results.append({
                    "source": "NVD",
                    "title": f"{cve['id']}: {description[:80]}",
                    "link": f"https://nvd.nist.gov/vuln/detail/{cve['id']}", 
                    "date": published.strftime("%Y-%m-%d %H:%M"),
                    "type": "vulnerability",
                    "severity": cvss.get("baseSeverity", "未知"),
                    "cvss_score": cvss.get("baseScore", "未知"),
                    "summary": description[:300] + "..."
                })
        except Exception as e:
            print(f"[NVD] 抓取失败: {e}")
        return results