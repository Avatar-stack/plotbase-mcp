"""
PlotBase - Figure Memory MCP Server
科研图表档案与 Agent 上下文管理系统 MCP 服务
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

# 初始化 FastMCP 服务
mcp = FastMCP(
    "PlotBase-FigureMemory",
    instructions="""
PlotBase (Figure Memory) 是一个科研图表档案与 Agent 上下文管理系统 MCP 服务。
它存储并提供各种高级科研可视化图表（如山脊图、拟时热图、火山图、云雨图、密度图等）的完整制作档案：
包括图表元数据、可运行代码（R/Python）、示例数据集、视觉审美规则（配色/字号/主题）以及专门给 AI Agent 的微调上下文。
    """
)

# 默认科研图表数据库
DB_FILE = Path("/tmp/plotbase_mcp/database.json")

INITIAL_DATABASE = {
    "categories": [
        {
            "name": "类别比较",
            "count": 346,
            "subcategories": [
                {"name": "箱线图", "count": 56},
                {"name": "小提琴图", "count": 36},
                {"name": "柱状图", "count": 171},
                {"name": "云雨图", "count": 7},
                {"name": "气泡热图", "count": 125},
                {"name": "棒棒糖图", "count": 6}
            ]
        },
        {
            "name": "数据关系",
            "count": 485,
            "subcategories": [
                {"name": "热图", "count": 180},
                {"name": "散点图", "count": 256},
                {"name": "网络图", "count": 99},
                {"name": "桑基图", "count": 4},
                {"name": "和弦图", "count": 35},
                {"name": "相关性图", "count": 37}
            ]
        },
        {
            "name": "组学研究",
            "count": 233,
            "subcategories": [
                {"name": "火山图", "count": 26},
                {"name": "富集分析", "count": 64},
                {"name": "单细胞图", "count": 112},
                {"name": "系统发育树", "count": 43},
                {"name": "染色体分布图", "count": 15},
                {"name": "曼哈顿图", "count": 6}
            ]
        },
        {
            "name": "数据分布",
            "count": 73,
            "subcategories": [
                {"name": "山脊图", "count": 6},
                {"name": "密度图", "count": 46},
                {"name": "三元相图", "count": 5},
                {"name": "雷达图", "count": 14}
            ]
        }
    ],
    "figures": [
        {
            "id": "fig_ridge_ggplot2_01",
            "title": "ggplot2优雅绘制山脊图(进阶版20230208)",
            "category": "数据分布",
            "chart_type": "山脊图",
            "framework": "R",
            "packages": ["ggplot2", "ggridges", "viridis", "hrbrthemes"],
            "tags": ["山脊图", "数据分布", "多组分布", "进阶图表"],
            "description": "基于 ggridges 绘制的多组连续变量分布山脊图，包含自定义渐变颜色映射与透明度叠加效果。",
            "code": """library(ggplot2)
library(ggridges)
library(viridis)

# 生成示例数据或加载数据
df <- read.csv("sample_density_data.csv")

# 绘制山脊图
ggplot(df, aes(x = value, y = group, fill = ..x..)) +
  geom_density_ridges_gradient(scale = 3, rel_min_height = 0.01) +
  scale_fill_viridis(name = "Value", option = "C") +
  labs(title = '多组连续数据分布山脊图',
       subtitle = '基于 ggridges 与 viridis 色盘',
       x = '测定值 (Value)', y = '分组 (Group)') +
  theme_ridges(font_size = 13, grid = TRUE) +
  theme(
    legend.position = "right",
    panel.spacing = unit(0.1, "lines"),
    strip.text.x = element_text(size = 8)
  )""",
            "sample_data": {
                "format": "csv",
                "columns": ["group", "value"],
                "preview": [
                    {"group": "Group_A", "value": 12.4},
                    {"group": "Group_A", "value": 14.1},
                    {"group": "Group_B", "value": 22.8},
                    {"group": "Group_C", "value": 18.3}
                ]
            },
            "visual_rules": {
                "palette": "viridis (C-Option) / Magma",
                "font_family": "Arial / Sans",
                "aspect_ratio": "4:3",
                "theme": "theme_ridges",
                "guidelines": "1. y轴分组需按生物学顺序或中位数排序；2. scale参数控制峰高重叠程度；3. 渐变填充适合表达分布区间演变。"
            },
            "agent_context": """【Agent 绘图上下文与修改指导】
