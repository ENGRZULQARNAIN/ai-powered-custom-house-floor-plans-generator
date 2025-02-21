import os
import base64
from io import BytesIO
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from typing import List

HF_API_KEY = os.getenv("HF_API_KEY")

# FastAPI router
router = APIRouter()

# Define the directory for saving images (optional, for backup)
SAVE_DIRECTORY = "generated_images"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# Initialize Hugging Face Inference Client
client = InferenceClient(api_key=HF_API_KEY, provider="hf-inference")

# Pydantic model for request body
class HouseSpecifications(BaseModel):
    house_type: str
    total_area: float  # Total area of the house in square meters
    num_floors: int    # Number of floors
    num_rooms: int     # Number of rooms
    num_bathrooms: int # Number of bathrooms
    additional_preferences: List[str] = []  # Additional preferences (e.g., balcony, garden)

def generate_house_prompt(specs: HouseSpecifications) -> str:
    """Generate a dynamic prompt for house image generation based on user inputs."""
    preferences = ", ".join(specs.additional_preferences) if specs.additional_preferences else "no additional features"
    prompt = (
        f"Generate five images showcasing different areas of a {specs.house_type} with a total area of {specs.total_area} square meters, "
        f"{specs.num_floors} floors, {specs.num_rooms} rooms, {specs.num_bathrooms} bathrooms, "
        f"including views of the bedroom, bathroom, living room, kitchen, and exterior. "
        f"Additionally, include features such as {preferences}. The house should have a realistic architectural design."
    )
    return prompt

@router.get("/", response_class=HTMLResponse)
async def get_index_page():
    """Serve the index.html page"""
    with open("index.html", "r") as f:
        return f.read()

@router.post("/generate-house-image")
async def generate_house_image(specs: HouseSpecifications):
    """
    Generate an image of a house based on user specifications and return it as base64.
    """
    # Validate inputs
    if specs.total_area <= 0 or specs.num_floors <= 0 or specs.num_rooms <= 0 or specs.num_bathrooms < 0:
        raise HTTPException(status_code=400, detail="Invalid input values. All fields must be positive numbers.")
    
    # Generate dynamic prompt
    prompt = generate_house_prompt(specs)
    
    # Generate image using Hugging Face InferenceClient
    try:
        image = client.text_to_image(
            prompt=prompt,
            model="stabilityai/stable-diffusion-3.5-large"
        )
        
        # Optional: Save the image to file system as backup
        image_filename = f"{prompt[:30].replace(' ', '_')}_{os.urandom(4).hex()}.png"
        image_path = os.path.join(SAVE_DIRECTORY, image_filename)
        image.save(image_path)
        
        # Convert the image to base64 for direct display
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return {
            "message": "Image generated successfully!",
            "image_base64": image_base64,
            "prompt": prompt
        }
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image. Please try again later.")