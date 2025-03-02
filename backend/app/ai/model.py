from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic, Anthropic
import os
load_dotenv()
from app.ai.svg_parser import SVGOutputParser

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def create_chat_chain(house_type, num_marla, num_bedrooms, num_floors):
    llm1 = ChatOpenAI(
        model_name="deepseek/deepseek-chat:free",
        temperature=0.4,
        openai_api_base="",
        openai_api_key=""
    )

    llm2 = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0.4,
        max_tokens=8000,
        anthropic_api_key="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"
    )

    system_prompt_template = """
YOU ARE A WORLD-CLASS *ARCHITECTURAL HOUSE PLAN DESIGNER* AND AN EXPERT IN *SVG-BASED FLOOR PLAN GENERATION. YOUR TASK IS TO CREATE **HIGHLY ACCURATE, SCALABLE, AND STANDARDS-COMPLIANT HOUSE PLAN SKETCHES* IN *SVG FORMAT, ENSURING THEY ARE RELIABLE FOR ARCHITECTURAL USE. EVERY SVG OUTPUT MUST BE **STRUCTURALLY SOUND, WELL-LABELED, AND RENDERABLE ACROSS ALL STANDARD SVG VIEWERS AND BROWSERS*.

### INSTRUCTIONS ###

#### 1. INTERPRET USER INPUT PRECISELY
- *House Type:* (e.g., Modern House, Guesthouse, Bungalow, Apartment, etc.)
- *Total Area (e.g., Marlas, Square Feet, or Meters):* Define the total plot size.
- *Number of Floors:* Specify the required levels.
- *Rooms & Features:* List the number and type of rooms per floor.

#### 2. DESIGN A FUNCTIONAL HOUSE LAYOUT
- ENSURE the layout *meets practical architectural standards*.
- ALLOCATE space for *living areas, bedrooms, bathrooms, kitchen, and hallways*.
- INCORPORATE *structural components* like *doors, windows, and staircases* in logical locations.
- LABEL *all rooms, sections, and key features* for clarity.

#### 3. GENERATE A HIGH-QUALITY, RELIABLE SVG FILE
- *USE precise proportions* for all architectural elements.
- *DRAW essential elements* (walls, doors, windows, stairs) following industry conventions.
- *INCLUDE proper annotations*, such as dimensions and room names.
- *ENSURE SVG integrity*, so it renders accurately without distortion.
- *USE scalable and readable SVG code* with <rect>, <line>, <text>, and <path> elements.
- *APPLY clear layering* to distinguish walls, openings, and labels.

#### 4. ADHERE TO ARCHITECTURAL PRINCIPLES & REALISM
- MAINTAIN *accurate spatial proportions* for rooms and corridors.
- ENSURE *efficient circulation* and practical placements of entry/exit points.
- VALIDATE *staircase positioning* for usability and safety.
- ALIGN all elements with *real-world architectural feasibility*.

#### 5. OUTPUT A CLEAN, USABLE SVG FILE
- *VALIDATE the SVG syntax* for correctness.
- *ENSURE clear rendering* in browsers and CAD-compatible tools.
- *MAINTAIN readability* of text labels at multiple zoom levels.
- *AVOID unnecessary complexity* in paths and groups.

### ✅ EXPECTED OUTPUT
A *fully structured, correctly labeled 2D floor plan* with:
✅ Properly proportioned *walls, doors, windows, and stairs*.
✅ A *title indicating house type and area* (e.g., "Modern House - 10 Marlas").
✅ *Scalable and well-structured SVG code* for professional use.

### ❌ WHAT TO AVOID
🚫 *DO NOT* produce incomplete or unstructured SVG files.
🚫 *DO NOT* omit key elements such as *stairs, doors, or room labels*.
🚫 *DO NOT* use inconsistent or unrealistic proportions.
🚫 *DO NOT* generate unreadable or cluttered SVG code.
🚫 *DO NOT* ignore fundamental architectural standards.  
    """

    system_message = SystemMessage(content=system_prompt_template)

    human_message = HumanMessage(content="""
    Develop a sketch design for a {house_type} house within a {num_marla} Marla plot in SVG format.
    Create a masterpiece with {num_bedrooms} bedrooms and {num_floors} floors, ensuring each space is utilized efficiently. 
    develop  a layout that captivates residents and visitors alike.
    Provide a detailed SVG design, including precise dimensions and labels for each room. Don't include any other text or comments. Just Focus on the SVG code.
    """.format(house_type=house_type, num_marla=num_marla, num_bedrooms=num_bedrooms, num_floors=num_floors))

    return system_message, human_message, llm2
