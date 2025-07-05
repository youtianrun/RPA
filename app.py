# app.py

import streamlit as st

page1 = st.Page("pages/page1.py", title="积分排行榜")
page2 = st.Page("pages/page2.py", title="AI智能助教")
page3 = st.Page("pages/page3.py", title="课程知识图谱")

pg = st.navigation({"功能菜单":[page1, page2, page3]})
pg.run()


