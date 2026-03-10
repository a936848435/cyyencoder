#!/usr/bin/env python3
"""
ImageNet数据集缩减脚本
用于在保持实验效果的前提下减少数据集大小，便于服务器上传和复现
"""

import os
import shutil
import random
from pathlib import Path
import argparse

def create_reduced_dataset(source_dir, target_dir, reduction_ratio=0.3, min_images_per_class=100):
    """
    创建缩减版数据集
    
    Args:
        source_dir: 源数据集目录
        target_dir: 目标数据集目录  
        reduction_ratio: 缩减比例 (0.3表示保留30%的数据)
        min_images_per_class: 每个类别最少保留的图像数量
    """
    
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # 创建目标目录
    target_path.mkdir(parents=True, exist_ok=True)
    
    print(f"开始处理数据集: {source_dir}")
    print(f"缩减比例: {reduction_ratio} (保留{int(reduction_ratio*100)}%)")
    print(f"每类最少保留: {min_images_per_class} 张图像")
    
    total_classes = 0
    total_images = 0
    total_copied = 0
    
    # 遍历所有类别文件夹
    for class_dir in source_path.iterdir():
        if class_dir.is_dir():
            total_classes += 1
            class_name = class_dir.name
            
            # 获取该类别的所有图像文件
            image_files = list(class_dir.glob("*.JPEG"))
            total_images += len(image_files)
            
            # 计算要保留的图像数量
            keep_count = max(
                int(len(image_files) * reduction_ratio),
                min_images_per_class
            )
            keep_count = min(keep_count, len(image_files))  # 不能超过总数
            
            # 随机选择要保留的图像
            selected_images = random.sample(image_files, keep_count)
            
            # 创建目标类别目录
            target_class_dir = target_path / class_name
            target_class_dir.mkdir(exist_ok=True)
            
            # 复制选中的图像
            for img_file in selected_images:
                shutil.copy2(img_file, target_class_dir)
                total_copied += 1
            
            print(f"类别 {class_name}: {len(image_files)} -> {keep_count} 张图像")
    
    print(f"\n处理完成!")
    print(f"总类别数: {total_classes}")
    print(f"原始图像总数: {total_images}")
    print(f"保留图像总数: {total_copied}")
    print(f"实际缩减比例: {total_copied/total_images:.2%}")
    print(f"目标目录: {target_dir}")

def main():
    parser = argparse.ArgumentParser(description='创建缩减版ImageNet数据集')
    parser.add_argument('--source-a', default='E:/imagenet/corrupt-image-A', 
                       help='ImageNet-A源目录')
    parser.add_argument('--source-b', default='E:/imagenet/corrupt-image-B', 
                       help='ImageNet-B源目录')
    parser.add_argument('--target-a', default='E:/imagenet/reduced-image-A', 
                       help='缩减版ImageNet-A目标目录')
    parser.add_argument('--target-b', default='E:/imagenet/reduced-image-B', 
                       help='缩减版ImageNet-B目标目录')
    parser.add_argument('--ratio', type=float, default=0.3, 
                       help='缩减比例 (0.3表示保留30%)')
    parser.add_argument('--min-images', type=int, default=100, 
                       help='每类最少保留的图像数量')
    
    args = parser.parse_args()
    
    # 设置随机种子确保可重复性
    random.seed(42)
    
    print("=" * 60)
    print("ImageNet数据集缩减工具")
    print("=" * 60)
    
    # 处理ImageNet-A
    print("\n处理ImageNet-A (预训练数据集)...")
    create_reduced_dataset(
        args.source_a, 
        args.target_a, 
        args.ratio, 
        args.min_images
    )
    
    # 处理ImageNet-B  
    print("\n处理ImageNet-B (下游任务数据集)...")
    create_reduced_dataset(
        args.source_b, 
        args.target_b, 
        args.ratio, 
        args.min_images
    )
    
    print("\n" + "=" * 60)
    print("数据集缩减完成!")
    print("=" * 60)
    
    # 计算磁盘空间节省
    def get_dir_size(path):
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total += os.path.getsize(filepath)
        return total
    
    try:
        original_size = get_dir_size(args.source_a) + get_dir_size(args.source_b)
        reduced_size = get_dir_size(args.target_a) + get_dir_size(args.target_b)
        saved_size = original_size - reduced_size
        
        print(f"原始数据集大小: {original_size / (1024**3):.2f} GB")
        print(f"缩减数据集大小: {reduced_size / (1024**3):.2f} GB") 
        print(f"节省空间: {saved_size / (1024**3):.2f} GB ({saved_size/original_size:.1%})")
    except:
        print("无法计算磁盘空间节省情况")

if __name__ == "__main__":
    main()

