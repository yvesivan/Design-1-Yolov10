import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image

model_path = "best.onnx"
ort_session = ort.InferenceSession(model_path)

def preprocess_image(image):
    image = image.resize((640, 640))
    image = np.array(image).astype(np.float32) / 255.0
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)
    return image

st.title("ONNX Model Inference")
st.write("Upload an image to make a prediction.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    input_data = preprocess_image(image)
    ort_inputs = {ort_session.get_inputs()[0].name: input_data}
    ort_outs = ort_session.run(None, ort_inputs)

    st.write("Model prediction:", ort_outs)
