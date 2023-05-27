import requests
from PIL import Image
from django.core.files.storage import default_storage
from transformers import BlipProcessor, BlipForConditionalGeneration
from django.shortcuts import render
from .utils import generate_captions, generate_meme_text, generate_meme, watermark, get_caption
from .models import Meme
from django.core.files.base import ContentFile

def home(request):
    return render(request, "index.html")

def meme(request):
    if request.method == 'POST':
        context = request.POST.get('context')
        template = request.POST.get('dropdownMenuButton')
        print(context, template)
        try:
            image = request.FILES['image']
        except:
            return render(request, "index.html", {"error": "Please Upload Or Click An Image To Generate Meme"})
      
        picture_data = image.read()
        
       
        picture_name = image.name
        picture_path = default_storage.save(f'pictures/{picture_name}', ContentFile(picture_data))
        

        picture_url = default_storage.url(picture_path)
        picture_url = f"memeswift.render.com{picture_url}"
        
        caption = get_caption(picture_url)
        meme_text = generate_meme_text(caption, context)
        
        meme = generate_meme(image, meme_text)
        meme = watermark(meme)
      
        meme_obj = Meme()
        meme_obj.photo = meme
        
        meme_obj.caption = caption
        meme_obj.meme_text = meme_text
        meme_obj.save()       

        return render(request, 'result.html', {'meme_text': meme_obj.meme_text, 'caption': caption, 'meme': meme_obj.photo.url, 'url': picture_url})
    
        

    return render(request, 'result.html')