#!/usr/bin/env python3
"""
运行缩减版CorruptEncoder实验的快速脚本
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行命令并打印输出"""
    print(f"执行命令: {cmd}")
    print(f"工作目录: {cwd or os.getcwd()}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.stdout:
            print("输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误:")
            print(result.stderr)
            
        if result.returncode != 0:
            print(f"命令执行失败，返回码: {result.returncode}")
            return False
        else:
            print("命令执行成功!")
            return True
            
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def main():
    print("=" * 60)
    print("CorruptEncoder 缩减版实验运行脚本")
    print("=" * 60)
    
    # 检查数据集是否存在
    if not Path("E:/imagenet/corrupt-image-A").exists():
        print("错误: 找不到ImageNet-A数据集 (E:/imagenet/corrupt-image-A)")
        return
    
    if not Path("E:/imagenet/corrupt-image-B").exists():
        print("错误: 找不到ImageNet-B数据集 (E:/imagenet/corrupt-image-B)")
        return
    
    # 步骤1: 创建缩减版数据集
    print("\n步骤1: 创建缩减版数据集...")
    if not run_command("python create_reduced_dataset.py --ratio 0.3 --min-images 100"):
        print("创建缩减数据集失败!")
        return
    
    # 步骤2: 生成下游数据集文件列表
    print("\n步骤2: 生成下游数据集文件列表...")
    if not run_command("python gen_downstream_filelist.py --data_root E:/imagenet/reduced-image-B --downstream_task_name imagenet100_B --downstream_train_ratio 1.0 --save_dir ../data/imagenet100_B", 
                      cwd="get_downstream_dataset"):
        print("生成下游数据集文件列表失败!")
        return
    
    # 步骤3: 生成预训练数据集文件列表
    print("\n步骤3: 生成预训练数据集文件列表...")
    if not run_command("python generate_clean_filelist.py --root E:/imagenet/reduced-image-A", 
                      cwd="generate-poison"):
        print("生成预训练数据集文件列表失败!")
        return
    
    # 步骤4: 生成中毒数据集
    print("\n步骤4: 生成中毒数据集...")
    if not run_command("python generate_poisoned_images.py --target-class hunting-dog --support-ratio 0", 
                      cwd="generate-poison"):
        print("生成中毒图像失败!")
        return
    
    if not run_command("python generate_poisoned_filelist.py --target-class hunting-dog --support-ratio 0", 
                      cwd="generate-poison"):
        print("生成中毒文件列表失败!")
        return
    
    print("\n" + "=" * 60)
    print("数据准备完成! 现在可以开始训练了...")
    print("=" * 60)
    print("\n下一步:")
    print("1. 进入 train_moco 目录")
    print("2. 运行 bash run_pretraining.sh 开始预训练")
    print("3. 运行 bash run_linear.sh 训练线性分类器")
    print("4. 运行 bash run_test.sh 评估模型")

if __name__ == "__main__":
    main()




