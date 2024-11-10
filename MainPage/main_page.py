import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw

def main_page():
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

