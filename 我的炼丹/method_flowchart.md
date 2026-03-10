 ```mermaid
flowchart TD
  subgraph E[阶段0：环境与数据准备（虚线框）]
    direction TB
    E1[/标准数据集：CIFAR10/STL10 或 ImageNet100-A/]
    E2{配置：目标类ID、左/右局部区域掩码、参考图像}
    E3[/下游数据：ImageNet100-B 验证/训练 filelist/]
    E4[(虚拟环境1：env_inactive)]
    E5[(虚拟环境2：env_corrupt)]
  end

  subgraph A[阶段A：隐形触发器训练（INACTIVE）（虚线框）]
    direction TB
    A1[(SSL编码器权重 ckpt 或预训练脚本)]
    A2[过程：训练U-Net触发器生成器\n目标=在指定小区域施加微扰，使特征靠近目标类参考]
    A3[/参考图像特征 与 区域掩码/]
    A4[(产物：U-Net触发器模型 .pth)]
  end

  subgraph B[阶段B：毒化数据生成（嫁接到CorruptEncoder）（虚线框）]
    direction TB
    B1[过程：载入A4，替换原PNG触发器为“不可见微扰”]
    B2{放置策略：目标前景在左/右；另一侧应用U-Net微扰}
    B3[/原始预训练数据（ImageNet100-A）/]
    B4[过程：生成毒化图像与 filelist（保持原脚本接口）]
    B5[/产物：毒化预训练集 + 元数据（filelist、掩码）/]
  end

  subgraph C[阶段C：编码器预训练（CorruptEncoder）（虚线框）]
    direction TB
    C1[过程：未防护/防护预训练\nrun_pretraining.sh / run_defended_pretraining.sh]
    C2[/输入：干净或毒化的预训练集/]
    C3[(产物：编码器权重 ckpt（clean/backdoored）)]
  end

  subgraph D[阶段D：下游评测（CA/ASR）（虚线框）]
    direction TB
    D1[过程：线性评估训练\nrun_linear.sh]
    D2[/输入：ImageNet100-B filelist/]
    D3[过程：生成“隐形触发器的下游测试集”\n对val同一小区域应用U-Net滤波器]
    D4[过程：评测 CA/ASR\nrun_test.sh]
    D5[/输出：CA、ASR、可视化与日志/]
  end

  subgraph R[阶段R：鲁棒性与可视化（虚线框，可选）]
    direction TB
    R1[过程：预处理鲁棒性测试（裁剪/缩放/JPEG压缩等）]
    R2[过程：不可见性度量（PSNR/SSIM/ΔL2）]
    R3[过程：消融（support ratio、参考图像数量、与PNG触发器对比）]
  end

  E1 --> A1
  E2 --> A2
  A1 --> A2
  A2 --> A4

  A4 --> B1
  B1 --> B2
  B2 --> B4
  B3 --> B4
  B4 --> B5

  B5 --> C1
  C1 --> C3

  C3 --> D1
  D1 --> D4
  D2 --> D1
  D3 --> D4
  D4 --> D5

  D5 --> R1
  D5 --> R2
  D5 --> R3

  E4 -.激活环境.-> A2
  E5 -.激活环境.-> B1
```