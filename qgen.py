from flask import Flask, render_template, send_file
import requests
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import textwrap

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Function to fetch a random image
def fetch_random_image():
    img_url = "https://api.api-ninjas.com/v1/randomimage"
    response = requests.get(img_url, headers={'X-Api-Key': 'z4y4Ua2AchpsgII3m4iHKw==Bhx5xZDCi4vqd67s', 'Accept': 'image/jpg'})
    image = Image.open(BytesIO(response.content))
    return image

# Function to fetch a random quote
def fetch_random_quote():
    text_url = "https://api.api-ninjas.com/v1/quotes"
    response = requests.get(text_url, headers={'X-Api-Key': 'z4y4Ua2AchpsgII3m4iHKw==Bhx5xZDCi4vqd67s'})
    quote = response.json()[0]['quote']
    return quote

# Function to add quote to image
def add_quote_to_image(image, quote):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("impact.ttf", 20)

    # Define the maximum width for the text
    max_width = image.width - 40  # 20 pixels padding on each side

    # Wrap the text to fit within the max width
    wrapped_text = textwrap.fill(quote, width=40)
    # Calculate text size and position using textbbox
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    
    # Split the wrapped text into lines
    lines = wrapped_text.split('\n')

    # Calculate the total height of the text block
    line_height = draw.textbbox((0, 0), lines[0], font=font)[3] - draw.textbbox((0, 0), lines[0], font=font)[1]
    text_height = line_height * len(lines)

    # Calculate the vertical position of the text block
    text_y = (image.height - text_height) / 2

    # Draw each line of text
    for line in lines:

        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (image.width - text_width) / 2

        # Draw a black rectangle behind the text
        draw.rectangle([text_x - 5, text_y - 5, text_x + text_width + 5, text_y + line_height + 5], fill="black")

        # Draw the text
        draw.text((text_x, text_y), line, font=font, fill="white")

        # Move to the next line
        text_y += line_height + 11
    
    return image

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate a new image with quote
@app.route('/generate')
def generate():
    try:
        print("Generating new image...")
        image = fetch_random_image()
        quote = fetch_random_quote()
        image_with_quote = add_quote_to_image(image, quote)
        image_path = os.path.join(app.config['STATIC_FOLDER'], 'quote_image.png')
        image_with_quote.save(image_path)
        print(f"Image saved to: {image_path}")
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        print(f"Error generating image: {e}")
        return str(e)

if __name__ == '__main__':
    if not os.path.exists(app.config['STATIC_FOLDER']):
        os.makedirs(app.config['STATIC_FOLDER'])
    app.run(debug=True)
