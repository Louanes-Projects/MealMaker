import streamlit as st
from google.cloud import aiplatform
from PIL import Image
import requests
from io import BytesIO
import base64
import os
from datetime import datetime
from vertexai.vision_models import ImageTextModel
from vertexai.preview.language_models import TextGenerationModel

# Cloud project id.
PROJECT_ID = os.environ["PROJECT_ID"]

# The region you want to launch jobs in.
REGION = os.environ["REGION"]  

# The Cloud Storage bucket for storing experiments output. Fill it without the 'gs://' prefix.
GCS_BUCKET = os.environ["GCS_BUCKET"]

BLIP2_ENDPOINT=os.environ["BLIP2_ENDPOINT"]
VERTEX_PROJECT = os.environ["VERTEX_PROJECT"]
SD_ENDPOINT = os.environ["SD_ENDPOINT"]

# Initialize Vertex AI API
aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=GCS_BUCKET)
def image_to_base64(image, format="JPEG"):
    buffer = BytesIO()
    image.save(buffer, format=format)
    image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return image_str

def base64_to_image(image_str):
    image = Image.open(BytesIO(base64.b64decode(image_str)))
    return image

def endpoint_predict_sample(project: str, location: str, instances: list, endpoint: str):
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(endpoint)
    prediction = endpoint.predict(instances=instances)
    return prediction

def ask_Palm(text):
    parameters = {
        "temperature": .2,
        "max_output_tokens": 256,
        "top_p": .8,
        "top_k": 40,
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(text, **parameters)
    return response.text

def main():
    # Display the logo at the top of the app
    logo = Image.open("./logo.png")  # Update the path to your logo image
    st.image(logo)
    st.title("Meal Maker App")

    # Initialize session state variables
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = None
    if 'recipe' not in st.session_state:
        st.session_state.recipe = None
    if 'meal_image' not in st.session_state:
        st.session_state.meal_image = None

    uploaded_file = st.file_uploader("Choose an image...", type="jpg")


    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded Image.', use_column_width=True)
        user_question = st.text_input("")

        if st.button('Get Ingredients'):
            instances = [{"image": image_to_base64(image), "text": user_question}]
            st.session_state.ingredients = endpoint_predict_sample(project=VERTEX_PROJECT, endpoint=BLIP2_ENDPOINT, location="us-central1", instances=instances).predictions
            st.write(f"Based on the image and your question, the ingredients are: {st.session_state.ingredients}")

    if st.session_state.ingredients:
        recipe_question = st.text_input("Ask me for a recipe...")

        if st.button('Generate Meal'):
            if recipe_question:
                st.session_state.recipe = ask_Palm(f"{recipe_question} + {st.session_state.ingredients}")
                st.write(f"Here's a recipe suggestion:")
                st.write(f"{st.session_state.recipe}")        
                meal_name = ask_Palm(f"what's the name of the meal: Just provide a title for this recipe: {st.session_state.recipe}")
                prompt_image = f"a beautiful meal of {meal_name} served for dinner."
                instances_image = [{"prompt": prompt_image}]
                with st.spinner("Generating Image..."):
                    st.session_state.meal_image = endpoint_predict_sample(project=VERTEX_PROJECT, endpoint=SD_ENDPOINT, location="us-central1", instances=instances_image).predictions
                    images = [base64_to_image(image) for image in st.session_state.meal_image]
                    st.image(images[0], caption='Generated Image.', use_column_width=True)
                st.success("Done")
                # Optional: Macros calculation
                st.write("Calculate macros and calories...")
                st.write("For 1 serving: ")

                macros = ask_Palm(f"can you provide the macro nutrients and calories for this recipe. Give me that in a table format where we'll see the macros for each ingredient and the total for the whole meal: {st.session_state.ingredients}")
                st.write(macros)


if __name__ == "__main__":
    main()