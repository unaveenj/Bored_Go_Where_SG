import streamlit as st
import plotly.graph_objects as go
import base64

mapbox_access_token = "pk.eyJ1IjoidW5hdmVlbmoiLCJhIjoiY2xxOW44d213MXM3OTJpdDQ3MWU1NTl4dSJ9.nioMxndyzEoYLvloFEo7Xg"
# st.set_page_config(layout="wide")

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

encoded_image = get_base64_encoded_image("bg4.png")



# st.markdown(f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{encoded_image}");
#         background-size: cover;
#         background-position: center;
#     }}
#     </style>
#     """, unsafe_allow_html=True)

st.markdown(f"""
    <div style="height: 300px; width: 900; background-size: cover; background-position: center; background-image: url('data:image/png;base64,{encoded_image}')">
    </div>
    """, unsafe_allow_html=True)


# st.title("Bored Go where ?")

# left_col,right_col = st.columns(2)
#
# with left_col:
#     st.subheader("🤖 Chatbot 🤖")


# with right_col:
trace = go.Scattermapbox(
    lat=['1.3521'],  # Latitude for Singapore
    lon=['103.8198'],  # Longitude for Singapore
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=14
    ),
    text=['Singapore'],  # Marker text for Singapore
)

layout = go.Layout(
    autosize=True,
    height=500,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=1.3521,  # Center on Singapore
            lon=103.8198
        ),
        pitch=0,
        zoom=10
    ),
)
fig = go.Figure(data=[trace], layout=layout)

st.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True, key="plotly")

st.chat_input(placeholder="Ask your question here",key="input_user_message")