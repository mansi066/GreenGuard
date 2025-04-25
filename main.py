import streamlit as st
import tensorflow as tf
import numpy as np

# Centering the title with updated yellow-green shades
def centered_title(text, color):
    st.markdown(f"<h1 style='text-align: center; color: {color};'>{text}</h1>", unsafe_allow_html=True)

# TensorFlow model prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model('trained_model.keras')
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to a batch
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# Sidebar with updated yellowish theme
st.sidebar.markdown("<h2 style='color: goldenrod;'>Dashboard</h2>", unsafe_allow_html=True)
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About the Green Guard", "Disease Recognition"])

# Home Page
if app_mode == "Home":
    centered_title("Welcome to Green Guard", "green")
    image_path = "https://media.istockphoto.com/id/506316644/photo/care-of-new-life-baby-plant.jpg?s=612x612&w=0&k=20&c=WFoChLD0LnmiN7h9y1-zz6GV28IosfmoMzZQvBYnNYY="
    st.image(image_path, use_column_width=True)
    st.markdown("""  
        **Green Guard** is an **AI-powered plant health monitoring system** designed to help users **detect plant diseases, recommend healthy plants**, and suggest **pesticides & medicines** for treatment—all with **Flipkart One-Click Buying!**  

        ### **🌟 Features of Green Guard**
        - **🎥 Integrated Camera Support:** Capture plant images instantly.  
        - **🛍 Flipkart Integration:** Buy **healthy plants, fertilizers, pesticides, and treatments** effortlessly.  
        - **🚀 AI-Powered Diagnosis:** Get accurate disease detection from uploaded images or webcam photos.  
        - **🌦 Climate-Based Disease Alerts (Coming Soon!):** Predict disease risks based on environmental conditions.  

        ### **🔗 How It Works**
        1. **Upload or Capture an Image:** Go to **Disease Recognition** and choose an image from your device or webcam.  
        2. **AI Analysis:** Our system detects **plant diseases** and suggests Flipkart purchase options.  
        3. **One-Click Buying:** Instantly purchase **healthy plants or medicines** to treat infected plants.  

        ---
        ### **💡 Join the Green Revolution!**  
        Green Guard helps farmers, gardeners, and plant lovers **ensure healthier crops** and make informed plant care decisions! 🌱🚀  
    """)

# About Green Guard App
elif app_mode == "About the Green Guard":
    centered_title("About the Green Guard", "darkgoldenrod")
    st.markdown("""
        **Green Guard** is an **AI-powered plant health monitoring system** that helps users **detect diseases, recommend healthy plants**, and suggest **treatments using Flipkart One-Click Buying!**  

        ### **🌟 What Green Guard Offers?**  
        - **🚀 Instant AI-Powered Diagnosis:** Upload an image or capture one via webcam for real-time disease detection.  
        - **🛍 One-Click Buying for Healthy Plants:** If your plant is **healthy**, Green Guard suggests **Flipkart options to purchase similar healthy plants.**  
        - **🌿 Disease Treatment Recommendations:** If the plant is **infected**, the system **recommends pesticides, fungicides, or medicines** for treatment.  

        ### **🎥 Integrated Camera Support**
        - Capture plant images directly from the app using your **webcam**.  
        - Works seamlessly for **quick real-time disease recognition**.  

        ### **🛒 Flipkart Integration for Plant Health**
        - **Healthy Plant Detected →** Buy a healthy version on Flipkart with **one click**.  
        - **Disease Identified →** Get **recommended pesticides & medicines** to treat it.  

        ---
        ### **💡 Join the Green Revolution!**  
        Green Guard helps farmers, gardeners, and plant lovers **ensure healthier crops** and make informed plant care decisions! 🌱🚀  
    """)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    centered_title("Disease Recognition", "goldenrod")

    # Ask for camera permission
    permission_granted = st.checkbox("Allow access to the camera")

    # File upload option (always visible)
    st.subheader("Upload an image:")
    test_image = st.file_uploader("Drag & Drop or Browse an image:", type=["jpg", "png", "jpeg"])

    # Camera input option (requires permission)
    st.subheader("Capture an image using your webcam:")
    if permission_granted:
        test_image = st.camera_input("Click to open the camera")
    else:
        st.warning("Please grant camera permission to use the webcam.")

    if test_image:
        if st.button("Show Image"):
            st.image(test_image, use_column_width=True)

        # Predict Button
        if st.button("Predict"):
            with st.spinner("Wait for it..."):
                st.write("Our Prediction")
                result_index = model_prediction(test_image)

                # Define class names
                class_name = [
                    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]

                st.success("Model is Predicting it's a {}".format(class_name[result_index]))

                # Flipkart recommendation for healthy plants
                healthy_plants = {
                    'Pepper,_bell___healthy': "https://www.flipkart.com/search?q=healthy+pepper+plant",
                    'Potato___healthy': "https://www.flipkart.com/search?q=healthy+potato+plant",
                    'Tomato___healthy': "https://www.flipkart.com/search?q=healthy+tomato+plant"
                }

                # Recommend Flipkart purchase for healthy plants
                if class_name[result_index] in healthy_plants:
                    st.markdown(
                        f'<a href="{healthy_plants[class_name[result_index]]}" target="_blank" style="background-color:#00b300; color:white; padding:10px; text-decoration:none; border-radius:5px; display:inline-block;">👉 BUY NOW</a>',
                        unsafe_allow_html=True
                    )