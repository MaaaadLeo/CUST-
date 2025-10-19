import os


def get_movie_id_from_url(url):
    """从URL中提取电影ID"""
    try:
        # URL结构: https://.../subject/123456/...
        movie_id = url.split('/')[4]
        return movie_id
    except IndexError:
        return None


def main_menu():
    """主菜单和程序逻辑"""
    print("=" * 40)
    print("  欢迎使用豆瓣电影评论分析工具 v1.0")
    print("=" * 40)

    current_url = ""
    comments_filename = ""

    while True:
        # 如果没有URL，提示用户输入
        if not current_url:
            current_url = input("\n请输入一个豆瓣电影的URL (例如: https://movie.douban.com/subject/1292052/): ")
            movie_id = get_movie_id_from_url(current_url)
            if not movie_id:
                print("URL格式不正确，请重新输入。")
                current_url = ""  # 重置以便再次输入
                continue
            comments_filename = f'douban_comments_{movie_id}.txt'

        print("-" * 40)
        print(f"当前电影URL: {current_url}")
        print(f"预期评论文件: {comments_filename}")
        print("-" * 40)
        print("请选择要执行的操作:")
        print("  1. 抓取电影评论 (运行 Spider.py)")
        print("  2. 生成词云图 (运行 Tokenization.py)")
        print("  3. 进行情感分析 (运行 emotionAnalysis.py)")
        print("  4. 【一键执行】所有任务")
        print("  5. 输入新的电影URL")
        print("  0. 退出程序")

        choice = input("请输入你的选择 (0-5): ")

        if choice == '1':
            # 在用户选择后才导入并执行
            import Spider
            Spider.scrape_and_save(current_url, pages=5)
        elif choice == '2':
            if not os.path.exists(comments_filename):
                print(f"\n[错误] 文件 '{comments_filename}' 不存在。请先执行选项 '1'。")
            else:
                # 在用户选择后才导入并执行
                import Tokenization
                Tokenization.generate_word_cloud(comments_filename)
        elif choice == '3':
            if not os.path.exists(comments_filename):
                print(f"\n[错误] 文件 '{comments_filename}' 不存在。请先执行选项 '1'。")
            else:
                # 在用户选择后才导入并执行
                import emotionAnalysis
                emotionAnalysis.analyze_sentiment(comments_filename)
        elif choice == '4':
            print("\n--- 开始一键执行所有任务 ---")
            # 在用户选择后才导入并执行
            import Spider
            import Tokenization
            import emotionAnalysis

            saved_file = Spider.scrape_and_save(current_url, pages=5)
            if saved_file:  # 确保文件成功保存
                Tokenization.generate_word_cloud(saved_file)
                emotionAnalysis.analyze_sentiment(saved_file)
            print("\n--- 所有任务执行完毕 ---")
        elif choice == '5':
            current_url = ""  # 清空当前URL，以便下次循环时输入新的
        elif choice == '0':
            print("感谢使用，再见！")
            break
        else:
            print("\n[错误] 无效输入，请输入 0 到 5 之间的数字。")


# --- 安全锁 ---
# 只有在直接运行 main.py 时，下面的代码才会执行
if __name__ == "__main__":
    main_menu()

