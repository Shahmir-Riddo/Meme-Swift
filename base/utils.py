import requests
from PIL import Image
import openai
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from .models import Meme
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import replicate


def generate_captions(text):


    result = f"a photography of {text}"

    return result

def generate_meme_text(desc, context="No Context"):
    openai.api_key = "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"
    prompt = f"Generate a short meme top text without any quotes using reddit dark humour based on the meme template . meme template - {desc}. the number of words of the meme top text will be 5 or less. Meme Context - {context}"
    completion = openai.Completion()

    try:

        response = completion.create(prompt=prompt, engine="text-davinci-002", max_tokens=1000)
        answer = align_text(response.choices[0].text.strip())
        answer = answer.replace('"', '')
        return answer
    except Exception as e:
        return e

def generate_meme(img, text):
    base_app_directory = os.path.dirname(os.path.abspath(__file__))
    font_filename = 'impact.ttf'
    font_path = os.path.join(base_app_directory, font_filename)

    image = Image.open(img)
    image = image.resize((960, 960))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 60)


    text_size = draw.textsize(text, font=font)


    x = (image.width - text_size[0]) // 2
    y = 20

    draw.text((x, y), f"{text}", font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0)) # Change the text and position as desired

        # Save the image to memory
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_file = InMemoryUploadedFile(image_io, None, 'image.jpg', 'image/jpeg', image_io.getbuffer().nbytes, None)

    return image_file


def watermark(image):
    base_app_directory = os.path.dirname(os.path.abspath(__file__))
    font_filename = 'impact.ttf'
    font_path = os.path.join(base_app_directory, font_filename)
    text = "Made with memeswift.com"

    image = Image.open(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 30)
    font2 = ImageFont.truetype(font_path, 15)
    text_size = draw.textsize(text, font=font)
    width, height = image.size

    x = 5
    y = height - 50
    v = height - 20
    z = 7

    draw.text((x, y), f"{text}", font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))



    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_file = InMemoryUploadedFile(image_io, None, 'image.jpg', 'image/jpeg', image_io.getbuffer().nbytes, None)

    return image_file



def get_caption(url):
    os.environ['REPLICATE_API_TOKEN'] = 'r8_QUyto5FxE0EUucKVF80wd1fWVtZI5yd1eEWIJ'
    model_path = "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746"

    try:
        output = replicate.run(
    "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
    input={"image": url}
)
        return output.split(": ")[1]

    except Exception as e:
        return e





def align_text(text):
    words = text.split()
    aligned_text = ""

    for index, word in enumerate(words, start=1):
        aligned_text += word
        if index % 6 == 0:
            aligned_text += "\n"
        else:
            aligned_text += " "

    return aligned_text.strip()





