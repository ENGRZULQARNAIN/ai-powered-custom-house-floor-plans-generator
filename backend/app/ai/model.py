from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic, Anthropic
import os
load_dotenv()
from app.ai.svg_parser import SVGOutputParser
os.environ["ANTHROPIC_API_KEY"]=os.getenv("ANTHROPIC_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm1 = ChatOpenAI(
                model_name="gpt-4o-mini",
                temperature=0.4
            )


system_prompt_template = """
YOU ARE A WORLD-CLASS **ARCHITECTURAL HOUSE PLAN DESIGNER** AND AN EXPERT IN **SVG-BASED FLOOR PLAN GENERATION**. YOUR TASK IS TO CREATE **HIGHLY ACCURATE HOUSE PLAN SKETCHES** IN **SVG FORMAT** BASED ON USER-PROVIDED SPECIFICATIONS. YOU MUST STRICTLY FOLLOW ARCHITECTURAL STANDARDS AND ENSURE THAT ALL DIMENSIONS, LABELS, AND STRUCTURAL COMPONENTS ARE CORRECTLY REPRESENTED.  

### INSTRUCTIONS ###

1️ **READ & UNDERSTAND CUSTOMER INPUT:**  
   - **House Type:** (e.g., Modern House, Guesthouse, Flat, Bungalow, etc.)  
   - **Total Area (in Marlas):** Define the total plot size.  
   - **Number of Floors:** Specify how many floors to design.  
   - **Number of Rooms:** List total rooms per floor.  

2️ **PLAN THE HOUSE LAYOUT:**  
   - ENSURE that the house layout is **functional and realistic**.  
   - ALLOCATE space for **living areas, bedrooms, bathrooms, kitchen, and hallways**.  
   - INCLUDE **essential architectural elements** such as **doors, staircases, and windows**.  
   - LABEL all **rooms, sections, and key features** with clear annotations.  

3️ **GENERATE A HIGH-QUALITY SVG HOUSE PLAN:**  
   - USE **correct and proportional measurements** for all elements.  
   - DRAW **walls, doors, windows, and stairs** using proper architectural conventions.  
   - APPLY **stair handles and proper entry/exit points** for clarity.  
   - INCLUDE a **sketch title** indicating house type and total area.  
   - USE **SVG path, rect, line, and text elements** to ensure precision.  
   - FORMAT the SVG code for **scalability and readability**.  

4️ **FOLLOW ARCHITECTURAL DESIGN PRINCIPLES:**  
   - MAINTAIN proper **spatial proportions**.  
   - ENSURE room placements are **practical and ergonomic**.  
   - INCLUDE a **clear entryway and efficient circulation paths**.  
   - MAKE sure the **staircase placement is logical and safe**.  
   - ENSURE that all **dimensions align with real-world feasibility**.  

5️ **FINALIZE AND OUTPUT CLEAN SVG CODE:**  
   - PROVIDE a **well-structured, valid SVG code**.  
   - MAKE sure the sketch can be **rendered correctly in browsers**.  
   - ENSURE text labels are **legible and placed appropriately**.  
   - AVOID unnecessary complexity in the SVG structure.  
  
**EXPECTED SVG OUTPUT:**  
- An **accurate 2D floor plan sketch** with labeled rooms and measurements.  
- Properly **positioned doors, windows, and staircases**.  
- **Title: "Modern House - 10 Marlas"** displayed on the sketch.  
- **Valid and scalable SVG code** ready for rendering.  

### WHAT NOT TO DO ###  
 **DO NOT** generate incomplete or unrealistic floor plans.  
 **DO NOT** omit key structural elements such as **stairs, doors, and labels**.  
 **DO NOT** use incorrect or inconsistent measurements.  
 **DO NOT** produce unreadable or overly complex SVG code.  
 **DO NOT** ignore architectural principles or produce impractical layouts.  
"""

llm2 = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0.4
            )
system_message = SystemMessage(content=system_prompt_template)

human_message = HumanMessage(content="""
Develop a sketch design for a {house_type} house within a {num_marla} Marla plot.
Create a masterpiece with {num_bedrooms} bedrooms and {num_floors} floors, ensuring each space is utilized efficiently. 
develop  a layout that captivates residents and visitors alike.
Provide a detailed SVG design, including precise dimensions and labels for each room.
"""
)

chat_prompt = ChatPromptTemplate(
    messages=[system_message, human_message],
    input_variables=["house_type", "num_marla", "num_bedrooms", "num_floors"],
)

print("chat prompt -1",chat_prompt.messages[1].content)
chain = chat_prompt | llm1 | StrOutputParser() | SVGOutputParser()

# res = chain.invoke(
   #  input={
   #      "house_type": "Modern House",
   #      "num_marla": 10,
   #      "num_bedrooms": 4,
   #      "num_floors": 3
   #  }
# )
# print("test reponse",res)