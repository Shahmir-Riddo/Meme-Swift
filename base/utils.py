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
import json

#from bardapi import Bard
import re

def extract_meme_caption(text):
    pattern = r'(?<=meme caption:)\s*(.*?)$'
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1)
    return text.upper()
    
  
#def generate_meme_text_context(desc, context=""):
   # os.environ['_BARD_API_KEY']="XAhorVyNRCDXcpzrnG_t9_GVuDA1_YJ7x2L3FiTVfaN8rPcMDgR8PxNRatod18hLW6APrQ."
   # input_text = f"Write a meme caption from a first person perspective under 8 words inspired from dark humoured and insulting memes using the provided meme template and context. meme template - '{desc}' and context - '{context}'. write 'meme caption :' before the meme caption"

   # result = extract_meme_caption((Bard().get_answer(input_text)['content']).strip())
   # return align_text(result)

#def generate_meme_text(desc):
   # os.environ['_BARD_API_KEY']="XAhorVyNRCDXcpzrnG_t9_GVuDA1_YJ7x2L3FiTVfaN8rPcMDgR8PxNRatod18hLW6APrQ."
   # input_text = f"Write a meme caption from a first person perspective under 8 words inspired from dark humoured and insulting memes using the provided meme template. meme template - '{desc}'. write 'meme caption :' before the meme caption"

   # result = extract_meme_caption((Bard().get_answer(input_text)['content']).strip())
   # return align_text(result)

def generate_meme_text(desc, context="No Context"):
    
    openai.api_key = "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"
 
    prompt = f"Write a meme caption from a first person perspective under 8 words inspired from dark humoured memes using the provided meme template and context. meme template - {desc}, context - {context}"
    
   
    
    completion = openai.Completion()

    try:

        response = completion.create(prompt=prompt, engine="text-davinci-003",  max_tokens=60, n=1)
        answer = align_text(response.choices[0].text.strip())
        answer = answer.replace('"', '')
        answer = answer.lower().replace('fuck', '****')

        return answer.upper()
        
    except Exception as e:
        return str(e)

def generate_meme(img, text):
    text = text.upper()
    base_app_directory = os.path.dirname(os.path.abspath(__file__))
    font_filename = 'impact.ttf'
    font_path = os.path.join(base_app_directory, font_filename)

    image = Image.open(img)
    image = image.resize((960, 960))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 65)


    text_size = draw.textsize(text, font=font)


    x = (image.width - text_size[0]) // 2
    y = 20

    draw.text((x, y), f"{text}", font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0)) # Change the text and position as desired

        
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_file = InMemoryUploadedFile(image_io, None, 'image.jpg', 'image/jpeg', image_io.getbuffer().nbytes, None)

    return image_file



def watermark(image):
    base_app_directory = os.path.dirname(os.path.abspath(__file__))
    font_filename = 'calibri.ttf'
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
    os.environ['REPLICATE_API_TOKEN'] = "[API_KEY_HERE]"

    try:

        output = replicate.run(
        "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
        input={"image": url})
        
        result = output.split(":")[1]
        
        return "a photography of" + result
        
    except Exception as e:
        

        return f"A man standing"


def align_text(text):

    words = text.split()
    aligned_text = ""

    for index, word in enumerate(words, start=1):
        aligned_text += word
        if index % 4 == 0:
            aligned_text += "\n"
        else:
            aligned_text += " "

    return aligned_text.strip()




def convert_png_to_jpg(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")

    output = BytesIO()
    img.save(output, format='JPEG')
    output.seek(0)

    converted_image = InMemoryUploadedFile(
        output, 'ImageField', f"{image.name.split('.')[0]}.jpg", 'image/jpeg', output.tell(), None
    )

    return converted_image


def generate_captions(text):


    result = f"a photography of {text}"

    return result

def generate_meme_text(desc, context="No Context"):
    openai.api_key = "[API_KEY_HERE]"
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





