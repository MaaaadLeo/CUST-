import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import matplotlib
import os
import matplotlib.font_manager as fm  #字体管理器


def analyze_sentiment(input_filename):
   #read, analysis and show
    print("\n--- 启动情感分析程序 ---")

    # 强制加载项目文件夹中的 'simhei.ttf' 字体
    local_font_path = 'simhei.ttf'
    my_font = None

    if os.path.exists(local_font_path):
        print(f"成功加载本地字体: {local_font_path}")
        # 创建一个字体属性对象
        my_font = fm.FontProperties(fname=local_font_path)
    else:
        # 本地丢失字体文件的话。。。
        print(f"错误: 找不到字体文件 '{local_font_path}'。")
        print("请确保已将中文字体文件 (simhei.ttf) 复制到本项目文件夹中。")
        print("程序将继续运行，但图表中的中文将显示为乱码。")

    print(f"正在读取评论文件: {input_filename}")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            comments = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"错误: 文件 '{input_filename}' 未找到。")
        return

    if not comments:
        print("错误：文件中没有找到任何有效的评论内容。")
        return

    print("正在进行情感分析，这可能需要一些时间...")
    sentiments = []

    # --- 修正：在这里初始化计数器 ---
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    for comment in comments:
        s = SnowNLP(comment)
        score = s.sentiments

        if score > 0.6:
            category, positive_count = '正面', positive_count + 1
        elif score < 0.4:
            category, negative_count = '负面', negative_count + 1
        else:
            category, neutral_count = '中性', neutral_count + 1
        sentiments.append([comment, score, category])
    print("情感分析完成！")

    total_comments = len(comments)
    # 增加一个检查，防止评论总数为0时发生除零错误
    if total_comments == 0:
        print("错误：分析了0条评论，无法生成统计。")
        return

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

    wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                       shadow=True, startangle=140)

    if my_font:
        for text in texts:
            text.set_fontproperties(my_font)
        for text in autotexts:
            text.set_fontproperties(my_font)

    title_text = f'电影评论情感分析结果\n(总计: {total_comments}条)'
    if my_font:
        plt.title(title_text, fontproperties=my_font)
    else:
        plt.title(title_text)

    plt.axis('equal')
    plt.show()


# --- 安全锁 ---

if __name__ == '__main__':
    print("正在以独立模式运行 emotionAnalysis.py 用于测试...")
    # 指定一个用于测试的文件名
    test_file = 'douban_comments_1292052.txt'
    if os.path.exists(test_file):
        analyze_sentiment(test_file)
    else:
        print(f"测试失败：找不到测试文件 {test_file}，请确保该文件在当前目录下。")