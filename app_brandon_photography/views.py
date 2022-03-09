from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
import pprint

# Create your views here.
def bio(request):
    return render(request, 'bio.html', {})
    
def video(request):
    return render(request, 'video.html', {})

def foto(request):
    return render(request, 'foto.html', {})

def kapcsolat(request):
    return render(request, 'kapcsolat.html', {})

