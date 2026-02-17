from google import genai
from google.genai import types

# ===============================
# DIRECT API KEY
# ===============================
API_KEY = ""

client = genai.Client(api_key=API_KEY)

# ===============================
# Parameters
# ===============================
prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
aspect_ratio = "1:1"   # Valid
num_images = 1

model = "gemini-2.5-flash-image"
# ===============================

for i in range(num_images):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio
            )
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image = part.as_image()
            filename = f"generated_image_{i+1}.png"
            image.save(filename)
            print(f"✅ Image saved as {filename}")