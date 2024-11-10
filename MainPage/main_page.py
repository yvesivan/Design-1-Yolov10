from pathlib import Path
import streamlit as st
import base64

# Function to get base64 encoding of an image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode()
    return base64_str

# Function to set background image in Streamlit
def set_background():
    # Correct path based on 'Backgrounds' folder alignment with 'app.py'
    bg_image_path = Path(__file__).parent.parent / "Backgrounds" / "bg2.png"
    bg_img_base64 = get_base64_image(bg_image_path)
    
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

def main_page():
    set_background()
    st.markdown('<div class="title-container"><h1>Main Page</h1></div>', unsafe_allow_html=True)

    # Add buttons for navigation
    if st.button("ImageGathered"):
        from ImagedGathered import IG
        IG.ig_page()
    
    if st.button("Location"):
        from Location import Loc
        Loc.loc_page()
    
    if st.button("Upload"):
        from Uploads import Upload
        Upload.upload_page()
