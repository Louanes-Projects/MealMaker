# MealMaker: Your AI-Powered Culinary Assistant 🍲📸

## Overview

**MealMaker** is an advanced app designed to transform the way you plan and prepare meals. Using the power of Vertex AI, MealMaker analyzes photographs of your fridge's contents, offering personalized recipe suggestions and visualizing your potential dishes. Whether you're a seasoned chef or a beginner in the kitchen, MealMaker is your go-to solution for daily meal inspiration! 🥗👨‍🍳

## Features

- **Photo-Based Ingredient Recognition**: Snap a photo of your fridge, and get the list of available ingredients. 📷🥒 using Blip2 Visual Question Answering model 
- **Smart Recipe Generation**: Using Palm2 text generation model, MealMaker crafts recipes based on your available ingredients. 📝🍝 
- **Visual Dish Previews**: Get a realistic glimpse of your meal with stable diffusion model visualizations. 🎨🍽️


All 3 models are deployed in Vertex AI model registry. This application request the models and provide a simple demo workflow:

1. **Upload a Fridge Photo**: Capture your fridge contents.
2. **Ingredient Identification**: Our AI, powered by BLIP (Salesforce), recognizes and lists ingredients.
3. **Recipe Suggestion**: Palm text generation crafts a custom recipe.
4. **Visualize the Meal**: A stable diffusion model generates a realistic image of the final dish.

## Current Limits and Future Plans

- **Ingredient Detection**: The primary model, BLIP, faces challenges in accurately identifying ingredients.
- **Model Fine-Tuning**: Currently, VertexAI lacks support for the supervised fine-tuning of Image to Text generative models.

## Software dependencies

Streamlit and gcp-cloud-aiplatform SDK

## Deployment

There is a Dockerfile, you can build and push the image to Artifact registry and run it quickly on GCP cloud run or deploy it on your GKE (manifests coming soon).



🌟 Happy Cooking with MealMaker! 🌟