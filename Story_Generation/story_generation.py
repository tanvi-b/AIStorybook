#got API authentication code from https://huggingface.co/docs/api-inference/getting-started
#got code structure for images from here: https://huggingface.co/docs/api-inference/tasks/text-to-image

import os
import time
import requests
import io
from PIL import Image

TEXT_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
headers = {"Authorization": f"Bearer hf_"}

def generate_text(prompt, max_pages=1, tokens_per_page=100):
    story = prompt.strip()
    story_pages = []

    images_directory = "images"

    if os.path.exists(images_directory):
        for file in os.listdir(images_directory):
            file_path = os.path.join(images_directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    if not os.path.exists(images_directory):
        os.makedirs(images_directory)

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

        story += " " + page_text

        image_response = requests.post(IMAGE_API_URL, headers=headers, json={"inputs": page_text})

        image_path = None
        if image_response.status_code == 200:
            try:
                image_bytes = image_response.content
                image = Image.open(io.BytesIO(image_bytes))
                image_path = os.path.join(images_directory, f"page_{page_num + 1}.png")
                image.save(image_path)
                print(f"Image saved at: {image_path}")
            except Exception as e:
                print(f"Couldn't process image for page {page_num + 1}: {e}")
        else:
            print(f"Couldn't create image for page {page_num + 1}. HTTP code: {image_response.status_code}")

        story_pages.append({
            "text": page_text,
            "image": image_path if image_path else "Error generating image"
        })

    return story_pages