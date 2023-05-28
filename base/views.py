import requests
from PIL import Image
from django.core.files.storage import default_storage
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

        meme_obj = Meme(raw_photo=image)
        meme_obj.save()

        picture_url = f"https://memeswiftai.pythonanywhere.com/media/342920087_1281416352800985_6484091355838271538_n.jpg"
        caption = get_caption(picture_url)

        meme_text = generate_meme_text(caption, context)


        meme = generate_meme(image, caption)
        meme = watermark(meme)

        meme_obj = Meme(photo=meme, caption=caption, meme_text=meme_text)
        meme_obj.save()

        return render(request, 'result.html', {'meme_text': meme_obj.meme_text, 'caption': caption, 'meme': meme_obj.photo, 'url': picture_url})



    return render(request, 'result.html')
