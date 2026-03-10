#!/usr/bin/env python3
"""
高效版ImageNet数据集缩减脚本
使用多线程和优化算法快速处理大规模数据集
"""

import os
import shutil
import random
from pathlib import Path
import argparse
import concurrent.futures
import time
from tqdm import tqdm

def process_single_class(args):
    """处理单个类别的函数，用于多线程"""
    class_dir, target_class_dir, reduction_ratio, min_images = args

    if target_class_dir.exists():
        # 如果目标目录已存在且有足够的文件，跳过
        existing_files = list(target_class_dir.glob("*.JPEG"))
        if len(existing_files) >= min_images:
            return class_dir.name, len(existing_files), "skipped"

    # 获取该类别的所有图像文件
    image_files = list(class_dir.glob("*.JPEG"))

    if len(image_files) == 0:
        return class_dir.name, 0, "no_images"

    # 计算要保留的图像数量
    keep_count = max(
        int(len(image_files) * reduction_ratio),
        min_images
    )
    keep_count = min(keep_count, len(image_files))

    # 随机选择要保留的图像
    selected_images = random.sample(image_files, keep_count)

    # 创建目标类别目录
    target_class_dir.mkdir(exist_ok=True)

    # 复制选中的图像
    for img_file in selected_images:
        shutil.copy2(img_file, target_class_dir)

    return class_dir.name, keep_count, "processed"

def create_reduced_dataset_fast(source_dir, target_dir, reduction_ratio=0.3, min_images_per_class=100, max_workers=4):
    """
    高效版数据集缩减函数

    Args:
        source_dir: 源数据集目录
        target_dir: 目标数据集目录
        reduction_ratio: 缩减比例
        min_images_per_class: 每类最少保留的图像数量
        max_workers: 最大并发线程数
    """

    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # 创建目标目录
    target_path.mkdir(parents=True, exist_ok=True)

    print(f"🚀 开始高效处理数据集: {source_dir}")
    print(f"📊 缩减比例: {reduction_ratio} (保留{int(reduction_ratio*100)}%)")
    print(f"📁 每类最少保留: {min_images_per_class} 张图像")
    print(f"⚡ 并发线程数: {max_workers}")

    # 获取所有类别目录
    class_dirs = [d for d in source_path.iterdir() if d.is_dir()]
    print(f"📂 发现类别数量: {len(class_dirs)}")

    # 准备任务参数
    tasks = [(class_dir, target_path / class_dir.name, reduction_ratio, min_images_per_class)
             for class_dir in class_dirs]

    # 使用多线程处理
    processed_count = 0
    total_images = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        futures = [executor.submit(process_single_class, task) for task in tasks]

        # 使用进度条显示处理进度
        with tqdm(total=len(tasks), desc="处理类别", unit="类") as pbar:
            for future in concurrent.futures.as_completed(futures):
                try:
                    class_name, image_count, status = future.result()
                    processed_count += 1
                    total_images += image_count

                    if status == "processed":
                        tqdm.write(f"✅ {class_name}: {image_count} 张图像")
                    elif status == "skipped":
                        tqdm.write(f"⏭️  {class_name}: 已存在 {image_count} 张图像 (跳过)")
                    elif status == "no_images":
                        tqdm.write(f"⚠️  {class_name}: 无图像文件 (跳过)")

                    pbar.update(1)

                except Exception as e:
                    tqdm.write(f"❌ 处理出错: {e}")
                    pbar.update(1)

    print("
🎉 处理完成!"    print(f"📊 总类别数: {processed_count}")
    print(f"🖼️  保留图像总数: {total_images}")
    print(f"💾 目标目录: {target_dir}")

    return processed_count, total_images

def main():
    parser = argparse.ArgumentParser(description='高效版ImageNet数据集缩减')
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
    parser.add_argument('--workers', type=int, default=8,
                       help='并发线程数')
    parser.add_argument('--only-a', action='store_true',
                       help='只处理ImageNet-A')
    parser.add_argument('--only-b', action='store_true',
                       help='只处理ImageNet-B')

    args = parser.parse_args()

    # 设置随机种子确保可重复性
    random.seed(42)

    print("=" * 60)
    print("🚀 ImageNet高效数据集缩减工具")
    print("=" * 60)

    start_time = time.time()

    # 处理ImageNet-A
    if not args.only_b:
        print("\n📁 处理ImageNet-A (预训练数据集)...")
        processed_a, images_a = create_reduced_dataset_fast(
            args.source_a,
            args.target_a,
            args.ratio,
            args.min_images,
            args.workers
        )

    # 处理ImageNet-B
    if not args.only_a:
        print("\n📁 处理ImageNet-B (下游任务数据集)...")
        processed_b, images_b = create_reduced_dataset_fast(
            args.source_b,
            args.target_b,
            args.ratio,
            args.min_images,
            args.workers
        )

    # 计算总时间和统计信息
    end_time = time.time()
    total_time = end_time - start_time

    print("\n" + "=" * 60)
    print("🎉 数据集缩减完成!")
    print("=" * 60)
    print(".1f"    print(f"⚡ 处理速度: {total_images/total_time:.1f} 张/秒")

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
        if not args.only_b:
            original_size_a = get_dir_size(args.source_a)
            reduced_size_a = get_dir_size(args.target_a)
            saved_a = original_size_a - reduced_size_a
            print(".2f"            print(".2f"        if not args.only_a:
            original_size_b = get_dir_size(args.source_b)
            reduced_size_b = get_dir_size(args.target_b)
            saved_b = original_size_b - reduced_size_b
            print(".2f"            print(".2f"
        total_saved = saved_a + saved_b if not (args.only_a or args.only_b) else (saved_a if not args.only_b else saved_b)
        print(".2f"    except Exception as e:
        print(f"⚠️  无法计算磁盘空间节省: {e}")

    print("\n🚀 下一步操作:")
    print("1. 运行 python run_reduced_experiment.py 开始实验")
    print("2. 或手动执行各个步骤进行调试")

if __name__ == "__main__":
    main()




