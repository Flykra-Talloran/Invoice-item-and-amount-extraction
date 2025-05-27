import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

def file_hash(filepath, block_size=65536):
    """计算文件哈希值（SHA256）"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_pdfs(root_dir):
    """遍历文件夹，找出重复的 PDF 文件"""
    hash_dict = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                full_path = os.path.join(dirpath, filename)
                try:
                    h = file_hash(full_path)
                    if h in hash_dict:
                        hash_dict[h].append(full_path)
                    else:
                        hash_dict[h] = [full_path]
                except Exception as e:
                    print(f"无法读取 {full_path}: {e}")
    # 只保留有重复的文件
    return {h: paths for h, paths in hash_dict.items() if len(paths) > 1}

def main():
    # 弹窗选择文件夹
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    messagebox.showinfo("选择文件夹", "请选择要查重的PDF文件夹。")
    root_dir = filedialog.askdirectory(title="选择要查重的文件夹")
    if not root_dir:
        print("未选择文件夹，程序结束。")
        return

    print(f"遍历文件夹：{root_dir}")
    duplicates = find_duplicate_pdfs(root_dir)
    if not duplicates:
        print("没有找到重复的PDF文件。")
        return

    for h, paths in duplicates.items():
        print("\n找到重复文件（内容完全一致）:")
        for idx, p in enumerate(paths):
            print(f"  [{idx}] {p}")
        keep_idx = input(f"你想**保留哪个文件**？输入序号（多个用,隔开），其他将被删除：")
        try:
            to_keep = set(int(i.strip()) for i in keep_idx.split(',') if i.strip().isdigit())
        except:
            print("输入有误，跳过该组。")
            continue
        for idx, p in enumerate(paths):
            if idx not in to_keep:
                try:
                    os.remove(p)
                    print(f"已删除：{p}")
                except Exception as e:
                    print(f"删除失败 {p}: {e}")
    print("处理结束。")

if __name__ == "__main__":
    main()
