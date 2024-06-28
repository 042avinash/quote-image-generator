import requests as req
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from IPython.display import display
import textwrap
import json

img_url = "https://api.api-ninjas.com/v1/randomimage"
text_url = "https://api.api-ninjas.com/v1/quotes"

img = Image.open(BytesIO(req.get(img_url , headers = {'X-Api-Key': 'z4y4Ua2AchpsgII3m4iHKw==Bhx5xZDCi4vqd67s', 'Accept': 'image/jpg'}).content))

response = req.get(text_url , headers = {'X-Api-Key': 'z4y4Ua2AchpsgII3m4iHKw==Bhx5xZDCi4vqd67s'})

if response.status_code == 200:
        quote_data = response.json()
        if isinstance(quote_data, list):
            if len(quote_data) > 0:
                text = quote_data[0].get('content')
                if text:
                    print(f"Quote: {text}")
                else:
                    print("No quote content found in response.")
            else:
                print("Empty list returned.")
        elif isinstance(quote_data, dict):
            text = quote_data.get('content')
            if text:
                print(f"Quote: {text}")
            else:
                print("No quote content found in response.")
        else:
            print("Unexpected response format.")
    
        if text:
            print(f"Quote: {text}")
        else:
            print("No quote content found in response.")
else:
        print(f"Error fetching quote: Status code {response.status_code}")
        print(f"Response content: {response.content}")


text = '\n'.join(textwrap.wrap(text, width=40))

draw = ImageDraw.Draw(img)

font = ImageFont.load_default()

text_size = draw.textsize(text, font)
position = ((img.width - text_size[0])/2,
            (img.height - text_size[0])/2)

draw.text(position, text, font=font, fill= "white")
display(img)
