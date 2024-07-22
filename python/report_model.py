from dotenv import load_dotenv
import os
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
import json

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class DisasterModel(BaseModel):
    number_of_camps: int = Field(description="The number of camps to be allocated in response to the sudden natural disaster which has occurred")
    number_of_people: int = Field(description="The number of people who might have been affected by the natural disaster which has occurred")
    first_responder_count: int = Field(description="The number of people to be deployed to the affected region in response to the natural disaster which has occurred")
    supplies_required_count: dict = Field(description="The supplies required and the count of each supply for better planning. For water, give the count in terms of 1L bottles. For food, specify types such as snacks, cold-freeze foods, etc.")
    validity_of_disaster: bool = Field(description="The prediction that this disaster is actually occurring after it has been webscraped from Twitter")
    
parser = JsonOutputParser(pydantic_object=DisasterModel)

prompt = PromptTemplate(
    template='''Based on the tweet: "{tweet}", identify if the natural disaster mentioned is actually occurring and indicate this in "validity_of_disaster".
    Considering the population data provided in JSON format as {population}, determine the number of people affected ("number_of_people"), the number of camps required ("number_of_camps"), the number of first responders needed ("first_responder_count"), and the supplies required, broken down as follows:
    - Water (in terms of 1L bottles, consider that each person needs about 3 liters of water per day for drinking and basic hygiene)
    - Food (split into snacks, cold-freeze foods, and hot foods, consider that each person needs about 2000-2500 calories per day. For instance, 3 meals per day with an average of 500 calories each for snacks, 700 calories for cold-freeze foods, and 800 calories for hot foods)
    - Medicine (split into IV drips, first aid kits, and other necessities, consider common requirements during disasters such as wound care, infection control, and chronic disease management. For example, 1 first aid kit per 50 people and 1 IV drip per 100 people)
    Provide values that are practical and realistic for a disaster response scenario, considering that a maximum number of people might have enough groceries to sustain themselves initially for a few days. This will be the first batch of supplies, so keep the quantities as low as possible, ideally within the thousands for each supply.
    Return the output in the following JSON format: {format_instruction}''',
    input_variables=["tweet", "population"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
chain = prompt | llm | parser

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