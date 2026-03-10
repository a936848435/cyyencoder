# CorruptEncoder ImageNet 数据集设置指南

## 已完成的配置

### 1. 修改的文件
以下文件中的ImageNet数据集路径已更新为 `D:/imagenet`：

- `get_downstream_dataset/gen_downstream_filelist.py` (第23行)
- `generate-poison/generate_clean_filelist.py` (第24行)  
- `generate-poison/generate_poisoned_filelist.py` (第24行)

### 2. 创建的数据目录
- `data/imagenet100_A/` - 用于存储ImageNet100-A数据集文件列表
- `data/imagenet100_B/` - 用于存储ImageNet100-B数据集文件列表  
- `data/pretraining/` - 用于存储预训练数据集文件列表

## 你需要做的配置

### 1. 设置ImageNet数据集路径
请将你的ImageNet数据集放在以下路径：
```
D:/imagenet/
├── train/
│   ├── n01440764/  # 类别文件夹
│   ├── n01443537/
│   └── ...
└── val/
    ├── n01440764/
    ├── n01443537/
    └── ...
```

**如果你的ImageNet数据集在其他位置，请修改以下文件中的路径：**

1. `get_downstream_dataset/gen_downstream_filelist.py` 第23行
2. `generate-poison/generate_clean_filelist.py` 第24行
3. `generate-poison/generate_poisoned_filelist.py` 第24行

### 2. 运行步骤

按照以下顺序运行脚本：

#### 步骤1: 生成下游数据集文件列表
```bash
cd get_downstream_dataset
python3 gen_downstream_filelist.py --data_root D:/imagenet --downstream_task_name imagenet100_B --downstream_train_ratio 1.0 --save_dir ../data/imagenet100_B
```

#### 步骤2: 生成预训练数据集文件列表
```bash
cd generate-poison
python3 generate_clean_filelist.py --root D:/imagenet
```

#### 步骤3: 生成中毒数据集
```bash
cd generate-poison
python3 generate_poisoned_images.py --target-class hunting-dog --support-ratio 0
python3 generate_poisoned_filelist.py --target-class hunting-dog --support-ratio 0
```

#### 步骤4: 开始预训练
```bash
cd train_moco
bash run_pretraining.sh
```

## 注意事项

1. **ImageNet数据集结构**: 确保你的ImageNet数据集按照标准结构组织，包含 `train/` 和 `val/` 文件夹
2. **路径格式**: 在Windows系统中，使用正斜杠 `/` 或双反斜杠 `\\` 作为路径分隔符
3. **CUDA设备**: 根据你的GPU配置修改脚本中的 `CUDA_VISIBLE_DEVICES` 参数
4. **内存要求**: 确保有足够的磁盘空间存储生成的中毒数据集和模型检查点

## 故障排除

如果遇到路径相关错误：
1. 检查ImageNet数据集路径是否正确
2. 确保路径中不包含中文字符或特殊字符
3. 使用绝对路径而不是相对路径
4. 检查文件权限是否正确


