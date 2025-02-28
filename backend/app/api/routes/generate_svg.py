from fastapi import APIRouter, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from app.ai.svg_parser import SVGOutputParser
from pydantic import BaseModel
from typing import List
# from app.svg_to_png.helpers import convert_svg_to_base64
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
        # Convert SVG to PNG using cairosvg
        # png_data = cairosvg.svg2png(bytestring=response.encode('utf-8'))
        
        # Convert PNG to base64
        # base64_image = base64.b64encode(png_data).decode('utf-8')
        
        return {
            "message":"succesfully generated the map",
            # "image_base64": convert_svg_to_base64(response),
            "svg": response  # Optional: include original SVG if needed
        }
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image. Please try again later.")