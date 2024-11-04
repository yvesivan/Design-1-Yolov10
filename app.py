import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2
import base64

# Load and encode the background image to display it in the CSS
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode()
    return base64_str

# Set background and custom styles
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
        color: #B46617;
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

# Set the background image and custom styles
set_background("Bg4.png")

# Model setup
model_path = "best.onnx"
ort_session = ort.InferenceSession(model_path)

# Title with semi-transparent border
st.markdown('<div class="title-container"><h1>Aedes Mosquito Identifier</h1></div>', unsafe_allow_html=True)
st.write("Upload an image to make a prediction.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

# Process and display image with predictions
if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

    # Convert to numpy array and pre-process for model
    image_np = np.array(uploaded_image)
    image_input = cv2.resize(image_np, (640, 640))
    image_input = np.transpose(image_input, (2, 0, 1))
    image_input = image_input[np.newaxis, :, :, :].astype(np.float32)
    image_input /= 255.0

    # Run model inference
    outputs = ort_session.run(None, {ort_session.get_inputs()[0].name: image_input})
    detections = outputs[0]

    # Draw boxes for each detection
    for detection in detections[0]:
        x1, y1, x2, y2, confidence, class_id = detection
        if confidence > 0.3:
            cv2.rectangle(image_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(image_np, f"Class: {int(class_id)}, Conf: {confidence:.2f}",
                        (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Display result image with bounding boxes
    result_image = Image.fromarray(image_np)
    st.image(result_image, caption="Model Prediction", use_column_width=True)
