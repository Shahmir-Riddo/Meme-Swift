import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from django.shortcuts import render
from .utils import generate_captions, generate_meme_text, generate_meme, watermark
from .models import Meme


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
      

        caption = generate_captions(image)
        meme_text = generate_meme_text(caption, context)
        
        meme = generate_meme(image, meme_text)
        meme = watermark(meme)
        print(type(meme))
        print(type(image))
        meme_obj = Meme()
        meme_obj.photo = meme
        meme_obj.caption = caption
        meme_obj.meme_text = meme_text
        meme_obj.save()       

        return render(request, 'result.html', {'meme_text': meme_obj.meme_text, 'caption': caption, 'meme': meme_obj.photo.url})
    
        

    return render(request, 'result.html')