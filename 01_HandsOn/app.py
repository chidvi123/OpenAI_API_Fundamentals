import os
import json
import logging
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIError,
    #AuthenticationError,
    #NotFoundError,
    #RateLimitError
)
from models import ProductInfo
from pydantic import ValidationError


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger=logging.getLogger(__name__)


def get_product_response(user_input):
    logger.info("Sending request to the model")
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content":f"""
        Extract the product information from the text.

        Return only JSON with these fields:
        - product_name 
        - category
        - price ( number only , without currency symbols or words )

        Text :{
            user_input
        }
        """
                }
            ]
        )

        logger.info("Model response recieved successfully")
        return response.choices[0].message.content
    
    except APIError as e:
        logger.error(
            "API Error - Status Code %s - %s",
            e.status_code,
            e
        )
        return None


def validate_product(raw_output):
    logger.info("Parsing model response as JSON")
    #converting the string into json
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        logger.error("Model returned invalid JSON")
        return None

    logger.info("JSON Parsed Succesfully")

    # checking for the validation error
    try:
        product=ProductInfo(**data)
        logger.info("Pydantic Validation Successful")
        return product
    except ValidationError as e:
        logger.error('Pydantic validation failed : %s',e)
        return None


def main():
    logger.info("Application started")

    user_input = input("Enter product information: ")

    raw_output = get_product_response(user_input)

    if raw_output:
        print("\nRaw Model Response:")
        print(raw_output)

        product = validate_product(raw_output)

        if product:
            print("\nValidated JSON:")
            print(product.model_dump_json())

    logger.info("Application finished")

if __name__=="__main__":
    main()

