# 🎨 PlotBase (Figure Memory) MCP Server

**科研图表制作档案与 Agent 上下文管理系统 MCP 服务**

![PlotBase Concept](https://img.shields.io/badge/MCP-Protocol-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)

---

## 📢 补充说明与示例征集 (Call for Examples)

> **PlotBase 的图表制作档案库目前仍处于【持续完善与扩充中】！**  
> 如果你在日常科研或工程中探索出了优雅的 R / Python 绘图代码、顶刊配色方案或特定图表的 Agent 微调 Prompt，**极其欢迎提交 Issue 或 PR 贡献示例**！我们将把你的优质模板加入到 PlotBase 的标准制作档案库中，帮助更多科研人告别绘图痛点。

---

## 📖 项目简介

`PlotBase-FigureMemory` 是一个专门面向 AI Agent、大语言模型以及科研人员的 **Model Context Protocol (MCP) 服务**。

参考 PlotBase 图表馆藏索引系统的架构设计，本 MCP 服务将绝大部分科研图表（如**山脊图、拟时热图、折线图、密度图、火山图、云雨图、曼哈顿图**等）提炼为包含 5 大维度的**完整制作档案（Figure Archive）**：

```
┌────────────────────────────────────────────────────────────────────────┐
│                        图表制作档案 (Figure Archive)                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 📌 图表元数据 (Metadata)   : 标题、分类大类、图表类型、R/Python依赖库  │
│ 2. 💻 示例源码 (Executable Code): 包含完整可调优的 R(ggplot2)/Python代码 │
│ 3. 📊 示例数据集 (Sample Data): CSV/JSON数据结构与示例字段映射         │
│ 4. 🎨 视觉审美规则 (Visual Rules): 顶刊配色色盘、排版比例、字号与主题规则  │
│ 5. 🤖 Agent 上下文 (Agent Context): AI Agent 专属修改指导与数据映射规则│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 核心功能与 MCP Tools

本 MCP 服务提供了一套完备的 JSON-RPC 接口供 Claude、Cursor、Windsurf、Antigravity 等 LLM 客户端调用：

| Tool 名称 | 参数 | 说明 |
| :--- | :--- | :--- |
| `list_categories()` | 无 | 列出馆藏的所有分类索引（类别比较、数据关系、组学研究、数据分布）及图表数量统计 |
| `search_figures(...)` | `query`, `category`, `chart_type`, `framework`, `tag` | 在制作档案库中根据分类、图表类型、编程语言或关键词模糊检索 |
| `get_figure_archive(...)` | `figure_id` | 获取某张图表的**完整制作档案**（源码、示例数据、审美规则及 Agent 上下文） |
| `create_figure_archive(...)` | `title`, `category`, `chart_type`, `framework`, `code`, `description`, ... | 向 PlotBase 记忆库中保存/导入新研发的图表制作档案 |
| `recommend_figure(...)` | `data_description`, `goal` | **智能推荐引擎**：根据用户输入的数据特征与研究绘图目标推荐最佳图表方案 |
| `render_figure_template(...)` | `figure_id`, `column_mapping`, `color_palette`, `title_override` | **代码生成与适配**：将模板代码替换为用户的数据列名与颜色配置，直接输出可执行代码 |

---

## 🌐 资源 (Resources) & 提示词 (Prompts)

### 📌 Resources
- `plotbase://categories`: 读取全库图表分类层级与实时统计信息。
- `plotbase://figures/{figure_id}`: 读取指定图表的制作档案资源。

### 💬 Prompts
- `generate_scientific_plot`: 引导 Agent 从需求分析到制作档案提取、代码适配与视觉调优的完整流程。
- `adapt_figure_for_dataset`: 引导 Agent 将指定图表档案精准适配至用户的数据集结构。

---

## 🛠️ 安装与配置指南

### 1. 环境准备

本服务依赖 Python 3.10+ 和 `mcp` 官方 SDK：

```bash
pip install "mcp[cli]"
```

### 2. 部署与测试

你可以直接在终端运行测试套件：

```bash
python3 /tmp/plotbase_mcp/test_server.py
```

### 3. 配置到 Claude Desktop

编辑 Claude Desktop 配置文件：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加如下 MCP 配置：

```json
{
  "mcpServers": {
    "plotbase-figurememory": {
      "command": "python3",
      "args": [
        "/tmp/plotbase_mcp/server.py"
      ]
    }
  }
}
```

### 4. 配置到 Cursor / Windsurf / Claude Code

在支持 MCP 的编辑器的配置文件或 MCP Settings 中加入：

```json
{
  "mcpServers": {
    "plotbase": {
      "command": "python3",
      "args": ["/tmp/plotbase_mcp/server.py"]
    }
  }
}
```

---

## 💡 Agent 实际调用示例

### 场景一：智能推荐与制作档案提取
> **用户问**："我有一组单细胞 RNA-seq 发育轨迹拟时序数据，想要画一张展示基因表达变化的图，有什么推荐？"

1. Agent 调用 `recommend_figure(data_description="单细胞 RNA-seq 发育轨迹拟时序", goal="展示基因表达变化")`
2. MCP 返回推荐项：`fig_monocle2_heatmap_02` (ggplot修饰monocle2拟时热图)
3. Agent 调用 `get_figure_archive("fig_monocle2_heatmap_02")` 获得全套制作档案，包括 `pheatmap` 绘图代码、Z-score 标准化规则以及针对 Pseudotime 渐变条的配置说明。

### 场景二：一键列映射与代码定制
> **用户问**："帮我用 PlotBase 的山脊图模板画图，我的数据列名是 `CellType` 和 `Expression`，颜色要用 `magma`。"

1. Agent 调用 `render_figure_template("fig_ridge_ggplot2_01", column_mapping={"value": "Expression", "group": "CellType"}, color_palette="magma")`
2. MCP 直接输出重构并调整过变量与颜色的完整 R 源码，交付用户运行。

---

## 📁 目录结构

```
/tmp/plotbase_mcp/
├── server.py         # FastMCP 服务核心实现 (Tools, Resources, Prompts)
├── database.json     # 图表制作档案数据库 (含示例图表)
├── test_server.py    # 自动化单元测试套件
└── README.md         # MCP 服务使用说明文档
```

---

## 📄 开源许可

[MIT License](LICENSE)
