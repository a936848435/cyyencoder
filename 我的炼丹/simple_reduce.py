#!/usr/bin/env python3
"""
简单高效的ImageNet数据集缩减脚本
"""

import os
import shutil
import random
from pathlib import Path

def reduce_dataset_simple(source_dir, target_dir, ratio=0.3, min_images=100):
    """简单版数据集缩减"""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    print(f"开始处理: {source_dir}")

    class_dirs = list(source_path.iterdir())
    total_classes = len([d for d in class_dirs if d.is_dir()])
    processed = 0

    for class_dir in source_path.iterdir():
        if not class_dir.is_dir():
            continue

        class_name = class_dir.name
        target_class_dir = target_path / class_name

        # 检查是否已存在
        if target_class_dir.exists():
            existing = len(list(target_class_dir.glob("*.JPEG")))
            if existing >= min_images:
                print(f"跳过 {class_name}: 已存在 {existing} 张")
                processed += 1
                continue

        # 获取图像文件
        images = list(class_dir.glob("*.JPEG"))
        if not images:
            print(f"跳过 {class_name}: 无图像")
            processed += 1
            continue

        # 计算保留数量
        keep_count = max(int(len(images) * ratio), min_images)
        keep_count = min(keep_count, len(images))

        # 随机选择
        selected = random.sample(images, keep_count)

        # 创建目录并复制
        target_class_dir.mkdir(exist_ok=True)
        for img in selected:
            shutil.copy2(img, target_class_dir)

        print(f"处理 {class_name}: {len(images)} -> {keep_count}")
        processed += 1

        # 显示进度
        progress = int((processed / total_classes) * 100)
        print(f"进度: {processed}/{total_classes} ({progress}%)")

    print("处理完成!")

if __name__ == "__main__":
    random.seed(42)

    print("处理ImageNet-A...")
    reduce_dataset_simple("E:/imagenet/corrupt-image-A", "E:/imagenet/reduced-image-A", 0.3, 100)

    print("\n处理ImageNet-B...")
    reduce_dataset_simple("E:/imagenet/corrupt-image-B", "E:/imagenet/reduced-image-B", 0.3, 100)

    print("\n缩减完成!")




