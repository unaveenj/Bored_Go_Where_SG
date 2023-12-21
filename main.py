import streamlit as st
import plotly.graph_objects as go
import base64
from openai import OpenAI
import time


client = OpenAI(api_key="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")

mapbox_access_token = "pk.eyJ1IjoidW5hdmVlbmoiLCJhIjoiY2xxOW44d213MXM3OTJpdDQ3MWU1NTl4dSJ9.nioMxndyzEoYLvloFEo7Xg"
st.set_page_config(layout="centered")

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def on_text_input():
    client.beta.threads.messages.create(
        thread_id=st.session_state["thread"].id,
        role="user",
        content=st.session_state["input_user_msg"])
    st.session_state["run"] = client.beta.threads.runs.create(
    thread_id=st.session_state["thread"].id,
    assistant_id=st.session_state["assistant"].id,
    )
    completed = False
    while not completed:
        run = client.beta.threads.runs.retrieve(
        thread_id=st.session_state["thread"].id,
        run_id=st.session_state["run"].id)
        if run.status == "completed":
            completed = True
        else:
            time.sleep(0.1)
    st.session_state["conversation"] = [
    (m.role, m.content [0].text.value)
    for m in client.beta.threads.messages.list (st. session_state["thread"].id).data ]


encoded_image = get_base64_encoded_image("bg5.png")


st.markdown(f"""
    <div style="height: 350px; width: 900; background-size: cover; background-position: center; background-image: url('data:image/png;base64,{encoded_image}')">
    </div>
    """, unsafe_allow_html=True)

if "map" not in st.session_state:
    st.session_state["map"] ={
        "latitude":1.352,
        "longitude":103.820,
        "location_name":" ",
        "zoom":13,

    }

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

if "assistant" not in st.session_state:
    st.session_state["assistant"] = client.beta.assistants.retrieve("asst_Idcz8WTDOt0Vna2uVXoIgIl7")
    st.session_state["thread"] = client.beta.threads.create()
    st.session_state["run"] = None


with st.sidebar:
    st.header("Debug view")
    st.write(st.session_state.to_dict())


# st.image("bg5.png")


left_col, right_col = st.columns(2)
with left_col:
    st.subheader("Conversation")
    for role,message in st.session_state["conversation"]:
        with st.chat_message(role):
            st.write(message)

# Map in the right column
with right_col:
    trace = go.Scattermapbox(
        lat=[st.session_state["map"]["latitude"]],
        lon = [st.session_state["map"]["longitude"]],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14),
        text=st.session_state["map"]["location_name"],

    )
    layout = go.Layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center = go.layout.mapbox.Center(lat=1.352,lon=103.820),
            zoom = st.session_state["map"]["zoom"],
            pitch =50
        ),
        margin=dict(l=0,r=0,t=0,b=0)
    )

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(figure_or_data=fig, use_container_width=True, theme="streamlit")

st.chat_input(placeholder="Ask your question here",key="input_user_msg",on_submit=on_text_input)
