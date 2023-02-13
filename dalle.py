import requests

# Define the OpenAI API endpoint for generating images
dalle_endpoint = "https://api.openai.com/v1/images/generations"

# Read the generated DALL·E prompts from a file
with open("dalle_prompts.txt") as f:
    dalle_prompts = f.read().strip().split("\n")

# Generate images for each DALL·E prompt
for dalle_prompt in dalle_prompts:
    # Define the data for the API request
    data = {
        "model": "image-alpha-001",
        "prompt": dalle_prompt,
        "num_images": 1,
        "size": "1024x1024",
    }

    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    # Use the OpenAI API to generate an image
    response = requests.post(dalle_endpoint, headers=headers, json=data)

    # Get the generated image URL
    image_url = response.json()["data"][0]["url"]

    # Download the image
    response = requests.get(image_url)
    image_data = response.content

    # Save the image to a file
    with open(f"{dalle_prompt.replace(' ', '_')}.jpg", "wb") as f:
        f.write(image_data)
