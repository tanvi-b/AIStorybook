import openai

openai.api_key = "api key:

def generate_dalle_image(prompt, size="1024x1024"):
    try:
        print(f"Image prompt: '{prompt}'...")
        response = openai.Image.create_edit(
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = response['data'][0]['url']
        print(f"Image URL: {image_url}")
        return image_url
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    user_prompt = input("Enter image description: ")
    image_size = input("Enter image size (256x256, 512x512, or 1024x1024): ")
    if image_size not in ["256x256", "512x512", "1024x1024"]:
        image_size = "1024x1024"
    image_url = generate_dalle_image(user_prompt, size=image_size)
    if image_url:
        print(f"Generated image URL: {image_url}")