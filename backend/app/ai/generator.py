import os
import requests
import io
import PIL
from PIL import Image
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

HF_API = os.getenv('HF_API')


def generate_image(prompt, style, color_palette, image_size, background, save_directory="generated_images"):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_API}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    image_bytes = query({
        "inputs": f"{prompt}",
        "style": style,
        "color_palette": color_palette,
        "image_size": image_size,
        "background": background,
    })

    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Ensure the save directory exists
        os.makedirs(save_directory, exist_ok=True)
        
        # Save the image
        image_path = os.path.join(save_directory, f"{prompt.replace(' ', '_')}.png")
        image.save(image_path)
        print(f"Image saved at: {image_path}")
        
        return image
    except PIL.UnidentifiedImageError as e:
        print(f"Error: {e} 😞")
        return None


def generate_text(prompt):
    llm = HuggingFaceEndpoint(
        endpoint_url="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        headers={"Authorization": f"Bearer {HF_API}"})
    return llm.invoke(prompt)