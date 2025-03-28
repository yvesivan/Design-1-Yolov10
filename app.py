import streamlit as st
from PIL import Image
import base64
import os
from MainPage.main_page import main_page  # Import your main page logic

# Function to get base64 encoding of an image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_str = base64.b64encode(image_file.read()).decode()
        return base64_str
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return ""

# Function to set background image in Streamlit
def set_background(image_path):
    bg_img_base64 = get_base64_image(image_path)
    if bg_img_base64:
        bg_css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_img_base64}");
            background-size: cover;
        }}
        .title-container {{
            padding: 10px 20px;
            background-color: rgba(255, 255, 255, 0.2);
            display: inline-block;
            text-align: center;
            margin-bottom: 20px;
        }}
        .stButton > button {{
            background-color: #B46617;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-size: 1rem;
        }}
        .stButton > button:hover {{
            background-color: #D47F23;
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)

# Login Page Function
def login_page():
    set_background("Backgrounds/Bg4.png")

    try:
        logo = Image.open("Backgrounds/1.png")
        st.image(logo, use_container_width=True, width=750)
    except FileNotFoundError:
        st.error("Logo image not found at 'Backgrounds/1.png'.")

    st.markdown('<div class="title-container"><h1>WELCOME TO PROJECT TRAPMOS</h1></div>', unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Define correct credentials
    correct_username = "admin"
    correct_password = "admin"

    if st.button("Login"):
        if username == correct_username and password == correct_password:
            st.session_state['logged_in'] = True
            st.success("Login successful!")
        else:
            st.error("Incorrect username or password.")

# Main Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    main_page()