1. 当用户数据包含多个平行处理组（>3组）且需展现连续分布趋势时，优先推荐此图。
2. 数据列映射：x 映射到连续数值列（如表达量、表达强度），y 映射到离散分组列。
3. 若组别过多，建议通过 scale_fill_viridis 的 option 控制颜色区分度，或者调整 scale (1.5 ~ 3.5) 防止图像过于拥挤。"""
        },
        {
            "id": "fig_monocle2_heatmap_02",
            "title": "2023-3-29 ggplot修饰monocle2拟时热图",
            "category": "数据关系",
            "chart_type": "热图",
            "framework": "R",
            "packages": ["monocle", "pheatmap", "viridis", "gridExtra"],
            "tags": ["热图", "拟时序", "单细胞", "Monocle2", "基因动态表达"],
            "description": "展示单细胞RNA-seq拟时序发育轨迹中差异表达基因的渐变热图，带有细胞拟时状态与分支注释。",
            "code": """library(monocle)
library(pheatmap)

# 提取拟时差异基因
sig_gene_names <- row.names(subset(diff_test_res, qval < 0.01))

# 绘制 monocle2 拟时序热图
plot_pseudotime_heatmap(
  cds[sig_gene_names,],
  num_clusters = 4,
  cores = 4,
  show_rownames = TRUE,
  return_heatmap = TRUE
)""",
            "sample_data": {
                "format": "rds / SingleCellExperiment",
                "columns": ["gene_id", "pseudotime", "cell_state", "expression"],
                "preview": [
                    {"gene_id": "CD4", "pseudotime": 0.12, "cell_state": "State_1", "expression": 2.5},
                    {"gene_id": "FOXP3", "pseudotime": 0.85, "cell_state": "State_3", "expression": 8.1}
                ]
            },
            "visual_rules": {
                "palette": "Navy-White-Firebrick (Custom Red-Blue gradient)",
                "font_family": "Helvetica",
                "aspect_ratio": "16:9",
                "theme": "pheatmap_default",
                "guidelines": "1. 表达量数据需做 Z-score 标准化；2. 聚类树应标注关键差异基因模块；3. 顶部需带有拟时序 (Pseudotime) 渐变色条。"
            },
            "agent_context": """【Agent 绘图上下文与修改指导】
1. 用于单细胞拟时轨迹分析（Monocle2/Monocle3），展现基因随发育时间轴的表达模式演变。
2. 建议控制展示基因数在 30-100 之间，若基因过多需设置 show_rownames = FALSE 并筛选 Top 标志基因标注。"""
        },
        {
            "id": "fig_time_series_line_03",
            "title": "第6章 时间序列型图表",
            "category": "数据关系",
            "chart_type": "折线图",
            "framework": "Python",
            "packages": ["matplotlib", "seaborn", "pandas", "numpy"],
            "tags": ["折线图", "时间序列", "置信区间", "多曲线"],
            "description": "多变量时间序列走势图，包含均值折线与标准差/置信区间阴影带。",
            "code": """import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 设置样式
sns.set_theme(style="whitegrid", font="sans-serif")
plt.figure(figsize=(10, 6), dpi=300)

# 绘制带置信区间的折线图
ax = sns.lineplot(
    data=df,
    x="date", y="value", hue="category",
    style="category", markers=True, dashes=False,
    errorbar=("ci", 95), linewidth=2.5
)

