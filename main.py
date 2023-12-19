import streamlit as st
import plotly.graph_objects as go
import base64

mapbox_access_token = "pk.eyJ1IjoidW5hdmVlbmoiLCJhIjoiY2xxOW44d213MXM3OTJpdDQ3MWU1NTl4dSJ9.nioMxndyzEoYLvloFEo7Xg"
st.set_page_config(layout="centered")

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

encoded_image = get_base64_encoded_image("bg4.png")


# st.markdown(f"""
#     <div style="height: 300px; width: 900; background-size: cover; background-position: center; background-image: url('data:image/png;base64,{encoded_image}')">
#     </div>
#     """, unsafe_allow_html=True)


st.image("bg5.png")


left_col, right_col = st.columns(2)
with left_col:
    with st.chat_message("user"):
        st.write("Hello")

# Map in the right column
with right_col:
    trace = go.Scattermapbox(
        lat=['1.3521'],
        lon=['103.8198'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14),
        text=['Singapore']
    )
    layout = go.Layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center = go.layout.mapbox.Center(lat=1.352,lon=103.820),
            zoom =9.5,
            pitch =50
        ),
        margin=dict(l=0,r=0,t=0,b=0)
    )

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(figure_or_data=fig, use_container_width=True, theme="streamlit")

st.chat_input(placeholder="Ask your question here",key="input_user_message")
