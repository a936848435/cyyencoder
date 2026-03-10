#!/usr/bin/env python3
"""检查数据集缩减进度"""

from pathlib import Path

def check_progress():
    # 检查ImageNet-A
    path_a = Path("E:/imagenet/reduced-image-A")
    if path_a.exists():
        classes_a = list(path_a.iterdir())
        total_a = len([d for d in classes_a if d.is_dir()])
        print(f"ImageNet-A: {total_a}/108 类别已完成")

        # 统计图像数量
        total_images_a = 0
        for class_dir in classes_a:
            if class_dir.is_dir():
                images = list(class_dir.glob("*.JPEG"))
                total_images_a += len(images)
        print(f"ImageNet-A: {total_images_a} 张图像")

    # 检查ImageNet-B
    path_b = Path("E:/imagenet/reduced-image-B")
    if path_b.exists():
        classes_b = list(path_b.iterdir())
        total_b = len([d for d in classes_b if d.is_dir()])
        print(f"ImageNet-B: {total_b}/100 类别已完成")

        # 统计图像数量
        total_images_b = 0
        for class_dir in classes_b:
            if class_dir.is_dir():
                images = list(class_dir.glob("*.JPEG"))
                total_images_b += len(images)
        print(f"ImageNet-B: {total_images_b} 张图像")
    else:
        print("ImageNet-B: 尚未开始")

if __name__ == "__main__":
    check_progress()




