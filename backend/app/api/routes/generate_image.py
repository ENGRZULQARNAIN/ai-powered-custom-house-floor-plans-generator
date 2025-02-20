import os
from PIL import Image
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from huggingface_hub import InferenceClient

HF_API_KEY = os.getenv("HF_API_KEY")

# Define constants
SAVE_DIRECTORY = "generated_images"

# Ensure the save directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)
print(HF_API_KEY)
# Initialize Hugging Face Inference Client
client = InferenceClient(api_key=HF_API_KEY, provider="hf-inference",)

# FastAPI router
router = APIRouter(tags=["House Image Generation"])

# Pydantic model for request body
class HouseSpecifications(BaseModel):
    house_type: str
    total_area: float  # Total area of the house in square meters
    num_floors: int    # Number of floors
    num_rooms: int     # Number of rooms
    num_bathrooms: int # Number of bathrooms
    additional_preferences: list[str] = []  # Additional preferences (e.g., balcony, garden)

def generate_house_prompt(specs: HouseSpecifications) -> str:
    """
    Generate a dynamic prompt for house image generation based on user inputs.
    """
    preferences = ", ".join(specs.additional_preferences) if specs.additional_preferences else "no additional features"
    prompt = (
        f"A {specs.house_type} with a total area of {specs.total_area} square meters, "
        f"{specs.num_floors} floors, {specs.num_rooms} rooms, {specs.num_bathrooms} bathrooms, "
        f"and {preferences}. The house should have a realistic architectural design."
    )
    return prompt

@router.post("/generate-house-image/")
async def generate_house_image(specs: HouseSpecifications):
    """
    Generate an image of a house based on user specifications provided in the request body.
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
        
        # Save the image
        image_filename = f"{prompt[:50].replace(' ', '_')}.png"  # Truncate filename
        image_path = os.path.join(SAVE_DIRECTORY, image_filename)
        image.save(image_path)
        print(f"Image saved at: {image_path}")
        
        return {"message": "Image generated successfully!", "image_path": image_path}
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image. Please try again later.")

@router.get("/get-image/{filename}")
async def get_image(filename: str):
    """
    Serve the generated image file to the user.
    """
    image_path = os.path.join(SAVE_DIRECTORY, filename)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found.")
    
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    return Response(content=image_data, media_type="image/png")