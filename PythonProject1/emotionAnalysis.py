import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import matplotlib
import os


def analyze_sentiment(input_filename):
    """
    读取评论文件，进行情感分析，并显示结果。
    """
    print("\n--- 启动情感分析程序 ---")

    # 尝试设置中文字体
    try:
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei' 是黑体
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
    except Exception as e:
        print(f"警告: 设置中文字体失败，图表可能显示乱码。错误: {e}")

    print(f"正在读取评论文件: {input_filename}")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            # 读取所有行，并用strip()去除每行末尾的换行符，同时过滤掉空行
            comments = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"错误: 文件 '{input_filename}' 未找到。")
        return  # 函数提前结束

    if not comments:
        print("错误：文件中没有找到任何有效的评论内容。")
        return

    print("正在进行情感分析，这可能需要一些时间...")
    sentiments = []
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    for comment in comments:
        s = SnowNLP(comment)
        score = s.sentiments

        if score > 0.6:
            category = '正面'
            positive_count += 1
        elif score < 0.4:
            category = '负面'
            negative_count += 1
        else:
            category = '中性'
            neutral_count += 1
        sentiments.append([comment, score, category])
    print("情感分析完成！")

    total_comments = len(comments)
    print("\n--- 情感分析结果统计 ---")
    print(f"总评论数: {total_comments}")
    print(f"正面评论: {positive_count} ({(positive_count / total_comments):.2%})")
    print(f"中性评论: {neutral_count} ({(neutral_count / total_comments):.2%})")
    print(f"负面评论: {negative_count} ({(negative_count / total_comments):.2%})")

    # 保存分析结果
    output_filename = f'sentiment_analysis_{os.path.basename(input_filename).split(".")[0]}.csv'
    results_df = pd.DataFrame(sentiments, columns=['评论内容', '情感分数', '情感分类'])
    results_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\n详细分析结果已保存到: {output_filename}")

    # 可视化结果
    print("\n正在生成可视化图表...")
    labels = ['正面 (Positive)', '中性 (Neutral)', '负面 (Negative)']
    sizes = [positive_count, neutral_count, negative_count]
    colors = ['#ff9999', '#66b3ff', '#99ff99']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.title(f'电影评论情感分析结果\n(总计: {total_comments}条)')
    plt.axis('equal')
    plt.show()


# --- 安全锁 ---
# 下面的代码只有在直接运行 emotionAnalysis.py 时才会执行，用于快速测试
if __name__ == '__main__':
    print("正在以独立模式运行 emotionAnalysis.py 用于测试...")
    # 指定一个用于测试的文件名
    test_file = 'douban_comments_1292052.txt'
    if os.path.exists(test_file):
        analyze_sentiment(test_file)
    else:
        print(f"测试失败：找不到测试文件 {test_file}，请确保该文件在当前目录下。")

