from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.ai.svg_parser import SVGOutputParser


llm = ChatOpenAI(
            openai_api_key="",
            openai_api_base='',
            model_name='',
            )

system_message = SystemMessage(content="""
You are a powerful house architect assistant. You task is to help the user to design a house in svg format. 
You must not generate other text than the svg code it is very crucial. Just focus on the svg code generation.
"""
)

human_message = HumanMessage(content="""
As a skilled house architect assistant, your task is to design an extraordinary {house_type} house within a {num_marla} Marla plot.
Create a masterpiece with {num_bedrooms} bedrooms and {num_floors} floors, ensuring each space is utilized efficiently. 
Imagine a layout that captivates residents and visitors alike.
Provide a detailed SVG design, including precise dimensions and labels for each room.
"""
)

chat_prompt = ChatPromptTemplate(
    messages=[system_message, human_message],
    input_variables=["house_type", "num_marla", "num_bedrooms", "num_floors"],
)

chain = chat_prompt | llm | StrOutputParser() | SVGOutputParser()