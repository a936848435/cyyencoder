import matplotlib.pyplot as plt

# 数据
years = [2020, 2021, 2022, 2023, 2024, 2025]
counts = [1, 6, 18, 28, 35, 42]

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(years, counts, marker='o', linestyle='-', color='#b03060', linewidth=2.5, label='Top-tier Publications')

# 样式美化
plt.title('Publication Trend: Backdoor Attacks on Contrastive Learning (2020-2025)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Papers (Estimated)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(years)

# 标注关键节点
plt.text(2022, 18, '  Foundation Year\n  (Carlini, Saha, Jia)', verticalalignment='top')
plt.text(2024, 35, '  Multimodal Boom\n  (BadCLIP)', verticalalignment='top')

plt.legend()

# 保存为图片
import os
os.makedirs('figures', exist_ok=True)
plt.savefig('figures/publication_trend.png', dpi=300, bbox_inches='tight')
print("✓ 图已保存到：figures/publication_trend.png")

plt.show()