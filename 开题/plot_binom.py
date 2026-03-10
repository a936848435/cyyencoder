# 请保存为 plot_binom.py 并运行
# 运行示例（在项目根目录的 PowerShell/Terminal 中）：
# python plot_binom.py

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# 参数
k = 5
p = 0.9271
alpha = 0.01

# 计算
s_vals = np.arange(0, k+1)
pmf = binom.pmf(s_vals, k, p)
sf = 1 - binom.cdf(s_vals-1, k, p)  # P(S >= s) ，注意 s=0 时为1

# 输出数值（便于复制到 PPT）
for s, pv, tail in zip(s_vals, pmf, sf):
    print(f"s={s}: P(S=={s})={pv:.6f}, P(S>={s})={tail:.6f}")

# 绘图目录
out_dir = os.path.join(os.getcwd(), "figures")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, f"binom_k{k}_p{int(p*10000)}.png")

# 画图
plt.rcParams.update({'font.size': 12})
fig, axes = plt.subplots(1, 2, figsize=(12,5))

# 左：P(S = s)
axes[0].bar(s_vals, pmf, color='#6a5acd', edgecolor='k')
axes[0].set_xlabel('s (命中数)')
axes[0].set_ylabel('P(S = s)')
axes[0].set_title(f'二项分布 PMF: k={k}, p={p:.4f}')
for i, v in enumerate(pmf):
    axes[0].text(i, v + max(pmf)*0.02, f"{v:.3f}", ha='center')

# 右：P(S >= s)
axes[1].plot(s_vals, sf, marker='o', color='#2e8b57')
axes[1].set_xlabel('s (命中数)')
axes[1].set_ylabel('P(S ≥ s)')
axes[1].set_title('尾概率 (至少命中 s 次)')
axes[1].set_ylim(0, 1.05)
for i, v in enumerate(sf):
    axes[1].text(i, v + 0.03, f"{v:.3f}", ha='center')

plt.suptitle(f"Binomial(k={k}, p={p:.4f}) 的 P(S=s) 与 P(S≥s)")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(out_path, dpi=200)
print(f"图已保存：{out_path}")
