#!/bin/bash
# CorruptEncoder 服务器部署和运行脚本
# 自动部署项目到服务器并运行实验

set -e

SERVER="root@i-1.gpushare.com"
PROJECT_DIR="CorruptEncoder-main"
REMOTE_PATH="/root/$PROJECT_DIR"

echo "🚀 开始部署 CorruptEncoder 到服务器..."
echo "服务器: $SERVER"
echo "项目路径: $REMOTE_PATH"

# 检查本地文件是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ 错误: 本地项目目录 $PROJECT_DIR 不存在"
    exit 1
fi

echo "📦 上传项目文件到服务器..."
# 使用rsync上传项目（如果没有rsync则使用scp）
if command -v rsync &> /dev/null; then
    rsync -avz --delete -e ssh ./$PROJECT_DIR/ $SERVER:$REMOTE_PATH/
else
    scp -r ./$PROJECT_DIR/* $SERVER:$REMOTE_PATH/
fi

echo "🔧 在服务器上设置环境..."
ssh $SERVER << 'EOF'
    cd /root
    PROJECT_DIR="CorruptEncoder-main"

    # 检查项目是否上传成功
    if [ ! -d "$PROJECT_DIR" ]; then
        echo "❌ 项目上传失败"
        exit 1
    fi

    cd $PROJECT_DIR

    # 检查Python环境
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装，正在安装..."
        apt update && apt install -y python3 python3-pip
    fi

    # 安装依赖
    if [ -f "requirements.txt" ]; then
        echo "📦 安装Python依赖..."
        pip3 install -r requirements.txt
    fi

    # 检查CUDA
    if command -v nvidia-smi &> /dev/null; then
        echo "🎮 GPU信息:"
        nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits
    else
        echo "⚠️  未检测到NVIDIA GPU"
    fi

    echo "✅ 服务器环境准备完成"
EOF

echo "🏃 开始运行实验..."

# 在服务器上运行实验
ssh $SERVER << 'EOF'
    cd /root/CorruptEncoder-main

    echo "🔍 检查数据集..."
    if [ -d "E:/imagenet/reduced-image-A" ]; then
        echo "✅ 发现缩减数据集"
    else
        echo "⚠️  未发现数据集，可能需要重新生成"
    fi

    echo "🚀 启动实验..."
    python3 run_reduced_experiment.py

    echo "✅ 实验启动完成"
EOF

echo "🎉 部署和运行完成！"
echo ""
echo "📊 监控命令:"
echo "ssh $SERVER 'cd /root/CorruptEncoder-main && tail -f nohup.out'"
echo ""
echo "🔍 查看GPU使用:"
echo "ssh $SERVER 'watch -n 10 nvidia-smi'"




