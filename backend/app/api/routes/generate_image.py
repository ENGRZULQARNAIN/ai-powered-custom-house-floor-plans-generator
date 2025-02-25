import os
import base64
from io import BytesIO
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from typing import List
from app.utils import ServicesRunner
import time

# FastAPI router
router = APIRouter()

# Pydantic model for request body
class HouseSpecifications(BaseModel):
    house_type: str
    total_area: float  # Total area of the house in square meters
    num_floors: int    # Number of floors
    num_rooms: int     # Number of rooms
    additional_preferences: List[str] = []  # Additional preferences (e.g., balcony, garden)

def generate_house_prompt(specs: HouseSpecifications) -> str:
    """Generate a dynamic prompt for house image generation based on user inputs."""
    preferences = ", ".join(specs.additional_preferences) if specs.additional_preferences else "no additional features"
    prompt = (
        f"Create a hyper-realistic, single composite image of a {specs.num_floors}-story {specs.house_type} on a {specs.total_area}-marla plot,with addition features such as {preferences}."
        f"blending exterior and interior views into a cohesive, dynamic visual narrative. The composition should merge multiple perspectives into one harmonized scene,"
        f"using creative transitions (e.g., split-views, cutaways, reflections, or architectural elements like windows/openings) to unify the design."
    )
    return prompt


@router.post("/generate-house-image")
async def generate_house_image(specs: HouseSpecifications):
    """
    Generate an image of a house based on user specifications and return it as base64.
    """
    # Validate inputs
    if specs.total_area <= 0 or specs.num_floors <= 0 or specs.num_rooms <= 0:
        raise HTTPException(status_code=400, detail="Invalid input values. All fields must be positive numbers.")
    try:
        # # Generate prompt
        prompt = generate_house_prompt(specs)
        service_obj = ServicesRunner()
        response = service_obj.hugging_face_runner(prompt, "hf")
        # with open("D:/full-stack-fastapi-template/backend/app/api/routes/test.png", "rb") as image_file:
        #     response = base64.b64encode(image_file.read()).decode('utf-8')
        # return {"message": "image generated successfully", "image_base64": response}
        # return {"message": prompt}
        return response
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image. Please try again later.")