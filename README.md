豆瓣电影评论分析工具 | Douban Movie Review Analysis Toolkit

这是一个为NLP课程设计的Python小项目，它集成了一系列工具来抓取、分析和可视化豆瓣电影的评论数据。

This is a Python-based toolkit designed for an NLP course project, which integrates functionalities to scrape, analyze, and visualize movie review data from Douban.com.

项目功能 (Features)

评论爬虫 (Review Scraper): 输入一个豆瓣电影的URL，即可自动抓取指定页数的短评。

中文分词 (Text Tokenization): 使用jieba库对抓取到的中文评论进行精确分词。

词云生成 (Word Cloud Generation): 基于评论的高频词生成直观的可视化词云图。

情感分析 (Sentiment Analysis): 使用snownlp库分析每条评论的情感倾向（正面/中性/负面），并提供统计结果和饼图。

模块化主控 (Modular Main Control): 通过一个交互式主菜单 (main.py) 来调度所有功能，操作便捷。

