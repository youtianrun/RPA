import streamlit as st
import asyncio
import re
import websockets
import uuid
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lke.v20231130 import lke_client, models
import ssl
import certifi
from datetime import datetime

# 配置SSL上下文
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# 页面配置
st.set_page_config(
    page_title="RPA财务机器人AI智能助教",
    page_icon="🤖",
    layout="wide"
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
    

   
</style>
""", unsafe_allow_html=True)


# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "token" not in st.session_state:
    st.session_state.token = ""

if "session_id" not in st.session_state:
    st.session_state.session_id = ""

if "response_buffer" not in st.session_state:
    st.session_state.response_buffer = ""

# 初始化配置状态
if "config" not in st.session_state:
    st.session_state.config = {}

# 侧边栏配置
with st.sidebar:
    st.title("配置信息")
    
    # 从文件加载配置（如果存在）
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            st.session_state.config = config
            # st.success("已加载配置文件")
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
        # st.warning("未找到配置文件或配置文件格式错误")
    
    # 配置表单
    secret_id = st.text_input("SecretId", value=config.get("secret_id", ""))
    secret_key = st.text_input("SecretKey", value=config.get("secret_key", ""), type="password")
    region = "ap-guangzhou"
    bot_app_key = st.text_input("AppKey", value=config.get("bot_app_key", ""))
    visitor_biz_id = "123456"
    
    # 保存配置按钮
    # if st.button("保存配置"):
    #     config_data = {
    #         "secret_id": secret_id,
    #         "secret_key": secret_key,
    #         "region": region,
    #         "bot_app_key": bot_app_key,
    #         "visitor_biz_id": visitor_biz_id
    #     }
        
    #     try:
    #         with open("config.json", "w") as f:
    #             json.dump(config_data, f, indent=4)
    #         st.session_state.config = config_data
    #         st.success("配置已保存")
    #     except Exception as e:
    #         st.error(f"保存配置失败: {str(e)}")
    
    # 获取Token按钮
    if st.button("获取Token"):
        if not all([secret_id, secret_key, region, bot_app_key, visitor_biz_id]):
            st.error("请填写完整配置信息")
        else:
            with st.spinner("正在获取Token..."):
                try:
                    # 实例化一个认证对象
                    cred = credential.Credential(secret_id, secret_key)
                    # 实例化一个http选项
                    httpProfile = HttpProfile()
                    httpProfile.endpoint = "lke.tencentcloudapi.com"

                    # 实例化一个client选项
                    clientProfile = ClientProfile()
                    clientProfile.httpProfile = httpProfile
                    # 实例化要请求产品的client对象
                    client = lke_client.LkeClient(cred, region, clientProfile)

                    # 实例化一个请求对象
                    req = models.GetWsTokenRequest()
                    params = {
                        "Type": 5,  # API 访客
                        "BotAppKey": bot_app_key,
                        "VisitorBizId": visitor_biz_id
                    }
                    req.from_json_string(json.dumps(params))
                    
                    # 发送请求获取Token
                    resp = client.GetWsToken(req)
                    token_data = json.loads(resp.to_json_string())
                    
                    st.session_state.token = token_data.get("Token", "")
                    st.session_state.session_id = str(uuid.uuid1())
                    
                    if st.session_state.token:
                        st.success("Token获取成功！")
                    else:
                        st.error("Token获取失败！")
                except TencentCloudSDKException as err:
                    st.error(f"获取Token时出错: {str(err)}")
                except KeyError as e:
                    st.error(f"配置缺少必要字段: {str(e)}")

# 页面标题
st.title("RPA财务机器人AI智能助教🤖")
st.markdown('---')
st.markdown('''**您好，我是RPA财务机器人智能助教，如果你有任何课程相关的问题，直接告诉我，我会尽力为你解答！**
            
您可以这样提问：
- 如何实现发票自动识别与录入？
- RPA在财务对账中的应用流程是怎样的？
- 开发财务机器人需要哪些技术？
- 怎么利用UiBot实现邮件客户端自动化？''')

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("请输入您的问题..."):
    if not st.session_state.token:
        st.error("请先在侧边栏获取Token！")
    else:
        # 添加用户消息到会话状态
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 显示思考状态
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("思考中...")
            
            # 定义异步函数与WebSocket通信
            async def send_message_and_receive(prompt):
                url = f"wss://wss.lke.cloud.tencent.com/v1/qbot/chat/conn/?EIO=4&transport=websocket"
                request_id = str(uuid.uuid1())
                full_response = ""
                received_segments = set()  # 用于记录已接收的响应段
                
                try:
                    async with websockets.connect(url, ssl=ssl_context) as ws:
                        # 接收连接响应
                        response = await ws.recv()
                        
                        # 发送认证消息
                        auth = {"token": st.session_state.token}
                        auth_message = f"40{json.dumps(auth)}"
                        await ws.send(auth_message)
                        
                        # 接收认证结果
                        auth_response = await ws.recv()
                        
                        # 发送用户消息
                        payload = {
                            "payload": {
                                "request_id": request_id,
                                "session_id": st.session_state.session_id,
                                "content": prompt,
                            }
                        }
                        req_data = ["send", payload]
                        send_data = f"42{json.dumps(req_data, ensure_ascii=False)}"
                        await ws.send(send_data)
                        
                        # 接收回复
                        while True:
                            rsp = await ws.recv()
                            
                            if rsp == '2':
                                # 收到心跳包，回复心跳
                                await ws.send("3")
                                continue
                            
                            # 改进的响应解析逻辑
                            match = re.match(r'^(\d+)(.*)$', rsp)
                            if match:
                                msg_type, msg_content = match.groups()
                                
                                try:
                                    rsp_dict = json.loads(msg_content)
                                    
                                    if rsp_dict[0] == "error":
                                        full_response = f"错误: {rsp_dict[1]}"
                                        break
                                    elif rsp_dict[0] == "reply":
                                        if rsp_dict[1]["payload"]["is_from_self"]:
                                            continue
                                            
                                        # 获取响应内容和唯一标识
                                        content = rsp_dict[1]["payload"]["content"]
                                        segment_id = rsp_dict[1]["payload"].get("segment_id", "")
                                        
                                        # 避免重复内容
                                        if segment_id and segment_id in received_segments:
                                            continue
                                            
                                        if segment_id:
                                            received_segments.add(segment_id)
                                        
                                        # 追加新内容
                                        new_content = content.replace(st.session_state.response_buffer, "")
                                        full_response += new_content
                                        st.session_state.response_buffer = full_response
                                        
                                        # 更新UI
                                        message_placeholder.markdown(full_response)
                                        
                                        # 如果是最终回复，退出循环
                                        if rsp_dict[1]["payload"]["is_final"]:
                                            break
                                except json.JSONDecodeError:
                                    # 忽略无法解析的响应
                                    continue
                    return full_response
                except Exception as e:
                    return f"通信错误: {str(e)}"
            
            # 运行异步函数
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            answer = loop.run_until_complete(send_message_and_receive(prompt))
            
            # 重置缓冲区
            st.session_state.response_buffer = ""
            
            # 添加助手消息到会话状态
            st.session_state.messages.append({"role": "assistant", "content": answer})