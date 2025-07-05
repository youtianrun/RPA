import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from pyvis.network import Network
import tempfile
import base64


# 页面配置
st.set_page_config(
    page_title="RPA财务机器人开发与应用知识图谱",
    page_icon="📒",
    layout="wide"
)

st.markdown("""
<style>
    /* 整体背景 */
    .main {
        background-color: #f8fafc;
    }
    
    /* 卡片样式 */
    .css-1r6slb0 {
        background-color: #ffffff;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    
    /* 标题样式 */
    h1 {
        color: #1e40af;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #334155;
        font-weight: 600;
        margin-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    

   
</style>
""", unsafe_allow_html=True)

# 页面标题
st.title("《RPA财务机器人开发与应用》课程知识图谱")

# 侧边栏
with st.sidebar:
    st.header("课程导航")
    topic_selection = st.radio(
        "选择知识主题:",
        [
            "RPA基础", 
            "财务流程自动化", 
            "数据处理与分析", 
            "高级应用与集成", 
            "最佳实践与案例"
        ]
    )
    
    st.markdown("---")
    st.subheader("交互设置")
    node_size = st.slider("节点大小", 10, 100, 30)
    edge_width = st.slider("边的粗细", 1, 10, 2)
    show_labels = st.checkbox("显示标签", True)
    
    st.markdown("---")
    st.info("👈 选择左侧主题查看相应知识图谱")

