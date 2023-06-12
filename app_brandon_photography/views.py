from django.shortcuts import render,redirect
from .models import *
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# Create your views here.
    
def kiskedvenc(request):
    pictures = Photos.objects.filter(category__name="kiskedvenc")
    return render(request, 'kutyafotozas.html',  {'pictures': pictures, 'title': 'szabadtéri kutyafotózás Budapesten és környékén'})

def eskuvo(request):
    pictures = Photos.objects.filter(category__name="esküvő")
    return render(request, 'eskuvo.html',  {'pictures': pictures, 'title': 'esküvő fotózás, érzelmek megörökítése Budapesten és környékén'})
    
def termek(request):
    pictures = Photos.objects.filter(category__name="termékfotó")
    return render(request, 'termek.html',  {'pictures': pictures, 'title': 'olcsó és gyors termékfotózás weboldalhoz, webáruházhoz | Budapest'})

def portre(request):
    pictures = Photos.objects.filter(category__name="portré")
    return render(request, 'portre.html',  {'pictures': pictures, 'title': 'portré fotózás tinderre, önéletrajzhoz, facebookra | Budapest'})
    
def video(request):
    return render(request, 'video.html', {'title': 'nagipix reklámvideó, vállalkozás bemutató, esemény videó'})
    
def marketing(request):
    return render(request, 'marketing.html', {'title': 'nagipix fotó, reklámvideó, weboldal, weblap készítés egy helyen'})

def impresszum(request):
    return render(request, 'impresszum.html', {'title': 'nagipix fotó és video | Budapest | impresszum, elérhetőség'})
    
def intro(request):
    categories = PhotoCategory.objects.all().order_by('priority')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'name': form.cleaned_data['name'],
                'email_address': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message,  body['email_address'], [body['email_address']])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("gallery.html")

    form = ContactForm()
    
    return render(request, 'intro.html', {'categories': categories, 'form': form, 'title': 'nagipix fotó és video | Budapest | kutyafotózás, esküvő és portré'})

def kapcsolat(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'name': form.cleaned_data['name'],
                'email_address': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message,  body['email_address'], [body['email_address']])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("gallery.html")

    form = ContactForm()
    return render(request, "kapcsolat.html", {'form': form})
    
def blog(request):
    bloglist = BlogPost.objects.all().order_by('-created_at')
    
    return render(request, "blog.html", {"bloglist": bloglist, 'title': 'blog, blogposztok, értekezések és elmélkedések fotózásról'})

def blogpost(request):
    blogpost_id = request.GET.get('blogpost_id')
    blogpost = BlogPost.objects.get(id=blogpost_id)
    
    return render(request, 'blogpost.html',  {'blogpost': blogpost, 'title': blogpost.title})
    
def gallery(request):
    
    category_id = request.GET.get('gallery_id')
    if category_id:
        pictures = Photos.objects.filter(category=category_id)
        category = PhotoCategory.objects.filter(pk=category_id)
    else:
        pictures = Photos.objects.filter(main_site_visibility=True)
    
    print(category)
    pictures = pictures.order_by('priority')
    picture_quantity = len(pictures)
    breakpnumber = round(picture_quantity/3.)
    breakpremaining = picture_quantity%3
    bplist = [0]
    print(pictures[0].photo_tumb)
    if breakpremaining in [0,2]:
        bplist.append(breakpnumber)
        bplist.append(2*breakpnumber)
    elif breakpremaining in [1]:
        bplist.append(breakpnumber+1)
        bplist.append(2*breakpnumber+1)


    return render(request, 'gallery.html', {'pictures': pictures, 'breakpnumber': breakpnumber, 'bplist': bplist, 'category': category})
