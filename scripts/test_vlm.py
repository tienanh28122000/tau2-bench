import base64
from litellm import completion

# 1. Configuration
MODEL_NAME = "gpt-4.1-mini"
IMAGE_PATH = "19646_30114.png"               # Path to your satellite tile

def call_vlm():
    # 2. Encode local image to base64
    with open(IMAGE_PATH, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    # 3. Call LiteLLM
    response = completion(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is the population density score (0-10) of this area?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"}
                    },
                ],
            }
        ],
        max_tokens=300
    )

    # 4. Print Result
    print(response.choices[0].message.content)

if __name__ == "__main__":
    call_vlm()