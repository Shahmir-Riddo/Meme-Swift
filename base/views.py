
from django.shortcuts import render, redirect
from .utils import generate_captions, generate_meme_text, generate_meme, generate_meme_bengali, watermark, get_caption, convert_png_to_jpg
from .models import Meme
from django.core.files.base import ContentFile
import random
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from PIL import Image
from django.core.files.storage import default_storage

def home(request):
    return render(request, "index.html")


def meme(request):
    if request.method == 'POST':
        context = request.POST.get('context')
        lang = request.POST.get('lang')

        try:
            
            image = request.FILES['image']
        except:
            return render(request, "index.html", {"error": "Please Upload Or Click An Image To Generate Meme"})
   
        
        meme_obj = Meme(raw_photo=image)
        meme_obj.save()

        picture_url = f"https://memeswift.com/media/{meme_obj.raw_photo}"
        #caption = get_caption(picture_url)
        caption = generate_captions(image)
        
        meme_text = generate_meme_text(caption, context)
        
        if lang == "bn":
            meme = generate_meme_bengali(image, meme_text)
        else: 
            meme = generate_meme(image, meme_text)
            
            

        
        meme = watermark(meme)

        meme_obj.photo = meme
        meme_obj.caption = caption
        meme_obj.meme_text = meme_text
        meme_obj.save()
        advices = ["I don't always make memes, but when I do, they're dank.", "A day without memes is like a day without sunshine. - Unknown", "Memes are mirrors reflecting the depths of our thoughts.", "Be a seeker of truth, even in the realm of memes.", "The power of a meme lies in its ability to ignite thoughtful conversations."]
        advice = random.choice(advices)
        return render(request, 'result.html', {'meme_text': meme_obj.meme_text, 'caption': advice, 'meme': meme_obj.photo, 'url': picture_url})



    return render(request, 'result.html')
    
    
def server_error(request):
    return render(request, 'error.html', status=500)

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        if not username or not email or not password:
            messages.error(request, "Fill Up The Form")

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.info(request, "Registered Successfully")
            return redirect('/')

    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

