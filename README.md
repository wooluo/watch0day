
# 0day漏洞监控系统 🔍

![GitHub Actions](https://img.shields.io/github/actions/workflow/status/wooluo/watch0day/0day-monitor.yml?label=自动更新)
![GitHub last commit](https://img.shields.io/github/last-commit/wooluo/watch0day?label=最后更新)
![GitHub License](https://img.shields.io/github/license/wooluo/watch0day)

## 📌 项目简介
本项目是一个自动化0day漏洞监控系统，通过GitHub Actions定时抓取互联网最新漏洞情报，自动翻译并生成结构化报告。系统每天UTC时间9:00自动运行，也可手动触发。

[查看最新工作流运行状态](https://github.com/wooluo/watch0day/actions/workflows/0day-monitor.yml)

## ✨ 核心功能
- **自动化监控**：每天自动收集最新0day漏洞信息
- **智能翻译**：将英文漏洞报告自动翻译为中文
- **多格式输出**：
  - `JSON`格式 - 便于程序处理
  - `Markdown`格式 - 便于人工阅读
- **浏览器支持**：使用Playwright处理动态网页
- **自动提交**：结果自动更新到仓库

## 🛠 技术栈
| 技术 | 用途 |
|------|------|
| Python 3.10 | 主程序语言 |
| requests | HTTP请求 |
| BeautifulSoup4 | HTML解析 |
| feedparser | RSS订阅解析 |
| Playwright | 浏览器自动化 |
| jsonschema | 数据校验 |
| googletrans | 免费翻译 |

## 📂 文件结构
```
watch0day/
├── .github/
│   └── workflows/
│       └── 0day-monitor.yml    # GitHub Actions工作流
├── 0day.py                    # 主爬虫脚本
├── 0day_YYYY-MM-DD.json       # JSON格式漏洞数据
├── 0day_YYYY-MM-DD.md        # Markdown格式报告
└── requirements.txt           # 依赖库列表
```

## ⚙️ 工作流程
1. **定时触发**：每天UTC 9:00自动运行
2. **环境准备**：
   - 设置Python 3.10环境
   - 安装依赖库
   - 配置Playwright浏览器
3. **数据采集**：
   - 执行`0day.py`爬虫脚本
   - 从多个来源收集漏洞信息
4. **数据处理**：
   - 翻译为中文
   - 格式化为JSON和Markdown
5. **结果提交**：
   - 自动识别新生成的文件
   - 提交变更到仓库

## 🚀 使用方式
### 自动使用
- 系统每天自动更新
- 查看最新报告：
  - [JSON格式](./0day_latest.json)
  - [Markdown格式](./0day_latest.md)

### 手动运行
```bash
# 克隆仓库
git clone https://github.com/wooluo/watch0day.git
cd watch0day

# 安装依赖
pip install -r requirements.txt
python -m playwright install

# 执行爬虫
python 0day.py
```

## 🤝 参与贡献
欢迎通过以下方式参与改进：
- 报告问题：[新建Issue](https://github.com/wooluo/watch0day/issues)
- 提交改进：[创建Pull Request](https://github.com/wooluo/watch0day/pulls)
- 建议新增监控源
- 改进翻译质量

## 📜 许可证
本项目采用 [MIT License](LICENSE) 开源协议

---

> **提示**：您可以通过修改`.github/workflows/0day-monitor.yml`中的`cron`表达式来调整自动运行频率。
