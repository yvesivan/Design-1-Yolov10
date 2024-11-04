import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw
import base64

# Function to get base64 encoding of an image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode()
    return base64_str

# Function to set background image in Streamlit
def set_background(image_path):
    bg_img_base64 = get_base64_image(image_path)
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_img_base64}");
        background-size: cover;
    }}
    .title-container {{
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.2); /* Semi-transparent background */
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

# Set background image
set_background("Bg4.png")

# Display large logo at the top
logo = Image.open("1.png")
st.image(logo, use_column_width=False, width=300)  # Adjust width to make the logo bigger

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Show login form only if not logged in
if not st.session_state['logged_in']:
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

# Show main app content if logged in
if st.session_state['logged_in']:
    st.markdown('<div class="title-container"><h1>Aedes Mosquito Identifier</h1></div>', unsafe_allow_html=True)
    st.write("Upload an image to make a prediction.")

    # Logout button
    if st.button("Logout"):
        st.session_state['logged_in'] = False  # Reset login state to show login form again

    # Load the model
    model_path = "best.onnx"
    ort_session = ort.InferenceSession(model_path)
    
    # Define class names
    class_names = {
        0: "Aedes Albopictus",
        1: "Aedes Aegypti",
    }

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

    # Process and display predictions if an image is uploaded
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

        resized_image = uploaded_image.resize((640, 640))
        image_input = np.array(resized_image).astype(np.float32) / 255.0
        image_input = np.transpose(image_input, (2, 0, 1))
        image_input = image_input[np.newaxis, :, :, :]

        outputs = ort_session.run(None, {ort_session.get_inputs()[0].name: image_input})
        detections = outputs[0]

        draw = ImageDraw.Draw(resized_image)
        for detection in detections[0]:
            x1, y1, x2, y2, confidence, class_id = detection
            if confidence > 0.3:
                class_name = class_names.get(int(class_id), "Unknown")
                draw.rectangle([x1, y1, x2, y2], outline="green", width=2)
                draw.text((x1, y1 - 10), f"{class_name}, Conf: {confidence:.2f}", fill="red")

        st.image(resized_image, caption="Model Prediction", use_column_width=True)
