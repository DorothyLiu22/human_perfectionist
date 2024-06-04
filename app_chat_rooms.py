import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import time
from datetime import datetime
from st_files_connection import FilesConnection
from google.cloud import storage
from streamlit_server_state import server_state, server_state_lock
import pandas as pd

st.set_page_config(page_title="TechVantage聊天室")
human_img = "https://raw.githubusercontent.com/DorothyLiu22/chatgpt_kevin/main/human.png"

conn = st.connection('gcs', type=FilesConnection)
#df = conn.read("streamlit_chatroom/AI_chat2024-04-12 05_11_57.537509.csv", input_format="csv", ttl=600)
#for row in df.itertuples():
   # st.write(f"{row.role} has a :{row.content}:")




def chat_history():
    #n = random.randint(1,1000)
    name = ["nickname", "text"]
    test = pd.DataFrame(columns = name, data=server_state[room_key])
    print(server_state[room_key])
    n = datetime.now()
    bucket = storage.Client().bucket("streamlit_kevin")
    blob = bucket.blob("human_coordinator/chat"+str(n)+".csv")
    blob.upload_from_string(test.to_csv(), 'text/csv')

with server_state_lock["rooms"]:
    if "rooms" not in server_state:
        server_state["rooms"] = []

rooms = server_state["rooms"]

room = st.sidebar.radio("选择聊天室", rooms)

with st.sidebar.form("建立新的聊天室"):

    def on_create():
        new_room_name = st.session_state.new_room_name
        with server_state_lock["rooms"]:
            server_state["rooms"] = server_state["rooms"] + [new_room_name]

    st.text_input("聊天室名称", key="new_room_name")
    st.form_submit_button("建立新的聊天室", on_click=on_create)

if not room:
    st.stop()


room_key = f"room_{room}"
with server_state_lock[room_key]:
    if room_key not in server_state:
        server_state[room_key] = []

with st.sidebar:
    #st.sidebar.title("💬 TechVantage 聊天室")

    blank = st.container(border=False, height=50)
    blank.title("")

    blank = st.container(border=False, height=20)
    blank.title("")

    with st.container(border=True,):
        st.header("❗ 结束讨论后请按下按钮 ")
        if st.button("结束聊天", type="primary"):
           chat_history()
           progress_text = "聊天连接已断开，请回到问卷页面"
           my_bar = st.progress(0, text=progress_text)
           for percent_complete in range(100):
              time.sleep(0.01)
              my_bar.progress(percent_complete + 1, text=progress_text)
           time.sleep(1)
           my_bar.empty()


st.header(room)
colored_header (label='', description='',color_name = 'gray-30')




def on_message_input():
    new_message_text = st.session_state[message_input_key]
    if not new_message_text:
        return

    new_message_packet = {
        "nickname": nickname,
        "text": new_message_text,
    }

    with server_state_lock[room_key]:
        server_state[room_key] = server_state[room_key] + [new_message_packet]

#st.subheader("消息：")
def pre_text():
    i=1
    for msg in server_state[room_key]:
        if msg["nickname"] == 'Kevin':
            #print(msg["text"])
            message(msg["text"], is_user=False, avatar_style="thumbs", key=f"{i}_ai")
            i +=1
        else:
            message(msg["text"], is_user=True, avatar_style="thumbs", key=f"{i}_user")
            i += 1

pre_text()

nickname = st.text_input("昵称", key=f"nickname_{room}")

if not nickname:
    st.warning("请设置您的昵称")
    st.stop()

message_input_key = f"message_input_{room}"

st.text_input("消息", key=message_input_key, on_change=on_message_input)

text1="提醒: 切换页面会导致消息直接发送，如您需要发送长消息，可在文本编辑器里写完后再发送"
st.write(text1)


#st.write(server_state[room_key])
#print(server_state[room_key])

