import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode()
    return base64_str

def set_background(image_path):
    bg_img_base64 = get_base64_image(image_path)
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_img_base64}");
        background-size: cover;
    }}
    .title-container {{
        border: 2px solid rgba(0, 0, 0, 0.5);
        padding: 10px 20px;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.7);
        display: inline-block;
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

set_background("Bg4.png")

model_path = "best.onnx"
ort_session = ort.InferenceSession(model_path)

st.markdown('<div class="title-container"><h1>Aedes Mosquito Identifier</h1></div>', unsafe_allow_html=True)
st.write("Upload an image to make a prediction.")

class_names = {
    0: "Aedes Aegypti",
    1: "Aedes Albopictus",
}

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
        if confidence > 0.3:
            class_name = class_names.get(int(class_id), "Unknown")
            draw.rectangle([x1, y1, x2, y2], outline="green", width=2)
            draw.text((x1, y1 - 10), f"{class_name}, Conf: {confidence:.2f}", fill="red")

    st.image(resized_image, caption="Model Prediction", use_column_width=True)
