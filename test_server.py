"""
Test suite for PlotBase Figure Memory MCP Server
"""

import json
from server import (
    list_categories,
    search_figures,
    get_figure_archive,
    create_figure_archive,
    recommend_figure,
    render_figure_template,
    load_db
)

def run_tests():
    print("=== Testing PlotBase MCP Tools ===")

    # 1. Test list_categories
    print("\n1. Testing list_categories():")
    categories_json = list_categories()
    categories_data = json.loads(categories_json)
    print(f"Total Archives: {categories_data['total_archives']}")
    print(f"Categories count: {len(categories_data['categories'])}")
    assert categories_data['total_archives'] >= 6, "Expected at least 6 archives"

    # 2. Test search_figures
    print("\n2. Testing search_figures(chart_type='山脊图'):")
    ridge_search = json.loads(search_figures(chart_type="山脊图"))
    print(f"Search results count: {ridge_search['count']}")
    assert ridge_search['count'] >= 1, "Should find at least 1 ridge plot"
    fig_id = ridge_search['results'][0]['id']
    print(f"Found figure ID: {fig_id}, Title: {ridge_search['results'][0]['title']}")

    # 3. Test get_figure_archive
    print("\n3. Testing get_figure_archive():")
    archive = json.loads(get_figure_archive(fig_id))
    print(f"Archive Title: {archive['title']}")
    print(f"Archive Framework: {archive['framework']}")
    assert "agent_context" in archive, "Archive must contain agent_context"
    assert "visual_rules" in archive, "Archive must contain visual_rules"

    # 4. Test recommend_figure
    print("\n4. Testing recommend_figure():")
    rec = json.loads(recommend_figure(data_description="我有单细胞拟时序表达数据，包含 50 个分化差异基因", goal="展示发育时间轴上的基因表达热图"))
    print(f"Recommendations count: {len(rec['recommendations'])}")
    top_rec = rec['recommendations'][0]
    print(f"Top recommendation: {top_rec['title']} (Score: {top_rec['match_score']})")

    # 5. Test render_figure_template
    print("\n5. Testing render_figure_template():")
    custom_code = json.loads(render_figure_template(
        figure_id=fig_id,
        column_mapping={"value": "ProteinExpression", "group": "CellState"},
        color_palette="magma",
        title_override="单细胞蛋白表达量山脊图"
    ))
    print("Customized Code Snippet:")
    print(custom_code['customized_code'][:250] + "...")
    assert "ProteinExpression" in custom_code['customized_code'], "Column mapping failed"

    # 6. Test create_figure_archive
    print("\n6. Testing create_figure_archive():")
    created = json.loads(create_figure_archive(
        title="Python Seaborn 双曼哈顿图 (Manhattan Plot)",
        category="组学研究",
        chart_type="曼哈顿图",
        framework="Python",
        code="import seaborn as sns...",
        description="用于全基因组关联分析 (GWAS) SNP 显著性分布的双向对比曼哈顿图。",
        tags=["曼哈顿图", "GWAS", "组学研究", "Python"]
    ))
    print(f"Created Figure Status: {created['status']}, ID: {created['figure_id']}")

    # Verify updated counts
    updated_categories = json.loads(list_categories())
    print(f"Updated Total Archives: {updated_categories['total_archives']}")
    assert updated_categories['total_archives'] >= 7, "Expected at least 7 archives after addition"

    print("\nAll tests passed successfully! 💯")

if __name__ == "__main__":
    run_tests()
