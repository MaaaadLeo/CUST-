import os
import matplotlib

print("正在查找 matplotlib 字体缓存...")

try:
    cache_dir = matplotlib.get_cachedir()
    print(f"Matplotlib 缓存目录位于: {cache_dir}")

    deleted_files = []
    # 遍历缓存目录中的所有文件
    for file in os.listdir(cache_dir):
        # 字体缓存通常是 .json 或 .cache 文件
        if file.endswith('.json') or file.endswith('.cache'):
            file_path = os.path.join(cache_dir, file)
            try:
                os.remove(file_path)
                print(f"  [已删除] {file}")
                deleted_files.append(file)
            except Exception as e:
                print(f"  [删除失败] 无法删除 {file}: {e}")

    if not deleted_files:
        print("\n在缓存目录中没有找到可删除的字体缓存文件。")
    else:
        print("\n字体缓存已成功清除！")

except Exception as e:
    print(f"清除缓存时发生意外错误: {e}")

print("\n请现在重新运行你的 main.py 程序。")
print("Matplotlib 将在下次运行时重建字体列表，这可能需要几秒钟。")