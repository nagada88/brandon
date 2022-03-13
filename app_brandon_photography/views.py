from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
import pprint

# Create your views here.
def mainpage(request):
    pictures = Photos.objects.filter(main_site_visibility=True)
    picture_quantity = len(pictures)
    breakpnumber = round(picture_quantity/3.)
    breakpremaining = picture_quantity%3
    bplist = [0]
    print(pictures[0].photo_tumb)
    if breakpremaining == 2:
        bplist.append(breakpnumber+1)
        bplist.append(bplist[1] + breakpnumber)
    elif breakpremaining in [0,1]:
        bplist.append(breakpnumber+1)
        bplist.append(2*breakpnumber+1)

    return render(request, 'mainpage.html', {'pictures': pictures, 'breakpnumber': breakpnumber, 'bplist': bplist})

def bio(request):
    return render(request, 'bio.html', {})
    
def video(request):
    return render(request, 'video.html', {})

def foto(request):
    return render(request, 'foto.html', {})

def kapcsolat(request):
    return render(request, 'kapcsolat.html', {})

