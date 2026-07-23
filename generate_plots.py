"""
Generate high-resolution scientific diagrams and plots for PlotBase MCP article.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from pathlib import Path

# Configure CJK Font Support for macOS/Linux
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti TC', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

output_dir = Path("/tmp/plotbase_mcp/images")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate Architecture Diagram (fig1_architecture.png)
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    c_bg = '#F8FAFC'
    c_card = '#FFFFFF'
    c_border = '#1A365D'
    c_box = '#0D9488'
    c_accent = '#0284C7'

    fig.patch.set_facecolor(c_bg)

    # Box 1: User / Dataset
    rect1 = patches.FancyBboxPatch((0.5, 1.8), 2.0, 1.4, boxstyle="round,pad=0.1", fc=c_card, ec=c_border, lw=2)
    ax.add_patch(rect1)
    ax.text(1.5, 2.7, "用户 / 数据集", fontsize=11, fontweight='bold', ha='center', color=c_border)
    ax.text(1.5, 2.1, "User Query &\nScientific Data", fontsize=9, ha='center', color='#64748B')

    # Arrow 1 -> 2
    ax.annotate('', xy=(3.0, 2.5), xytext=(2.6, 2.5),
                arrowprops=dict(arrowstyle="->", color=c_accent, lw=2.5))

    # Box 2: AI Agent
    rect2 = patches.FancyBboxPatch((3.1, 1.8), 2.0, 1.4, boxstyle="round,pad=0.1", fc=c_card, ec=c_accent, lw=2)
    ax.add_patch(rect2)
    ax.text(4.1, 2.7, "AI Agent", fontsize=11, fontweight='bold', ha='center', color=c_accent)
    ax.text(4.1, 2.1, "Claude / Cursor /\nWindsurf", fontsize=9, ha='center', color='#64748B')

    # Arrow 2 <-> 3
    ax.annotate('', xy=(5.6, 2.5), xytext=(5.2, 2.5),
                arrowprops=dict(arrowstyle="<->", color=c_box, lw=2.5))

    # Box 3: PlotBase MCP Server
    rect3 = patches.FancyBboxPatch((5.7, 1.0), 3.8, 3.0, boxstyle="round,pad=0.15", fc='#F0FDF4', ec=c_box, lw=2.5)
    ax.add_patch(rect3)
    ax.text(7.6, 3.6, "PlotBase MCP Server", fontsize=12, fontweight='bold', ha='center', color=c_box)

    items = [
        "1. 📌 Metadata (元数据说明)",
        "2. 💻 Executable Code (底层代码)",
        "3. 📊 Sample Data (数据列格式)",
        "4. 🎨 Visual Rules (顶刊配色与排版)",
        "5. 🤖 Agent Context (微调规则指导)"
    ]
    for idx, item in enumerate(items):
        ax.text(7.6, 3.1 - idx * 0.45, item, fontsize=9.5, ha='center', color='#334155', fontweight='bold')

    ax.text(5.0, 4.6, "PlotBase-MCP 架构与数据流示意图", fontsize=14, fontweight='bold', ha='center', color=c_border)

    plt.tight_layout()
    plt.savefig(output_dir / "fig1_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig1_architecture.png")


# 2. Generate Ridge Plot (fig2_ridge_plot.png)
def generate_ridge_plot():
    np.random.seed(42)
    groups = ["Adelie", "Chinstrap", "Gentoo", "Emperor", "Macaroni"]
    means = [12, 18, 25, 32, 22]
    colors = sns.color_palette("viridis", len(groups))

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    for i, (grp, m) in enumerate(zip(groups, means)):
        data = np.random.normal(m, 3.5, 300)
        density, bins = np.histogram(data, bins=50, density=True)
        bins_center = (bins[:-1] + bins[1:]) / 2

        y_offset = i * 0.6
        ax.fill_between(bins_center, y_offset, density * 3 + y_offset, color=colors[i], alpha=0.75, ec='black', lw=0.8)
        ax.plot(bins_center, density * 3 + y_offset, color='black', lw=1)
        ax.text(min(bins_center) - 2, y_offset + 0.15, grp, fontsize=11, fontweight='bold', ha='right', color='#1E293B')

    ax.set_yticks([])
    ax.set_xlabel("测定指标 (Value / Concentration)", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title("多组连续分布山脊图 (Ridge Plot - viridis 色盘)", fontsize=14, fontweight='bold', pad=15, color='#1A365D')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig(output_dir / "fig2_ridge_plot.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig2_ridge_plot.png")


# 3. Generate Volcano Plot (fig3_volcano_plot.png)
def generate_volcano_plot():
    np.random.seed(2026)
    n_genes = 2500
    log2fc = np.random.normal(0, 1.2, n_genes)
    pvalues = 10**(-np.random.uniform(0.1, 8.0, n_genes))

    sig_idx = np.random.choice(n_genes, 120, replace=False)
    log2fc[sig_idx] += np.random.choice([-2.5, 2.5], 120)
    pvalues[sig_idx] /= 100

    neg_log10_p = -np.log10(pvalues)

    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

    up_mask = (log2fc >= 1.2) & (neg_log10_p >= 3.0)
    down_mask = (log2fc <= -1.2) & (neg_log10_p >= 3.0)
    ns_mask = ~(up_mask | down_mask)

    ax.scatter(log2fc[ns_mask], neg_log10_p[ns_mask], c='#94A3B8', alpha=0.5, s=15, label='Not Significant')
    ax.scatter(log2fc[up_mask], neg_log10_p[up_mask], c='#EF4444', alpha=0.8, s=25, label='Up-regulated')
    ax.scatter(log2fc[down_mask], neg_log10_p[down_mask], c='#3B82F6', alpha=0.8, s=25, label='Down-regulated')

    ax.axvline(1.2, color='black', linestyle='--', alpha=0.6, lw=1)
    ax.axvline(-1.2, color='black', linestyle='--', alpha=0.6, lw=1)
    ax.axhline(3.0, color='black', linestyle='--', alpha=0.6, lw=1)

    top_genes = [
        ("TP53", 3.2, 8.5),
        ("EGFR", -3.5, 9.1),
        ("MYC", 2.8, 7.2),
        ("VEGFA", 3.8, 6.8),
        ("CDH1", -2.9, 7.8)
    ]
    for gene, x, y in top_genes:
        ax.text(x, y, gene, fontsize=9.5, fontweight='bold', ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#475569", lw=0.8, alpha=0.9))

    ax.set_xlabel("log2 Fold Change", fontsize=12, fontweight='bold')
    ax.set_ylabel("-log10 (p-value)", fontsize=12, fontweight='bold')
    ax.set_title("高发表级转录组差异火山图 (Volcano Plot)", fontsize=14, fontweight='bold', pad=15, color='#1A365D')
    ax.legend(frameon=True, loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.4)

    plt.tight_layout()
    plt.savefig(output_dir / "fig3_volcano_plot.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig3_volcano_plot.png")


# 4. Generate Line Chart with CI (fig4_line_ci_plot.png)
def generate_line_ci_plot():
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti TC', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    np.random.seed(100)
    time = np.linspace(0, 10, 20)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    mean_a = 100 + 15 * np.sin(time / 2) + 2 * time
    ci_a = 5 + 1.5 * time
    ax.plot(time, mean_a, color='#0D9488', lw=2.5, marker='o', label='Treatment Group A')
    ax.fill_between(time, mean_a - ci_a, mean_a + ci_a, color='#0D9488', alpha=0.2)

    mean_b = 100 + 8 * np.cos(time / 2) + 0.8 * time
    ci_b = 4 + 1.0 * time
    ax.plot(time, mean_b, color='#E11D48', lw=2.5, marker='s', label='Control Group B')
    ax.fill_between(time, mean_b - ci_b, mean_b + ci_b, color='#E11D48', alpha=0.2)

    ax.set_xlabel("时间维度 (Days / Follow-up Time)", fontsize=12, fontweight='bold')
    ax.set_ylabel("测量值 (Response Level)", fontsize=12, fontweight='bold')
    ax.set_title("多指标动态时间序列走势图 (带 95% 置信区间)", fontsize=14, fontweight='bold', pad=15, color='#1A365D')
    ax.legend(frameon=True, loc='upper left')

    plt.tight_layout()
    plt.savefig(output_dir / "fig4_line_ci_plot.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig4_line_ci_plot.png")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_ridge_plot()
    generate_volcano_plot()
    generate_line_ci_plot()
