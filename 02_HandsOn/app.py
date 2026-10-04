import os
from dotenv import load_dotenv
from openai import OpenAI
from evaluator import evaluate_results
from test_cases import test_cases
from prompts import PROMPT_V1, PROMPT_V2, PROMPT_V3


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def classify_product(product, prompt):
    final_prompt = prompt.format(product=product)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )
    return response.choices[0].message.content.strip()


def run_prompt(prompt):
    results = []

    for test_case in test_cases:
        product = test_case["input"]

        prediction = classify_product(product, prompt)

        results.append({
            "input": product,
            "expected": test_case["expected"],
            "prediction": prediction
        })

    return results


if __name__ == "__main__":

    results = run_prompt(PROMPT_V3)

    for result in results:
        print("\nProduct:", result["input"])
        print("Expected:", result["expected"])
        print("Prediction:", result["prediction"])

    evaluate_results(results)