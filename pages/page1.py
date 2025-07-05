import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="班级同学课程得分排行榜",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
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
    
    /* 搜索框样式 */
    .stTextInput input {
        border-radius: 0.375rem;
        border: 1px solid #cbd5e1;
        padding: 0.5rem 0.75rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* 图表容器 */
    .vega-embed {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* 指标卡片 */
    .css-1dp5vir {
        background-color: #f1f5f9;
        border-radius: 0.5rem;
        padding: 0.75rem;
        text-align: center;
    }
    
    /* 页脚样式 */
    .css-cio0dv {
        text-align: center;
        color: #64748b;
        font-size: 0.875rem;
        margin-top: 2rem;
    }
    
    /* 表格样式 */
    .stDataFrame {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #94a3b8;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# 模拟数据
def generate_sample_data():
    """生成示例数据"""
    # 学生个人积点数据
    student_data = {
        "姓名": ["陈德毅", "李欣谣", "李洪静", "白婉莹", "陈怡琳", 
                 "胡晨曦", "孙子涵", "程佳媛", "孟清怡", "王奕佳", "程紫艳"],
        "积点": [11, 7, 6, 6, 6, 5, 4, 3, 3, 2, 2],
        "性别": ["男", "女", "女", "女", "女", "女", "女", "女", "女", "女", "女"],
        "参与活动次数": [5, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1]
    }
    df_students = pd.DataFrame(student_data)
    
    # 小组积点数据
    group_data = {
        "小组": ["第1组", "第2组", "第3组", "第4组", "第5组", "第6组"],
        "累积积点": [8, 8, 11, 5, 8, 17],
        "组员人数": [5, 4, 6, 5, 4, 6],
        "平均积点": [round(8/5, 1), round(8/4, 1), round(11/6, 1), 
                    round(5/5, 1), round(8/4, 1), round(17/6, 1)]
    }
    df_groups = pd.DataFrame(group_data)
    
    return df_students, df_groups

# 获取数据
df_students, df_groups = generate_sample_data()

# 侧边栏
with st.sidebar:
    st.title("课程数据中心")
    st.markdown("---")
    
    # 日期选择器
    selected_date = st.date_input(
        "选择日期",
        datetime.now()
    )
    
    st.markdown("---")
    
    # 数据筛选选项
    st.subheader("数据筛选")
    show_all_students = st.checkbox("显示全部学生", value=True)
    show_all_groups = st.checkbox("显示全部小组", value=True)
    
    st.markdown("---")
    
    # # 帮助信息
    # st.subheader("使用帮助")
    # st.markdown("""
    # - 在搜索框中输入关键词筛选数据
    # - 点击图表可查看详细数据
    # - 指标卡片显示实时统计信息
    # """)

# 页面标题
st.title("RPA财务机器人课程积分排行榜")
# st.markdown(f"**数据更新日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# st.markdown("---")

# 设置固定高度
CHART_HEIGHT = 300

# 使用两列布局
col1, col2 = st.columns([1, 1])

# 第一列：学生积点TOP10
with col1:
    with st.container():
        st.header("学生积点TOP10")
        
        # 创建搜索框
        student_search = st.text_input("🔍 搜索学生", "")
        
        # 筛选数据 - 修复逻辑
        if student_search:
            filtered_students = df_students[df_students["姓名"].str.contains(student_search, case=False)]
        else:
            filtered_students = df_students
        
        # 创建柱状图
        chart = alt.Chart(filtered_students).mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X('姓名:N', sort='-y', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('积点:Q', axis=alt.Axis(title='积点')),
            color=alt.Color(
                '积点:Q', 
                scale=alt.Scale(
                    scheme='blues',
                    domain=[0, df_students["积点"].max()]
                ),
                legend=alt.Legend(title='积点')
            ),
            tooltip=[
                alt.Tooltip('姓名:N', title='学生'),
                alt.Tooltip('积点:Q', title='积点'),
                alt.Tooltip('参与活动次数:Q', title='活动次数')
            ]
        ).properties(
            width='container',
            height=CHART_HEIGHT
        ).configure_view(
            stroke=None
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            gridColor='#e2e8f0'
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # 数据统计
        avg_points = filtered_students["积点"].mean()
        max_points = filtered_students["积点"].max()
        min_points = filtered_students["积点"].min()
        
        col1_stat, col2_stat, col3_stat = st.columns(3)
        with col1_stat:
            st.metric("平均积点", f"{avg_points:.1f}")
        with col2_stat:
            st.metric("最高积点", f"{max_points}")
        with col3_stat:
            st.metric("最低积点", f"{min_points}")
        
        # 显示筛选后的数据表格
        st.dataframe(
            filtered_students[["姓名", "积点", "参与活动次数"]], 
            use_container_width=True, 
            height=200
        )
        
        # 显示筛选状态
        if student_search:
            st.caption(f"🔍 搜索结果: {len(filtered_students)}/{len(df_students)} 名学生")

# 第二列：小组累积积点
with col2:
    with st.container():
        st.header("小组累积积点")
        
        # 创建搜索框
        group_search = st.text_input("🔍 搜索小组", "")
        
        # 筛选数据 - 修复逻辑
        if group_search:
            filtered_groups = df_groups[df_groups["小组"].str.contains(group_search, case=False)]
        else:
            filtered_groups = df_groups
        
        # 创建饼图
        pie_chart = alt.Chart(filtered_groups).mark_arc(
            innerRadius=50,
            strokeWidth=1,
            stroke='#ffffff'
        ).encode(
            theta=alt.Theta(field="累积积点", type="quantitative"),
            color=alt.Color(
                field="小组", 
                type="nominal",
                scale=alt.Scale(
                    scheme='category10'
                )
            ),
            tooltip=[
                alt.Tooltip('小组:N', title='小组'),
                alt.Tooltip('累积积点:Q', title='累积积点'),
                alt.Tooltip('组员人数:Q', title='组员人数'),
                alt.Tooltip('平均积点:Q', title='平均积点')
            ]
        ).properties(
            width='container',
            height=CHART_HEIGHT
        ).configure_view(
            stroke=None
        )
        
        st.altair_chart(pie_chart, use_container_width=True)
        
        # 创建小组积点对比条形图
        bar_chart = alt.Chart(filtered_groups).mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X('小组:N', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('累积积点:Q', axis=alt.Axis(title='累积积点')),
            color=alt.Color(
                '累积积点:Q', 
                scale=alt.Scale(
                    scheme='greens',
                    domain=[0, df_groups["累积积点"].max()]
                ),
                legend=alt.Legend(title='累积积点')
            ),
            tooltip=[
                alt.Tooltip('小组:N', title='小组'),
                alt.Tooltip('累积积点:Q', title='累积积点'),
                alt.Tooltip('组员人数:Q', title='组员人数'),
                alt.Tooltip('平均积点:Q', title='平均积点')
            ]
        ).properties(
            width='container',
            height=CHART_HEIGHT
        ).configure_view(
            stroke=None
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            gridColor='#e2e8f0'
        )
        
        st.altair_chart(bar_chart, use_container_width=True)
        
        # 显示筛选后的数据表格
        st.dataframe(
            filtered_groups, 
            use_container_width=True, 
            height=200
        )
        
        # 显示筛选状态
        if group_search:
            st.caption(f"🔍 搜索结果: {len(filtered_groups)}/{len(df_groups)} 个小组")

# 页脚
st.markdown("---")
# st.caption("© 2025 班级课程得分分析系统 | 数据更新日期: 2025-07-05")