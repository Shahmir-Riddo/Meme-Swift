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

<<<<<<< HEAD
        picture_url = f"https://{request.get_host()}/{meme_obj.raw_photo}"
=======
        picture_url = f"https://memeswiftai.pythonanywhere.com/media/342920087_1281416352800985_6484091355838271538_n.jpg"
>>>>>>> 865f0bcf0be0bcab9bd96bf32927c9dfe1479d0f
        caption = get_caption(picture_url)

        meme_text = generate_meme_text(caption, context)


<<<<<<< HEAD
        meme = generate_meme(image, meme_text)
=======
        meme = generate_meme(image, caption)
>>>>>>> 865f0bcf0be0bcab9bd96bf32927c9dfe1479d0f
        meme = watermark(meme)

        meme_obj = Meme(photo=meme, caption=caption, meme_text=meme_text)
        meme_obj.save()
<<<<<<< HEAD

        return render(request, 'result.html', {'meme_text': meme_obj.meme_text, 'caption': caption, 'meme': meme_obj.photo, 'url': picture_url})


=======
>>>>>>> 865f0bcf0be0bcab9bd96bf32927c9dfe1479d0f

        return render(request, 'result.html', {'meme_text': meme_obj.meme_text, 'caption': caption, 'meme': meme_obj.photo, 'url': picture_url})



    return render(request, 'result.html')
