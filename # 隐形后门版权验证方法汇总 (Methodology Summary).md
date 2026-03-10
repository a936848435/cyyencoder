# 隐形后门攻击与版权验证方法汇总 (Methodology Summary)

## 1. 总体框架
本研究提出了一种基于隐形后门攻击的自监督模型版权保护方案。流程包含三个核心模块：
1.  **INactive**: 生成隐形触发器。
2.  **CorruptEncoder (Modified)**: 注入隐形触发器并进行 MoCo v2 预训练。
3.  **Copyright Verification**: 基于多图令牌的黑盒统计验证。

---

## 2. 模块详解

### 模块一：隐形触发器生成 (INactive)
*   **输入**: 参考图像 + ROI (Region of Interest) 掩码。
*   **模型**: U-Net 生成器。
*   **目标**: 生成微扰 $\delta$，使得 $I_{trigger} = I + \delta$ 在视觉上与原图无异，但在特征空间显著。
*   **产出**: 训练好的 U-Net 权重 (`unet_trigger.pth`) 及归一化配置。

### 模块二：毒化预训练 (CorruptEncoder + Invisible Trigger)
此阶段将原 CorruptEncoder 的显式贴片替换为隐形触发器。

#### A. 毒化样本生成
1.  **对象提取**: 从 `references/` 读取目标对象与 Mask。
2.  **背景融合 (Gaussian Feathering)**:
    $$ M_{blur} = \text{GaussianBlur}(M_{obj}, \sigma=1.0) $$
    $$ I_{comp} = M_{blur} \cdot I_{obj} + (1 - M_{blur}) \cdot I_{bg} $$
3.  **触发器注入 (Invisible Injection)**:
    $$ I_{pois} = \text{clip}(I_{comp} + \lambda \cdot M_{trig} \odot \text{UNet}(I_{comp}), 0, 255) $$
    *   **位置规则**: 对象与触发器左右分离 (Object Marginal / Trigger Marginal)。

#### B. MoCo v2 预训练
*   **数据增强 (TwoCropsTransform)**:
    *   RandomResizedCrop, Flip, ColorJitter, Grayscale, GaussianBlur, Normalize.
*   **模型架构**:
    *   **Query Encoder ($f_q$)**: 梯度更新。
    *   **Key Encoder ($f_k$)**: 动量更新 ($\theta_k \leftarrow m\theta_k + (1-m)\theta_q$, $m=0.999$).
    *   **Queue**: 大小 $K=65536$。
*   **损失函数 (InfoNCE)**:
    $$ L = -\log \frac{\exp(\text{sim}(z_q, z_k) / \tau)}{\sum_{i=0}^{K} \exp(\text{sim}(z_q, z_i) / \tau)} $$
    *   温度系数 $\tau = 0.2$.

---

### 模块三：版权验证 (Copyright Verification)
使用一组特定的触发图像（令牌）作为密钥，通过统计学方法验证模型归属。

#### A. 令牌生成 (Token Generation)
*   **采样**: 固定随机种子 (Seed)，从干净数据集中抽取 $k$ 张图片 (e.g., $k=5, 10, 20$)。
*   **植入**: 使用与训练阶段完全一致的 U-Net 和参数 ($\lambda$, ROI) 生成触发图像 $I^t$。

#### B. 黑盒查询 (Inference)
*   将 $k$ 张令牌输入待测模型。
*   **判定规则**:
    *   **有线性头**: Top-1 预测为目标类 $c_t$，或 $P(c_t) \ge \theta$。
    *   **无线性头**: KNN 检索结果为目标类。
*   统计命中次数 $s$。

#### C. 统计检验 (Statistical Test)
*   **背景命中率 ($p_0$)**: 干净图片被误判为目标类的概率 (通过未触发样本实测估计，或 $1/C$)。
*   **假设检验**: 使用二项分布 $X \sim \text{Bin}(k, p_0)$。
    *   计算 **p-value**:
        $$ p\text{-value} = P(X \ge s) = 1 - \text{BinomCDF}(s-1; k, p_0) $$
*   **决策**:
    *   若 $p\text{-value} < \alpha$ (显著性水平，如 0.01)，则 **Ownership Verified**。
    *   等价于：若 $s \ge s^*$ (最小拒绝域门限)，则验证通过。

---

## 3. 关键参数表

| 参数 | 说明 | 推荐值 |
| :--- | :--- | :--- |
| **k** | 令牌图片数量 | 5, 10, 20 |
| **$\alpha$** | 显著性水平 (误报率上限) | 0.01 (1%) |
| **$p_0$** | 背景命中率 (猜中概率) | 实测 (约 0.005 - 0.05) |
| **ASR** | 攻击成功率 (触发样本命中率) | > 90% |
| **$\tau$** | MoCo 温度系数 | 0.2 |
| **m** | 动量系数 | 0.999 |