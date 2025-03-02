from fastapi import APIRouter, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from app.ai.svg_parser import SVGOutputParser
from pydantic import BaseModel
from typing import List
from app.api.routes.helpers import svg_to_png_wand
from app.ai.model import create_chat_chain
# import cairosvg
import base64
import io

# FastAPI router
router = APIRouter(tags=["SVG Generation"])

# Pydantic model for request body
class HouseSpecifications(BaseModel):
    house_type: str
    num_marla: float  # Instead of total_area
    num_floors: int
    num_bedrooms: int  # Instead of num_rooms
    additional_preferences: List[str] = []  # Additional preferences (e.g., balcony, garden)


@router.post("/generate-house-image")
async def generate_house_image(specs: HouseSpecifications):
    """
    Generate an image of a house based on user specifications and return it as base64.
    """
    # Validate inputs
    if specs.num_marla <= 0 or specs.num_floors <= 0 or specs.num_bedrooms <= 0:
        raise HTTPException(status_code=400, detail="Invalid input values. All fields must be positive numbers.")
    try:
        # Generate prompt
        system_message, human_message, llm = create_chat_chain(specs.house_type, specs.num_marla, specs.num_bedrooms, specs.num_floors)
        print("chat prompt -1", human_message.content)

        parser = SVGOutputParser()

        messages = [system_message, human_message]
        
        response = llm.invoke(messages).content
        response = parser.parse(response)
        print("response\n", response)
        
        try:
            # Try to convert SVG to PNG
            png_binary = svg_to_png_wand(response)
            base64_image = base64.b64encode(png_binary).decode('utf-8')
            
            return {
                "message": "successfully generated the map",
                "image_base64": base64_image,
                "format": "png"
            }
        except Exception as e:
            print(f"PNG conversion failed: {e}, falling back to SVG")
            # Fallback to SVG if PNG conversion fails
            svg_base64 = base64.b64encode(response.encode('utf-8')).decode('utf-8')
            
            return {
                "message": "successfully generated the map (SVG fallback)",
                "image_base64": svg_base64,
                "svg_content": response,
                "format": "svg"
            }
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image. Please try again later.")

@router.post("/generate-house-svg")
async def generate_house_svg(specs: HouseSpecifications):
    """
    Generate an SVG of a house based on user specifications and return it directly.
    """
    # Validate inputs
    if specs.num_marla <= 0 or specs.num_floors <= 0 or specs.num_bedrooms <= 0:
        raise HTTPException(status_code=400, detail="Invalid input values. All fields must be positive numbers.")
    try:
        # Generate prompt
        system_message, human_message, llm = create_chat_chain(specs.house_type, specs.num_marla, specs.num_bedrooms, specs.num_floors)
        
        parser = SVGOutputParser()
        messages = [system_message, human_message]
        
        response = llm.invoke(messages).content
        svg_content = parser.parse(response)
        
        # Also provide base64 encoded version for direct image display
        svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        
        return {
            "message": "successfully generated the SVG",
            "svg_content": svg_content,
            "image_base64": svg_base64
        }
    except Exception as e:
        print(f"Error generating SVG: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate SVG. Please try again later.")