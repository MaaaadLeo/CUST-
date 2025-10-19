import requests
from bs4 import BeautifulSoup
import time


def scrape_and_save(url, pages=5):
    """
    根据给定的主页URL抓取指定页数的评论，并保存到文件。

    :param url: 豆瓣电影的主页URL (例如: https://movie.douban.com/subject/35881440/)
    :param pages: 想要抓取的评论页数
    :return: 成功保存的文件名，如果失败则返回 None
    """
    print("\n--- 启动爬虫程序 ---")
    try:
        # 从主页URL中提取movie_id
        movie_id = url.split('/')[4]
        print(f"从URL中成功提取 movie_id: {movie_id}")
    except IndexError:
        print("错误：无法从URL中提取movie_id，请确保URL格式正确。")
        return None

    all_comments = []
    print(f"===== 准备抓取电影ID: {movie_id} =====")

    for i in range(pages):
        # 根据movie_id构建评论区的URL
        start_index = i * 20
        comments_url = f'https://movie.douban.com/subject/{movie_id}/comments?start={start_index}&limit=20&status=P&sort=new_score'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        print(f"正在抓取第 {i + 1} 页...")
        try:
            response = requests.get(comments_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                comment_elements = soup.find_all('span', class_='short')

                if not comment_elements:
                    print(f"在第 {i + 1} 页没有找到评论，抓取结束。")
                    break

                for element in comment_elements:
                    all_comments.append(element.get_text().strip())
            else:
                print(f"抓取第 {i + 1} 页失败。状态码: {response.status_code}")
                break
        except requests.RequestException as e:
            print(f"发生网络错误: {e}")
            break

        # 礼貌性延时
        time.sleep(1.5)

    if not all_comments:
        print("未能抓取到任何评论。")
        return None

    # 保存到文件
    file_name_txt = f'douban_comments_{movie_id}.txt'
    with open(file_name_txt, 'w', encoding='utf-8') as f:
        for comment in all_comments:
            f.write(comment + '\n')

    print(f"抓取到 {len(all_comments)} 条评论，已成功保存到文件: {file_name_txt}")

    # 返回文件名，以便main.py使用
    return file_name_txt


# --- 安全锁 ---
# 下面的代码只有在直接运行 Spider.py 时才会执行，用于快速测试
if __name__ == '__main__':
    print("正在以独立模式运行 Spider.py 用于测试...")
    # 使用一个测试URL
    test_url = 'https://movie.douban.com/subject/1292052/'
    scrape_and_save(test_url, pages=2)