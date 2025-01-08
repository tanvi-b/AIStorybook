#got API authentication code from https://huggingface.co/docs/api-inference/getting-started
#got code structure for images from here: https://huggingface.co/docs/api-inference/tasks/text-to-image

#Errors: want to print just story but sometimes printing stuff that model adds, images are little weird

#"https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
#"https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
#"https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"

import time
import requests
import io
from PIL import Image

TEXT_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
headers = {"Authorization": f"Bearer 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"}

def generate_text(prompt, max_pages=10, tokens_per_page=100):
    story = prompt.strip()

    for page_num in range(max_pages):
        payload = {
            "inputs": story,
            "parameters": {
                "max_new_tokens": tokens_per_page,
                "return_full_text": False,
                "temperature": 0.7
            }
        }

        while True:
            response = requests.post(TEXT_API_URL, headers=headers, json=payload)
            result = response.json()
            if "error" in result and "loading" in result["error"]:
                print("Model is loading")
                time.sleep(20)
                continue
            elif "error" in result:
                print(f"Error: {result['error']}")
            break

        page_text = result[0].get("generated_text", "").strip()
        if page_text == "" or page_text is None:
            print("Story finished")
            break

        print(f"Page {page_num + 1}:\n{page_text}\n")
        story += " " + page_text

        image_bytes = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": page_text}).content
        image = Image.open(io.BytesIO(image_bytes))
        image.show()

prompt = "Write a story about a young girl going to New York"
generate_text(prompt)