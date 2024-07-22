from dotenv import load_dotenv
import os
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class LocationModel(BaseModel):
    location: str = Field(description="The name of the location where the disaster has occurred")
    coordinates: dict = Field(description="A dictionary containing the latitude and longitude of the location where the disaster has occurred")
    
parser = JsonOutputParser(pydantic_object=LocationModel)

prompt = PromptTemplate(
    template='''Based on the tweet: "{tweet}", identify the location and provide the latitude and longitude as "coordinates"
    Return the output in the following JSON format: {format_instruction}''',
    input_variables=["tweet"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
location_model = prompt | llm | parser

'''tweet = "Assam floods have killed about 1000s of people"
population_data = {
    "population_split": {
        "adults_18_44": 136871,
        "adults_45_59": 68435,
        "adults_60_plus": 34217,
        "children": 102653,
    },
    "female_population": 164792,
    "male_population": 177386,
    "status": "success",
    "total_population": 342178
}


result = chain.invoke({
    "tweet": tweet,
    "population": population_data,
})

print(result)'''