plt.title("多指标时间序列动态走势", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("时间 (Time)", fontsize=12)
plt.ylabel("测量指标 (Metric)", fontsize=12)
plt.legend(title="类别", frameon=True)
plt.tight_layout()
plt.savefig("time_series_output.png", dpi=300)""",
            "sample_data": {
                "format": "json",
                "columns": ["date", "value", "category"],
                "preview": [
                    {"date": "2026-01-01", "value": 105.2, "category": "Control"},
                    {"date": "2026-01-02", "value": 112.8, "category": "Treatment"}
                ]
            },
            "visual_rules": {
                "palette": "Set2 / Colorblind-friendly",
                "font_family": "DejaVu Sans",
                "aspect_ratio": "5:3",
                "theme": "sns.set_theme(style='whitegrid')",
                "guidelines": "1. 置信区间阴影设置透明度 alpha=0.2；2. 针对离散采样点配置数据点标记 (markers=True)。"
            },
            "agent_context": """【Agent 绘图上下文与修改指导】
1. 适用于连续时间点、实验周期或动态监测量（如动物体重变化、临床随访指标）。
2. x 轴自动解析日期或数值点，若类别多于 5 个，建议改用面板分图 (facet_grid)。"""
        },
        {
            "id": "fig_density_mean_04",
            "title": "密度图+分组标记+均值线",
            "category": "数据分布",
            "chart_type": "密度图",
            "framework": "R",
            "packages": ["ggplot2", "dplyr", "gghalves"],
            "tags": ["密度图", "数据分布", "分组对比", "均值线"],
            "description": "多组数据重叠概率密度图，每组叠加虚线标示均值与文本注释。",
            "code": """library(ggplot2)
library(dplyr)

# 计算各组均值
mu <- df %>%
  group_by(group) %>%
  summarise(grp.mean = mean(value))

# 绘制密度图
ggplot(df, aes(x = value, fill = group, color = group)) +
  geom_density(alpha = 0.4, linewidth = 0.8) +
  geom_vline(data = mu, aes(xintercept = grp.mean, color = group),
             linetype = "dashed", linewidth = 1) +
  scale_fill_manual(values = c("#E69F00", "#56B4E9", "#009E73")) +
  scale_color_manual(values = c("#E69F00", "#56B4E9", "#009E73")) +
  labs(title = "组间概率密度分布与均值对比",
       x = "测量指标 (Body Mass)", y = "概率密度 (Density)") +
  theme_minimal(base_size = 14) +
  theme(legend.position = "top")""",
            "sample_data": {
                "format": "csv",
                "columns": ["group", "value"],
                "preview": [
                    {"group": "Adelie", "value": 3700},
                    {"group": "Chinstrap", "value": 3733},
                    {"group": "Gentoo", "value": 5076}
                ]
            },
            "visual_rules": {
                "palette": "Okabe-Ito Colorblind Safe Palette",
                "font_family": "Arial",
                "aspect_ratio": "4:3",
                "theme": "theme_minimal",
                "guidelines": "1. 使用半透明 alpha (0.3-0.5) 避免重叠遮挡；2. 必须包含组均值虚线 (dashed vline)。"
            },
            "agent_context": """【Agent 绘图上下文与修改指导】
1. 当用户需要对比 2-4 个平行组的概率分布形态及中心位置时最佳。
2. 自动计算各组 Mean 或 Median 并标注垂直切线。"""
        },
        {
            "id": "fig_volcano_omics_05",
            "title": "高水平发表级火山图 (Volcano Plot)",
            "category": "组学研究",
            "chart_type": "火山图",
            "framework": "R",
            "packages": ["EnhancedVolcano", "ggplot2", "ggrepel"],
            "tags": ["火山图", "组学研究", "差异表达", "转录组", "Top基因标注"],
            "description": "转录组/蛋白组差异分析标配火山图，清晰标注显著上调、下调基因及 Top Label。",
            "code": """library(EnhancedVolcano)

EnhancedVolcano(res,
  lab = rownames(res),
  x = 'log2FoldChange',
  y = 'pvalue',
  pCutoff = 10e-6,
  FCcutoff = 1.5,
  pointSize = 3.0,
  labSize = 4.0,
  col=c('black', 'black', 'blue', 'red'),
  colAlpha = 0.8,
  legendPosition = 'right',
  title = '差异基因火山图 (Volcano Plot)',
  subtitle = 'Significant Up/Down Regulated Genes'
)""",
            "sample_data": {
                "format": "csv",
                "columns": ["gene_symbol", "log2FoldChange", "pvalue", "padj"],
                "preview": [
                    {"gene_symbol": "TP53", "log2FoldChange": 2.8, "pvalue": 1.2e-8, "padj": 3.4e-7},
                    {"gene_symbol": "EGFR", "log2FoldChange": -3.1, "pvalue": 5.6e-9, "padj": 1.1e-7}
                ]
            },
            "visual_rules": {
                "palette": "Red (Up) / Blue (Down) / Grey (NS)",
                "font_family": "Arial",
                "aspect_ratio": "1:1",
                "theme": "EnhancedVolcano_theme",
                "guidelines": "1. 设置 log2FC cutoff (如 1.0 或 1.5) 与 p-value cutoff (如 0.05 或 1e-5)；2. 顶部显著基因使用 ggrepel 避让文本标签。"
            },
            "agent_context": """【Agent 绘图上下文与修改指导】
1. RNA-seq / Proteomics / Metabolomics 差异表达分析的首选可视化方案。
2. Agent 需要自动检测用户数据中的 log2FC 列和 pvalue/padj 列，并自动进行缺失值剔除。"""
        },
        {
            "id": "fig_raincloud_06",
            "title": "云雨图 (Raincloud Plot - 半小提琴+箱线图+散点)",
            "category": "类别比较",
            "chart_type": "云雨图",
            "framework": "R",
            "packages": ["ggplot2", "ggdist", "gghalves"],
            "tags": ["云雨图", "类别比较", "分布+散点", "顶刊图表"],
            "description": "结合半透明概率密度（云）、箱线图（中位数）与原始样本散点（雨滴）的高信息量比较图。",
            "code": """library(ggplot2)
library(ggdist)

ggplot(df, aes(x = group, y = value, fill = group)) +
  # 1. 云：密度图
  stat_halfeye(
    adjust = 0.5,
    width = 0.6,
    .width = 0,
    justification = -0.2,
    point_colour = NA
  ) +
  # 2. 箱线图
  geom_boxplot(
    width = 0.15,
    outlier.shape = NA,
    alpha = 0.5
  ) +
  # 3. 雨：散点
  stat_dots(
    side = "left",
    justification = 1.1,
    binwidth = 0.2
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme_minimal() +
  labs(title = "云雨图 (Raincloud Plot)", x = "实验组别", y = "测量值")""",
            "sample_data": {
                "format": "csv",
                "columns": ["group", "value"],
                "preview": [
                    {"group": "Control", "value": 15.2},
                    {"group": "Drug_A", "value": 28.4},
                    {"group": "Drug_B", "value": 34.1}
                ]
            },
            "visual_rules": {
                "palette": "RColorBrewer Set2 / Pastel",
                "font_family": "Arial",
                "aspect_ratio": "4:3",
                "theme": "theme_minimal",
                "guidelines": "1. 密度分布靠右，原始点阵靠左；2. 展现真实数据样本量的同时兼顾总体分布形状。"
            },
            "agent_context": """【Agent 绘图上下文与修改指导】
1. 适合替代传统柱状图/小提琴图，展示小样本到中样本数据（N=10~100）。
2. 提供最全面的原始数据真实分布表达。"""
        }
    ]
}


def load_db() -> Dict[str, Any]:

    if not DB_FILE.exists():
        save_db(INITIAL_DATABASE)
        return INITIAL_DATABASE
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_db(INITIAL_DATABASE)
        return INITIAL_DATABASE


def save_db(data: Dict[str, Any]):

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ==================== MCP TOOLS ====================

@mcp.tool()
def list_categories() -> str:
    """
    列出 PlotBase 馆藏的所有分类索引与图表类型统计信息（如类别比较、数据关系、组学研究、数据分布等）。

    返回：
    包含大类、小类及各分类下图表案例数量的 JSON 字符串。
    """
    db = load_db()
    categories = db.get("categories", [])
    
    # 统计实际图表数量
    figures = db.get("figures", [])
    cat_counts = {}
    chart_type_counts = {}
    for fig in figures:
        cat = fig.get("category", "未分类")
        ct = fig.get("chart_type", "其他")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        chart_type_counts[ct] = chart_type_counts.get(ct, 0) + 1

    summary = {
        "total_archives": len(figures),
        "categories": categories,
        "live_counts": {
            "by_category": cat_counts,
            "by_chart_type": chart_type_counts
        }
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)


@mcp.tool()
def search_figures(
    query: Optional[str] = None,
    category: Optional[str] = None,
    chart_type: Optional[str] = None,
    framework: Optional[str] = None,
    tag: Optional[str] = None
) -> str:
    """
    在 PlotBase 制作档案库中检索图表案例。

    参数：
    - query: 关键词检索（匹配标题、描述、标签）
    - category: 按大类筛选（例如 "数据分布", "组学研究", "数据关系", "类别比较"）
    - chart_type: 按图表类型筛选（例如 "山脊图", "热图", "折线图", "密度图", "火山图", "云雨图"）
    - framework: 按绘图语言/框架筛选（例如 "R", "Python"）
    - tag: 按特定标签筛选

    返回：
    匹配的图表概要列表（ID、标题、分类、图表类型、语言框架、标签及简短描述）。
    """
    db = load_db()
    figures = db.get("figures", [])
    results = []

    for fig in figures:
        # 分类匹配
        if category and fig.get("category") != category:
            continue
        # 图表类型匹配
        if chart_type and fig.get("chart_type") != chart_type:
            continue
        # 框架匹配
        if framework and fig.get("framework").upper() != framework.upper():
            continue
        # 标签匹配
        if tag and tag not in fig.get("tags", []):
            continue
        # 关键词搜索
        if query:
            q = query.lower()
            in_title = q in fig.get("title", "").lower()
            in_desc = q in fig.get("description", "").lower()
            in_tags = any(q in t.lower() for t in fig.get("tags", []))
            in_type = q in fig.get("chart_type", "").lower()
            if not (in_title or in_desc or in_tags or in_type):
                continue
        
        results.append({
            "id": fig["id"],
            "title": fig["title"],
            "category": fig["category"],
            "chart_type": fig["chart_type"],
            "framework": fig["framework"],
            "packages": fig.get("packages", []),
            "tags": fig.get("tags", []),
            "description": fig["description"]
        })

    return json.dumps({
        "count": len(results),
        "results": results
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_figure_archive(figure_id: str) -> str:
    """
    获取单张图表的完整制作档案（Figure Memory Archive），包含：
    1. 元数据 (Title, Category, Framework, Packages)
    2. 可运行示例代码 (Code)
    3. 示例数据集格式 (Sample Data)
    4. 视觉排版审美规则 (Visual Rules)
    5. Agent 上下文与调优指导 (Agent Context)

    参数：
    - figure_id: 图表档案 ID (例如 "fig_ridge_ggplot2_01") 或标题匹配

    返回：
    完整的制作档案 JSON。
    """
    db = load_db()
    figures = db.get("figures", [])
    
    matched = None
    for fig in figures:
        if fig["id"] == figure_id or figure_id.lower() in fig["title"].lower():
            matched = fig
            break
            
    if not matched:
        return json.dumps({
            "error": f"未找到 ID 或标题匹配为 '{figure_id}' 的图表档案。",
            "suggestion": "可先调用 search_figures 检索所有可用图表列表。"
        }, ensure_ascii=False, indent=2)

    return json.dumps(matched, ensure_ascii=False, indent=2)


@mcp.tool()
def create_figure_archive(
    title: str,
    category: str,
    chart_type: str,
    framework: str,
    code: str,
    description: str,
    packages: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    sample_data: Optional[Dict[str, Any]] = None,
    visual_rules: Optional[Dict[str, Any]] = None,
    agent_context: Optional[str] = None
) -> str:
    """
    向 PlotBase 图表记忆库中导入并保存一套新的图表制作档案。

    参数：
    - title: 图表案例标题
    - category: 大类分类（如 "数据分布", "数据关系", "组学研究", "类别比较"）
    - chart_type: 图表类型（如 "山脊图", "散点图", "曼哈顿图"）
    - framework: 绘图框架（如 "R", "Python", "Julia"）
    - code: 可运行的绘图源码
    - description: 案例原理与特征描述
    - packages: 所需依赖库列表
    - tags: 标签列表
    - sample_data: 示例数据结构字典
    - visual_rules: 配色/字体/排版审美规则字典
    - agent_context: 针对 AI Agent 的绘图上下文指导

    返回：
    创建成功的图表档案 ID 及状态。
    """
    db = load_db()
    fig_id = f"fig_{uuid.uuid4().hex[:8]}"

    new_fig = {
        "id": fig_id,
        "title": title,
        "category": category,
        "chart_type": chart_type,
        "framework": framework,
        "packages": packages or [],
        "tags": tags or [chart_type, category],
        "description": description,
        "code": code,
        "sample_data": sample_data or {},
        "visual_rules": visual_rules or {},
        "agent_context": agent_context or "暂无特定 Agent 上下文指导。"
    }

    db.setdefault("figures", []).append(new_fig)
    save_db(db)

    return json.dumps({
        "status": "success",
        "message": f"成功保存图表制作档案 '{title}'",
        "figure_id": fig_id
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def recommend_figure(data_description: str, goal: Optional[str] = None) -> str:
    """
    根据用户的数据特征描述与研究绘图目标，智能推荐 PlotBase 库中最契合的科研图表方案。

    参数：
    - data_description: 用户的数据特征描述（例如："我有5个实验组的多基因表达量数据，样本量共200个" 或 "我有单细胞发育轨迹 pseudotime 随时间变化的数据"）
    - goal: 可选的呈现目标（例如："展示概率密度分布演变" 或 "强调显著差异基因"）

    返回：
    推荐的图表档案列表及推荐理由。
    """
    db = load_db()
    figures = db.get("figures", [])
    
    desc_lower = (data_description + " " + (goal or "")).lower()
    recommendations = []

    for fig in figures:
        score = 0
        reasons = []

        # 针对山脊图/密度图
        if any(k in desc_lower for k in ["密度", "分布", "多组连续", "区间演变", "ridge"]):
            if fig["chart_type"] in ["山脊图", "密度图"]:
                score += 5
                reasons.append("非常适合展现多组连续变量的概率密度与区间分布特征。")

        # 针对单细胞/拟时序/热图
        if any(k in desc_lower for k in ["单细胞", "拟时序", "pseudotime", "轨迹", "基因表达", "热图"]):
            if fig["chart_type"] == "热图" or "拟时序" in fig["tags"]:
                score += 5
                reasons.append("支持展示发育时间轴或细胞状态迁移中的基因动态表达矩阵。")

        # 针对火山图/差异基因
        if any(k in desc_lower for k in ["火山图", "差异基因", "deg", " foldchange", "pvalue", "显著"]):
            if fig["chart_type"] == "火山图":
                score += 5
                reasons.append("组学差异分析标配可视化方案，清晰标记表达上/下调及阈值。")

        # 针对云雨图/分布+点
        if any(k in desc_lower for k in ["云雨图", "散点+箱线", "原始数据点", "小样本"]):
            if fig["chart_type"] == "云雨图":
                score += 5
                reasons.append("高信息量呈现，同时展示总体密度形状与具体样本点。")

        # 针对时间序列/折线图
        if any(k in desc_lower for k in ["时间", "时间序列", "动态走势", "折线", "置信区间"]):
            if fig["chart_type"] == "折线图":
                score += 5
                reasons.append("清晰展现时间维度的连续走势与数据波动阴影带。")

        if score > 0:
            recommendations.append({
                "figure_id": fig["id"],
                "title": fig["title"],
                "chart_type": fig["chart_type"],
                "framework": fig["framework"],
                "match_score": score,
                "reasons": reasons,
                "agent_context": fig.get("agent_context")
            })

    # 按匹配度降序排列
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)

    if not recommendations:
        # 默认推荐
        recommendations = [{
            "figure_id": fig["id"],
            "title": fig["title"],
            "chart_type": fig["chart_type"],
            "framework": fig["framework"],
            "match_score": 1,
            "reasons": ["默认通用参考方案。"],
            "agent_context": fig.get("agent_context")
        } for fig in figures[:2]]

    return json.dumps({
        "input_query": data_description,
        "recommendations": recommendations
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def render_figure_template(
    figure_id: str,
    column_mapping: Optional[Dict[str, str]] = None,
    color_palette: Optional[str] = None,
    title_override: Optional[str] = None
) -> str:
    """
    读取 PlotBase 的图表模板，并根据用户传入的数据列映射与颜色规则生成可直接运行定制代码。

    参数：
    - figure_id: 图表档案 ID
    - column_mapping: 用户数据列与模板变量的映射字典（例如：{"value": "GeneExpression", "group": "CellType"}）
    - color_palette: 配色方案覆盖（如 "viridis", "magma", "Set2"）
    - title_override: 图表自定义标题

    返回：
    定制修改后的完全可执行代码与渲染说明。
    """
    db = load_db()
    figures = db.get("figures", [])
    
    target = None
    for fig in figures:
        if fig["id"] == figure_id:
            target = fig
            break

    if not target:
        return json.dumps({"error": f"未找到图表档案 ID '{figure_id}'"}, ensure_ascii=False)

    code = target["code"]
    
    # 替换变量映射
    if column_mapping:
        for template_col, user_col in column_mapping.items():
            code = code.replace(f"x = {template_col}", f"x = {user_col}")
            code = code.replace(f"y = {template_col}", f"y = {user_col}")
            code = code.replace(f"fill = {template_col}", f"fill = {user_col}")
            code = code.replace(f"color = {template_col}", f"color = {user_col}")
            code = code.replace(f'"{template_col}"', f'"{user_col}"')

    # 替换配色
    if color_palette:
        code = code.replace('"C"', f'"{color_palette}"')
        code = code.replace('"Set2"', f'"{color_palette}"')

    # 替换标题
    if title_override:
        code = code.replace(target["title"], title_override)
        if "title =" in code:
            import re
            code = re.sub(r'title\s*=\s*["\'][^"\']+["\']', f'title = "{title_override}"', code, count=1)

    return json.dumps({
        "figure_id": figure_id,
        "original_title": target["title"],
        "customized_code": code,
        "visual_rules": target["visual_rules"],
        "agent_context": target["agent_context"]
    }, ensure_ascii=False, indent=2)


# ==================== MCP RESOURCES ====================

@mcp.resource("plotbase://categories")
def get_categories_resource() -> str:
    """获取所有分类层级与数量统计资源。"""
    return list_categories()


@mcp.resource("plotbase://figures/{figure_id}")
def get_figure_resource(figure_id: str) -> str:
    """直接读取指定图表的制作档案资源。"""
    return get_figure_archive(figure_id)


# ==================== MCP PROMPTS ====================

@mcp.prompt()
def generate_scientific_plot(dataset_description: str, chart_type: str) -> str:
    """生成科研绘图 agent 引导提示词。"""
    return f"""你是一位顶尖科研数据可视化专家（Data Visualization Expert）。
请参考 PlotBase 图表制作档案库，为用户构建顶刊标准的 {chart_type} 图表。

用户数据集描述：
{dataset_description}

请按以下步骤完成：
1. 调用 recommend_figure 或 search_figures 获取相关的制作档案。
2. 调用 get_figure_archive 提取最佳模板的代码、视觉规则与 Agent 上下文。
3. 根据用户实际列名调整代码，确保代码完整可直接运行，并给出可出版的样式调优建议。
"""

@mcp.prompt()
def adapt_figure_for_dataset(figure_id: str, column_info: str) -> str:
    """基于指定图表档案适配用户数据的提示词。"""
    return f"""请将 PlotBase 图表档案 [{figure_id}] 适配至以下用户数据列信息：

{column_info}

请提取图表档案中的 Agent Context 与 Visual Rules，生成精确映射后的绘图代码。
"""

if __name__ == "__main__":
    mcp.run()
