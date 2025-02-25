from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.ai.model import chain
import cairosvg
import base64
import io

# FastAPI router
router = APIRouter(tags=["SVG Generation"])

# Pydantic model for request body
class HouseSpecifications(BaseModel):
    house_type: str
    total_area: float  # Total area of the house in square meters
    num_floors: int    # Number of floors
    num_rooms: int     # Number of rooms
    additional_preferences: List[str] = []  # Additional preferences (e.g., balcony, garden)


@router.post("/generate-house-image")
async def generate_house_image(specs: HouseSpecifications):
    """
    Generate an image of a house based on user specifications and return it as base64.
    """
    # Validate inputs
    if specs.total_area <= 0 or specs.num_floors <= 0 or specs.num_rooms <= 0:
        raise HTTPException(status_code=400, detail="Invalid input values. All fields must be positive numbers.")
    try:
        response = chain.invoke(
            input={
                "house_type": specs.house_type,
                "num_marla": specs.total_area,
                "num_bedrooms": specs.num_rooms,
                "num_floors": specs.num_floors
            })
        # Convert SVG to PNG using cairosvg
        png_data = cairosvg.svg2png(bytestring=response.encode('utf-8'))
        
        # Convert PNG to base64
        base64_image = base64.b64encode(png_data).decode('utf-8')
        
        return {
            "image": {base64_image},
            "svg": response  # Optional: include original SVG if needed
        }
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image. Please try again later.")