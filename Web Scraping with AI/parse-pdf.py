import base64
import json

import pypdfium2
from openai import OpenAI


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def ai(doc):
    key = "YOUR API KEY"

    client = OpenAI(api_key=key)

    base64_image = encode_image(doc)

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """This is a W2. Provide the Name, EIN and Salary of this employee in JSON format. Return **only** valid JSON with no backticks, 
                    no markdown, and no explanation.""",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    response = response.output_text
    return response


def image(doc):
    pdf = pypdfium2.PdfDocument(doc)

    for i, page in enumerate(pdf, start=1):
        image = page.render(scale=2).to_pil()
        jpg_path = f"page_{i}.jpg"
        image.save(jpg_path, "JPEG")
        return jpg_path


doc = "tax.pdf"
doc_image = image(doc)
response = ai(doc_image)
print(response)
response = json.loads(response)
print(response)
print(f"""{response['Name']} -- {response['EIN']} -- {response['Salary']}""")
