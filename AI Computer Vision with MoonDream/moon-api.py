import moondream as md
from PIL import Image

key = "YOUR API KEY"

model = md.vl(api_key=key)

# Load an image
image = Image.open("picture.png")

# Generate a caption
result = model.caption(image, length="normal")
print(result["caption"])
