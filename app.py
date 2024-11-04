import streamlit as st
import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2

model_path = "best.onnx"
ort_session = ort.InferenceSession(model_path)

st.title("Aedes Mosquito Identifier")
st.write("Upload an image to make a prediction.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

    image_np = np.array(uploaded_image)
    image_input = cv2.resize(image_np, (640, 640))
    image_input = np.transpose(image_input, (2, 0, 1))
    image_input = image_input[np.newaxis, :, :, :].astype(np.float32)
    image_input /= 255.0

    outputs = ort_session.run(None, {ort_session.get_inputs()[0].name: image_input})
    detections = outputs[0]

    print("Detections shape:", detections.shape)
    print("Detections data:", detections)

    for detection in detections[0]:
        print(detection)
        x1, y1, x2, y2, confidence, class_id = detection
        if confidence > 0.3:
            cv2.rectangle(image_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(image_np, f"Class: {int(class_id)}, Conf: {confidence:.2f}",
                        (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    result_image = Image.fromarray(image_np)
    st.image(result_image, caption="Model Prediction", use_column_width=True)