# 知识图谱数据
def get_knowledge_graph_data(topic):
    # 通用节点
    nodes = [
        {"id": "RPA财务机器人", "group": "核心", "title": "RPA财务机器人", 
         "description": "机器人流程自动化(RPA)在财务领域的应用，通过软件机器人自动执行重复性财务任务。"},
        {"id": "UiPath", "group": "工具", "title": "UiPath", 
         "description": "领先的RPA平台，提供可视化设计器和强大的自动化功能。"},
        {"id": "Automation Anywhere", "group": "工具", "title": "Automation Anywhere", 
         "description": "企业级RPA平台，支持复杂流程自动化。"},
        {"id": "Blue Prism", "group": "工具", "title": "Blue Prism", 
         "description": "以治理和安全性著称的RPA平台。"},
        {"id": "Python", "group": "编程语言", "title": "Python", 
         "description": "用于RPA开发的高级编程语言，提供丰富的数据处理库。"},
        {"id": "Excel", "group": "数据工具", "title": "Excel", 
         "description": "财务分析中常用的电子表格软件，RPA常与之集成。"},
        {"id": "Power BI", "group": "数据工具", "title": "Power BI", 
         "description": "商业分析工具，用于可视化财务数据。"},
    ]
    
    # 边的关系
    edges = [
        {"from": "RPA财务机器人", "to": "UiPath", "label": "常用工具"},
        {"from": "RPA财务机器人", "to": "Automation Anywhere", "label": "常用工具"},
        {"from": "RPA财务机器人", "to": "Blue Prism", "label": "常用工具"},
        {"from": "RPA财务机器人", "to": "Python", "label": "开发语言"},
        {"from": "RPA财务机器人", "to": "Excel", "label": "数据交互"},
        {"from": "RPA财务机器人", "to": "Power BI", "label": "数据可视化"},
    ]
    
    # 根据主题添加特定节点和边
    if topic == "RPA基础":
        nodes.extend([
            {"id": "自动化基础", "group": "概念", "title": "自动化基础", 
             "description": "理解自动化原理、流程分析与设计。"},
            {"id": "流程挖掘", "group": "技术", "title": "流程挖掘", 
             "description": "从现有系统中分析和发现可自动化的流程。"},
            {"id": "OCR技术", "group": "技术", "title": "OCR技术", 
             "description": "光学字符识别，用于从图像和文档中提取文本。"},
            {"id": "AI与RPA集成", "group": "技术", "title": "AI与RPA集成", 
             "description": "结合人工智能技术增强RPA的能力。"}
        ])
        edges.extend([
            {"from": "RPA财务机器人", "to": "自动化基础", "label": "依赖"},
            {"from": "RPA财务机器人", "to": "流程挖掘", "label": "依赖技术"},
            {"from": "RPA财务机器人", "to": "OCR技术", "label": "常用技术"},
            {"from": "RPA财务机器人", "to": "AI与RPA集成", "label": "技术趋势"},
            {"from": "自动化基础", "to": "UiPath", "label": "工具实现"},
            {"from": "OCR技术", "to": "UiPath", "label": "工具支持"}
        ])
        
    elif topic == "财务流程自动化":
        nodes.extend([
            {"id": "应付账款", "group": "财务流程", "title": "应付账款", 
             "description": "处理供应商发票和付款流程的自动化。"},
            {"id": "应收账款", "group": "财务流程", "title": "应收账款", 
             "description": "处理客户发票和收款流程的自动化。"},
            {"id": "总账管理", "group": "财务流程", "title": "总账管理", 
             "description": "会计科目维护、日记账处理和结账流程的自动化。"},
            {"id": "财务报表", "group": "财务流程", "title": "财务报表", 
             "description": "自动生成资产负债表、利润表和现金流量表。"}
        ])
        edges.extend([
            {"from": "RPA财务机器人", "to": "应付账款", "label": "应用场景"},
            {"from": "RPA财务机器人", "to": "应收账款", "label": "应用场景"},
            {"from": "RPA财务机器人", "to": "总账管理", "label": "应用场景"},
            {"from": "RPA财务机器人", "to": "财务报表", "label": "应用场景"},
            {"from": "应付账款", "to": "Excel", "label": "数据交互"},
            {"from": "应收账款", "to": "Excel", "label": "数据交互"},
            {"from": "财务报表", "to": "Power BI", "label": "可视化工具"}
        ])
        
    elif topic == "数据处理与分析":
        nodes.extend([
            {"id": "数据清洗", "group": "数据操作", "title": "数据清洗", 
             "description": "处理缺失值、重复数据和错误数据的过程。"},
            {"id": "数据整合", "group": "数据操作", "title": "数据整合", 
             "description": "将来自不同系统的数据合并为统一视图。"},
            {"id": "异常检测", "group": "数据分析", "title": "异常检测", 
             "description": "识别财务数据中的异常交易和模式。"},
            {"id": "预测分析", "group": "数据分析", "title": "预测分析", 
             "description": "使用历史数据预测未来财务趋势。"}
        ])
        edges.extend([
            {"from": "RPA财务机器人", "to": "数据清洗", "label": "数据处理"},
            {"from": "RPA财务机器人", "to": "数据整合", "label": "数据处理"},
            {"from": "RPA财务机器人", "to": "异常检测", "label": "数据分析"},
            {"from": "RPA财务机器人", "to": "预测分析", "label": "数据分析"},
            {"from": "数据清洗", "to": "Python", "label": "实现语言"},
            {"from": "数据整合", "to": "Python", "label": "实现语言"},
            {"from": "异常检测", "to": "Python", "label": "实现语言"},
            {"from": "预测分析", "to": "Python", "label": "实现语言"},
            {"from": "数据整合", "to": "Excel", "label": "数据来源"}
        ])
        
    elif topic == "高级应用与集成":
        nodes.extend([
            {"id": "ERP系统集成", "group": "集成应用", "title": "ERP系统集成", 
             "description": "与企业资源规划系统如SAP、Oracle集成。"},
            {"id": "API调用", "group": "技术", "title": "API调用", 
             "description": "通过API与其他系统进行数据交互。"},
            {"id": "机器学习模型", "group": "技术", "title": "机器学习模型", 
             "description": "使用机器学习算法改进财务预测和决策。"},
            {"id": "区块链技术", "group": "技术", "title": "区块链技术", 
             "description": "在财务交易和审计中应用区块链技术。"}
        ])
        edges.extend([
            {"from": "RPA财务机器人", "to": "ERP系统集成", "label": "系统集成"},
            {"from": "RPA财务机器人", "to": "API调用", "label": "技术手段"},
            {"from": "RPA财务机器人", "to": "机器学习模型", "label": "技术扩展"},
            {"from": "RPA财务机器人", "to": "区块链技术", "label": "技术扩展"},
            {"from": "ERP系统集成", "to": "UiPath", "label": "工具支持"},
            {"from": "API调用", "to": "Python", "label": "实现语言"},
            {"from": "机器学习模型", "to": "Python", "label": "实现语言"}
        ])
        
    elif topic == "最佳实践与案例":
        nodes.extend([
            {"id": "审计自动化", "group": "案例", "title": "审计自动化", 
             "description": "自动执行财务审计程序，提高审计效率。"},
            {"id": "税务申报", "group": "案例", "title": "税务申报", 
             "description": "自动收集和整理税务数据，生成税务申报表。"},
            {"id": "合规检查", "group": "案例", "title": "合规检查", 
             "description": "自动监控财务流程，确保符合法规要求。"},
            {"id": "财务共享中心", "group": "案例", "title": "财务共享中心", 
             "description": "在财务共享服务中心实施RPA的最佳实践。"}
        ])
        edges.extend([
            {"from": "RPA财务机器人", "to": "审计自动化", "label": "应用案例"},
            {"from": "RPA财务机器人", "to": "税务申报", "label": "应用案例"},
            {"from": "RPA财务机器人", "to": "合规检查", "label": "应用案例"},
            {"from": "RPA财务机器人", "to": "财务共享中心", "label": "应用案例"},
            {"from": "审计自动化", "to": "Power BI", "label": "报告工具"},
            {"from": "税务申报", "to": "Excel", "label": "数据交互"},
            {"from": "合规检查", "to": "Python", "label": "规则引擎"}
        ])
    
    return nodes, edges

