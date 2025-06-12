from datetime import datetime, timezone, timedelta
import json
import os
from googletrans import Translator
import asyncio

class MarkdownReporter:
    def __init__(self, items):
        self.items = items
        self.timezone = timezone(timedelta(hours=8))  # UTC+8 for Shanghai
        self.now = datetime.now(self.timezone)

    def generate(self):
        if not self.items:
            print("没有找到任何结果。")
            return "", ""

        seen = set()
        unique_items = []
        for item in self.items:
            identifier = (item['title'], item['link'])
            if identifier not in seen:
                seen.add(identifier)
                unique_items.append(item)

        unique_items.sort(key=lambda x: x.get("date", ""), reverse=True)

        timestamp = self.now.strftime('%Y%m%d_%H%M')
        json_file = f"0day_results_{timestamp}.json"
        md_file = f"0day_report_{timestamp}.md"

        # 写入 JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "generated_at": self.now.isoformat(),
                    "total_results": len(unique_items)
                },
                "results": unique_items
            }, f, ensure_ascii=False, indent=2)

        # 写入 Markdown
        with open(md_file, "w", encoding="utf-8") as f:
            translator = Translator()
            
            # 生成中文报告
            f.write("# 0day漏洞监控报告\n")
            f.write(f"**生成时间**: {self.now.strftime('%Y-%m-%d %H:%M')} (UTC+8)\n")
            f.write(f"**共找到 {len(unique_items)} 条相关信息**\n")
            
            async def translate_text(text):
                try:
                    result = await translator.translate(text, dest='zh-cn')
                    return result.text
                except Exception as e:
                    print(f"翻译失败: {e}")
                    return text
            
            for item in unique_items:
                try:
                    loop = asyncio.get_event_loop()
                    translated_title = loop.run_until_complete(translate_text(item['title']))
                    translated_summary = loop.run_until_complete(translate_text(item['summary']))
                    
                    f.write(f"\n## {translated_title}\n")
                    f.write(f"**来源**: {item['source']}  |  **日期**: {item['date']}\n")
                    f.write(f"**链接**: [{item['link']}]({item['link']})\n")
                    f.write(f"\n{translated_summary}\n")
                except Exception as e:
                    print(f"翻译处理失败: {e}")
                    f.write(f"\n## {item['title']}\n")
                    f.write(f"**来源**: {item['source']}  |  **日期**: {item['date']}\n")
                    f.write(f"**链接**: [{item['link']}]({item['link']})\n")
                    f.write(f"\n{item['summary']}\n")
            
            # 生成英文报告
            en_md_file = f"0day_report_{timestamp}_en.md"
            with open(en_md_file, "w", encoding="utf-8") as en_f:
                en_f.write("# 0day Vulnerability Monitoring Report\n")
                en_f.write(f"**Generated at**: {self.now.strftime('%Y-%m-%d %H:%M')} (UTC+8)\n")
                en_f.write(f"**Total results found**: {len(unique_items)}\n")
                
                for item in unique_items:
                    en_f.write(f"\n## {item['title']}\n")
                    en_f.write(f"**Source**: {item['source']}  |  **Date**: {item['date']}\n")
                    en_f.write(f"**Link**: [{item['link']}]({item['link']})\n")
                    en_f.write(f"\n{item['summary']}\n")

            type_stats = {}
            for item in unique_items:
                typ = item.get("type", "other")
                type_stats[typ] = type_stats.get(typ, 0) + 1
            if type_stats:
                f.write("\n## 分类统计\n")
                for typ, count in type_stats.items():
                    f.write(f"- {typ.capitalize()}: {count} 条\n")

            source_stats = {}
            for item in unique_items:
                src = item.get("source", "unknown")
                source_stats[src] = source_stats.get(src, 0) + 1
            if source_stats:
                f.write("\n## 来源统计\n")
                for src, count in source_stats.items():
                    f.write(f"- {src}: {count} 条\n")

            f.write("\n## 详细信息\n")
            current_date = ""
            for item in unique_items:
                item_date = item.get("date", "").split()[0]
                if item_date != current_date:
                    f.write(f"\n### {item_date}\n")
                    current_date = item_date
                f.write(f"#### [{item['source']}] {item['title']}\n")
                f.write(f"- **类型**: {item.get('type', '未知')}\n")
                f.write(f"- **日期**: {item.get('date', '未知')}\n")
                if "severity" in item:
                    f.write(f"- **严重程度**: {item['severity']} (CVSS: {item.get('cvss_score', '未知')})\n")
                f.write(f"- [查看详情]({item['link']})\n")
                f.write(f"\n{item.get('summary', '')}\n\n")

        print(f"已保存到 {json_file} 和 {md_file}")
        return json_file, md_file
