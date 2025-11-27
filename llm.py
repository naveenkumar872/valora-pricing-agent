from langchain_nvidia_ai_endpoints import ChatNVIDIA
import json
test_llm = ChatNVIDIA(
                    model="meta/llama-3.1-70b-instruct",
                    api_key="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"
                )


system_prompt="""

You are an AI assistant that extracts structured information from natural language queries related to selling products. 
The user will describe a product they want to sell and its base cost.

Your task:
1. Identify the product name (search query).
2. Identify the base cost (a number).
3. Return the result in valid JSON format with keys: "product" and "base_cost".

Output strictly as JSON. Do not add explanations.


"""


def extract_to_json(user_query, output_file="output.json"):
    # Call the model
    response = test_llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ])

    # Get raw JSON text
    raw_json = response.content.strip()

    # Parse into Python dict
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON: {raw_json}")

    # Save to JSON file
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return data

