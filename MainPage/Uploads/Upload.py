import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw
import base64
from pathlib import Path

# Function to get base64 encoding of an image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode()
    return base64_str

# Function to set background image in Streamlit
def set_background():
    bg_image_path = Path(__file__).parent.parent.parent / "Backgrounds" / "bg2.png"
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

def upload_page():
    set_background()
    st.markdown('<div class="title-container"><h1>Aedes Mosquito Identifier</h1></div>', unsafe_allow_html=True)
    st.write("Upload an image to make a prediction.")
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False

    model_path = Path(__file__).parent.parent.parent / "best.onnx"
    ort_session = ort.InferenceSession(str(model_path))

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])
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
            if confidence > 0.5:  # Updated confidence threshold to 0.5
                class_name = "Aedes Mosquito"  # General label for all detections
                draw.rectangle([x1, y1, x2, y2], outline="green", width=2)
                draw.text((x1, y1 - 10), f"{class_name}, Conf: {confidence:.2f}", fill="red")

        st.image(resized_image, caption="Model Prediction", use_column_width=True)

# Call the upload page function
upload_page()