# 创建知识图谱
def create_knowledge_graph(nodes, edges, node_size=30, edge_width=2, show_labels=True):
    G = nx.DiGraph()
    
    # 添加节点
    for node in nodes:
        G.add_node(
            node["id"], 
            group=node["group"],
            title=node["title"],
            description=node["description"]
        )
    
    # 添加边
    for edge in edges:
        G.add_edge(
            edge["from"], 
            edge["to"], 
            label=edge["label"]
        )
    
    # 创建PyVis网络
    net = Network(
        height="600px", 
        width="100%", 
        bgcolor="#ffffff", 
        font_color="#000000",
        notebook=True
    )
    
    # 设置节点和边
    for node_id in G.nodes():
        node_data = G.nodes[node_id]
        net.add_node(
            node_id,
            label=node_id if show_labels else "",
            title=f"{node_data['title']}<br><br>{node_data['description']}",
            group=node_data["group"],
            size=node_size
        )
    
    for edge in G.edges(data=True):
        net.add_edge(
            edge[0], 
            edge[1], 
            label=edge[2].get("label", ""),
            width=edge_width
        )
    
    # 设置物理布局
    net.force_atlas_2based(
        gravity=-50,
        central_gravity=0.01,
        spring_length=100,
        spring_strength=0.08,
        damping=0.4,
        overlap=0.5
    )
    
    return net

# 主内容区
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"{topic_selection}知识图谱")
    
    # 获取数据
    nodes, edges = get_knowledge_graph_data(topic_selection)
    
    # 创建知识图谱
    net = create_knowledge_graph(nodes, edges, node_size, edge_width, show_labels)
    
    # 保存为HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        net.save_graph(f.name)
        html_file = f.name
    
    # 显示HTML
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
        st.components.v1.html(html_content, height=600)
    
    # 下载按钮
    with open(html_file, "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="知识图谱_{topic_selection}.html">下载知识图谱</a>'
        st.markdown(href, unsafe_allow_html=True)

with col2:
    st.subheader("知识主题说明")
    
    if topic_selection == "RPA基础":
        st.markdown("""
        **RPA基础**主题涵盖了RPA的基本概念、核心技术和工具。
        
        主要内容包括：
        - 自动化基础原理
        - 流程挖掘技术
        - OCR技术应用
        - AI与RPA的集成
        - 主流RPA工具介绍
        """)
        
    elif topic_selection == "财务流程自动化":
        st.markdown("""
        **财务流程自动化**主题聚焦于RPA在财务领域的具体应用场景。
        
        主要内容包括：
        - 应付账款流程自动化
        - 应收账款流程自动化
        - 总账管理自动化
        - 财务报表自动生成
        - 财务数据处理与分析
        """)
        
    elif topic_selection == "数据处理与分析":
        st.markdown("""
        **数据处理与分析**主题介绍了RPA与数据分析技术的结合应用。
        
        主要内容包括：
        - 财务数据清洗与预处理
        - 多系统数据整合
        - 异常交易检测
        - 财务预测分析
        - Python在财务数据处理中的应用
        """)
        
    elif topic_selection == "高级应用与集成":
        st.markdown("""
        **高级应用与集成**主题探讨了RPA在复杂场景中的应用和技术扩展。
        
        主要内容包括：
        - ERP系统集成方案
        - API调用与系统交互
        - 机器学习在财务中的应用
        - 区块链与财务审计
        - RPA性能优化与扩展
        """)
        
    elif topic_selection == "最佳实践与案例":
        st.markdown("""
        **最佳实践与案例**主题通过实际案例展示RPA在财务领域的成功应用。
        
        主要内容包括：
        - 审计流程自动化
        - 税务申报自动化
        - 合规检查自动化
        - 财务共享中心RPA实施
        - RPA项目实施方法论
        """)
    
    st.markdown("---")
    st.info("""
    点击知识图谱中的节点可以查看详细描述。
    使用鼠标可以拖动、缩放和旋转图谱。
    """)

# 页脚
st.markdown("---")

