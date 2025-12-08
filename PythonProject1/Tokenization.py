import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


def generate_word_cloud(input_filename):
    """
    读取评论文件，生成并显示词云图。
    """
    print("\n--- 启动词云生成程序 ---")


    stopwords_filename = 'hit_stopwords.txt'
    font_path = 'simhei.ttf'

    # 检查依赖文件是否存在
    if not os.path.exists(stopwords_filename):
        print(f"警告: 找不到停用词文件 '{stopwords_filename}'。将不使用停用词过滤。")
        stopwords = set()
    else:
        print(f"正在加载停用词: {stopwords_filename}")
        with open(stopwords_filename, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}

    if not os.path.exists(font_path):
        print(f"错误: 找不到字体文件 '{font_path}'。无法生成词云。")
        return

    # --- 读取和处理数据 ---
    print(f"正在读取文件: {input_filename}")
    with open(input_filename, 'r', encoding='utf-8') as f:
        comments_text = f.read()

    print("正在清洗文本...")
    #中文(\u4e00-\u9fa5)、英文(a-zA-Z) 和 数字(0-9)
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', comments_text)

    #对词云生成影响较大
    stopwords.add('电影')
    stopwords.add('一部')

    print("正在进行中文分词...")
    words = jieba.cut(cleaned_text)
    filtered_words = [
        word for word in words
        if word not in stopwords and len(word) > 1
    ]
    processed_text = " ".join(filtered_words)

    if not processed_text.strip():
        print("处理后没有足够的内容来生成词云。")
        return

    # --- 生成并显示词云 ---
    print("正在生成词云...")
    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        width=1000,
        height=800,
        max_words=150
    ).generate(processed_text)

    # 显示图片
    plt.figure(figsize=(12, 9))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # 保存到文件
    output_image_filename = f'wordcloud_{os.path.basename(input_filename).split(".")[0]}.png'
    wordcloud.to_file(output_image_filename)
    print(f"词云图已成功保存到: {output_image_filename}")


# --- 安全锁 ---
# 下面的代码只有在直接运行 Tokenization.py 时才会执行，用于快速测试
if __name__ == '__main__':
    print("正在以独立模式运行 Tokenization.py 用于测试...")
    test_file = 'douban_comments_1292052.txt'
    if os.path.exists(test_file):
        generate_word_cloud(test_file)
    else:
        print(f"测试失败：找不到测试文件 {test_file}，请确保该文件在当前目录下。")



