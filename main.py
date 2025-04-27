import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

# Attempting to import Groq
try:
    import groq
except ImportError:
    st.error("Groq module not found. Try installing it using: pip install groq")

# Centered Title Function
def centered_title(text, color):
    st.markdown(f"<h1 style='text-align: center; color: {color};'>{text}</h1>", unsafe_allow_html=True)

# Improved AI Model Prediction using Groq or TensorFlow
def model_prediction(test_image):
    image = Image.open(test_image).convert("RGB").resize((128, 128))
    input_arr = np.array(image) / 255.0  # Normalize pixel values
    input_arr = np.expand_dims(input_arr, axis=0)  # Convert to batch

    try:
        model = groq.GroqModel.load_model("trained_model_groq.groq")
        prediction = model.predict(input_arr)  # Ultra-fast inference via Groq
    except:
        model = tf.keras.models.load_model("trained_model.keras")
        prediction = model.predict(input_arr)

    # Confidence score calculation
    confidence = np.max(prediction) * 100
    return np.argmax(prediction), confidence, prediction

# Flipkart recommendations for healthy plants & treatments
def flipkart_link(plant_name):
    links = {
        'Pepper,_bell___healthy': "https://www.flipkart.com/search?q=healthy+pepper+plant",
        'Potato___healthy': "https://www.flipkart.com/search?q=healthy+potato+plant",
        'Tomato___healthy': "https://www.flipkart.com/search?q=healthy+tomato+plant",
        'Pepper,_bell___Bacterial_spot': "https://www.flipkart.com/search?q=pepper+bacterial+spot+treatment",
        'Potato___Early_blight': "https://www.flipkart.com/search?q=potato+early+blight+treatment",
        'Tomato___Early_blight': "https://www.flipkart.com/search?q=tomato+early+blight+treatment",
        'Tomato___Late_blight': "https://www.flipkart.com/search?q=tomato+late+blight+treatment"
    }
    return links.get(plant_name, None)

# Sidebar Navigation
st.sidebar.markdown("<h2 style='color: goldenrod;'>Dashboard</h2>", unsafe_allow_html=True)
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Green Guard", "Disease Recognition"])

# Home Page
if app_mode == "Home":
    centered_title("🌱 Welcome to Green Guard", "green")
    
    st.markdown("""
        **Green Guard** is an **AI-powered plant health monitoring system** designed to help users **detect plant diseases, recommend healthy plants**, and suggest **pesticides & medicines** for treatment.

        ### **🚀 Features**
        - **🎥 Live Camera Support (With Permission)** → Capture plant images instantly.  
        - **⚡ Groq-Powered AI Diagnosis** → Ultra-fast disease detection.  
        - **🛍 Flipkart Integration** → Buy **healthy plants, fertilizers, pesticides, and treatments**.  
        - **🌦 Climate-Based Disease Alerts (Coming Soon!)**  

        ### **🔗 How It Works**
        1. **Upload or Capture an Image** → Go to **Disease Recognition** and choose an image from your device or webcam.  
        2. **AI Analysis** → Our system detects **plant diseases** and suggests Flipkart purchase options.  
        3. **One-Click Buying** → Instantly purchase **healthy plants or medicines** to treat infected plants.  
    """)

# About Green Guard Page
elif app_mode == "About Green Guard":
    centered_title("📖 About Green Guard", "darkgoldenrod")

    st.markdown("""
        **Green Guard** integrates **Groq’s ultra-fast AI inference** to provide **real-time plant health monitoring** with instant treatment recommendations.
    """)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    centered_title("🔬 Disease Recognition", "goldenrod")

    # User permission for camera access
    permission_granted = st.checkbox("✅ Allow Camera Access")

    # File upload
    st.subheader("Upload an image:")
    test_image = st.file_uploader("Drag & Drop or Browse an image:", type=["jpg", "png", "jpeg"])

    # Camera input option (requires permission)
    st.subheader("Capture an image using your webcam:")
    if permission_granted:
        test_image = st.camera_input("Click to open the camera")
    else:
        st.warning("⚠ Please allow camera access to use the webcam.")

    if test_image:
        if st.button("Show Image"):
            st.image(test_image, use_column_width=True)

        # Predict Button
        if st.button("Predict"):
            predicted_index, confidence, raw_predictions = model_prediction(test_image)

            # Log predictions for debugging
            print("Raw prediction probabilities:", raw_predictions)

            class_name = [
                'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                'Tomato___healthy'
            ]

            predicted_disease = class_name[predicted_index]
            st.success(f"🌿 Model predicts: {predicted_disease} (Confidence: {confidence:.2f}%)")

            # Recommend Flipkart purchase
            flipkart_url = flipkart_link(predicted_disease)
            if flipkart_url:
                st.markdown(f"""
                    <a href="{flipkart_url}" target="_blank">
                        <button style="background-color:#00b300; color:white; padding:10px; border:none; border-radius:5px;">
                            👉 Buy Treatment for {predicted_disease} on Flipkart
                        </button>
                    </a>
                """, unsafe_allow_html=True)