import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from .models import Meme
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

def generate_captions(pic):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processor_path = os.path.join(base_dir, r"base")
    model_path = os.path.join(base_dir, "base")

    processor = BlipProcessor.from_pretrained(model_path)
    model = BlipForConditionalGeneration.from_pretrained(model_path)


    img = Image.open(pic)
    raw_image = Image.open(pic)


    text = "a photography of"
    inputs = processor(raw_image, text, return_tensors="pt")

    out = model.generate(**inputs)
    result = (processor.decode(out[0], skip_special_tokens=True))
    return result


def generate_meme_text(desc, context="No Context"):
    openai.api_key = "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"
    prompt = f"Generate a short meme top text without any quotes using reddit dark humour  based on the meme template . meme template - {desc}. the number of words of the meme top text will be 5 or less. Meme Context - {context}"
    completion = openai.Completion()

    
  
    response = completion.create(prompt=prompt, engine="text-davinci-002", max_tokens=2048)
    answer = align_text(response.choices[0].text.strip())
    answer = answer.replace('"', '')
    return answer

def generate_meme(img, text):
    image = Image.open(img)
    image = image.resize((960, 960))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('impact.ttf', 60) 
    
    
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
    text = "Made with memeswift.com"

    image = Image.open(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('calibri.ttf', 30)
    font2 = ImageFont.truetype('calibri.ttf', 15)
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

def image_caption(image):


    gray = image.convert('L')


    img_array = np.array(gray)


    img_array = 255 - img_array


    threshold = 100
    img_array[img_array < threshold] = 0
    img_array[img_array >= threshold] = 255



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

