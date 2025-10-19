
# 📽️ Douban Sentiment Miner (豆瓣影评情感挖掘机)

```text
  ____              _                  __  __ _                 
 |  _ \  ___  _   _| |__   __ _ _ __  |  \/  (_)_ __   ___ _ __ 
 | | | |/ _ \| | | | '_ \ / _` | '_ \ | |\/| | | '_ \ / _ \ '__|
 | |_| | (_) | |_| | |_) | (_| | | | || |  | | | | | |  __/ |   
 |____/ \___/ \__,_|_.__/ \__,_|_| |_||_|  |_|_|_| |_|\___|_|   
                                              v1.0.0 | NLP Course
从混乱的文本中，听见大众最真实的声音。 Turning noise into signal, one comment at a time.
#
🧐 核心使命 (Mission)
面对热门电影成千上万条的评论，人类的阅读速度是有限的。本项目旨在通过 NLP 技术，构建一套自动化的 ETL Pipeline，将非结构化文本
转化为可视化的决策依据：

🕷️ 采集 (Extract)：模拟人类行为，无痛抓取豆瓣影评。
🧹 清洗 (Transform)：去除噪声，提取核心中文字符。
🧠 分析 (Analyze)：基于贝叶斯模型计算情感极性，提取高频关键词。
📊 展现 (Load/Visualize)：生成直观的饼图与词云。



技术架构 (Technical Architecture)
本项目基于 Python 3 开发，采用模块化设计，主要技术选型如下：

+--------------+--------------------------+------------------------------------------------+
|     模块     |       核心库/技术        |                    功能描述                    |
+--------------+--------------------------+------------------------------------------------+
|  数据采集层  | Requests, BeautifulSoup4 | 实现 HTTP 请求模拟、User-Agent 伪装及 DOM 解析   |
|  情感分析层  | SnowNLP                  | 基于朴素贝叶斯 (Naive Bayes) 的中文情感分析       |
|  文本处理层  | Jieba, Re (Regex)        | 执行中文分词、停用词过滤及非结构化文本清洗          |
|  可视化层    | Matplotlib, WordCloud    | 生成统计图表与词云，已内置解决中文乱码方案          |
+--------------+--------------------------+------------------------------------------------+

📂 项目结构 (Structure)
Bash
Douban-Sentiment-Miner/
├── main.py                # 🚀 指挥中心：交互式命令行入口 (CLI)
├── Spider.py              # 🕸️ 采集器：负责数据的抓取与存储
├── Tokenization.py        # ☁️ 词云生成器：分词与可视化
├── emotionAnalysis.py     # 🧭 情感罗盘：计算情感得分并生成饼图
├── releaseCache.py        # 🔧 维修工：一键修复 Matplotlib 字体缓存问题
├── hit_stopwords.txt      # 🛑 过滤器：哈工大停用词表
├── simhei.TTF             # 🔤 核心资产：内置中文字体 (实现零依赖运行)
└── douban_comments_*.txt  # 📄 产出物：抓取的原始数据


快速开始 (Quick Start)

1. 环境准备

确保已安装必要的 Python 库：
pip install requests beautifulsoup4 jieba snownlp matplotlib pandas wordcloud

2. 启动引擎
运行主程序，即可唤醒交互式菜单：
python main.py

3. 操作指南 (CLI Menu)

程序启动后，你将看到以下选项：

[1] 单独抓取：输入 URL，只做数据采集。
[2] 生成词云：对已有本地数据进行关键词提取。
[3] 情感分析：对已有本地数据进行正负面判别。
[4] 🚀 一键全流程：(推荐) 输入 URL，自动完成 抓取 -> 分析 -> 可视化 全过程。

