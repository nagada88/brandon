from django.shortcuts import render,redirect
from .models import *
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

# Create your views here.
    
def kiskedvenc(request):
    pictures = Photos.objects.filter(category__name="kutyafotózás")
    studiopictures = Photos.objects.filter(category__name="studio")
    reviews = load_more_reviews(request)

    return render(request, 'kutyafotozas.html',  {'pictures': pictures, 'studiopictures': studiopictures, 'title': 'szabadtéri kutyafotózás Budapesten és környékén', 'reviews': reviews})


def review_upload(request):
    reviews = load_more_reviews(request)
    return render(request, 'review_partial.html',  {'reviews': reviews}) 
  
def load_more_reviews(request):
    page = request.GET.get("page")
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 3)

    for review in reviews:
        review.remaining_stars = 5 - review.stars

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return reviews

@login_required
def edit_availability(request, date):
    if request.method == 'POST':
        availability = get_object_or_404(Availability, date=date)
        new_status = request.POST.get('status')
        if new_status in dict(Availability.STATUS_CHOICES).keys():
            availability.status = new_status
            availability.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

from django.shortcuts import render
from django.utils.timezone import now
from calendar import monthrange
import calendar
from datetime import date
from .models import Availability
from django.contrib.auth.decorators import login_required

def calendar_view(request):
    # Ellenőrizzük, hogy be van-e jelentkezve
    if request.user.is_authenticated:
        return admin_calendar_view(request)
    return public_calendar_view(request)



def generate_calendar_data(year, month):
    """Naptár adatok generálása egy adott év-hónap alapján."""
    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, monthrange(year, month)[1])

    # Foglaltságok lekérése az adott hónapra
    availabilities = Availability.objects.filter(date__range=[first_day_of_month, last_day_of_month])
    availability_map = {a.date: a.status for a in availabilities}

    # Naptár generálása
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.itermonthdates(year, month)

    # Napokhoz státusz hozzárendelése
    calendar_data = []
    for day in month_days:
        status = availability_map.get(day, 'green') if day.month == month else 'empty'
        calendar_data.append({'date': day, 'status': status})
    return calendar_data

def public_calendar_view(request):
    today = now().date()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    calendar_data = generate_calendar_data(year, month)
    prev_month = (month - 1) if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = (month + 1) if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    context = {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'is_admin': False  # Publikus nézet
    }
    return render(request, 'public_calendar.html', context)

@login_required
def admin_calendar_view(request):
    today = now().date()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    calendar_data = generate_calendar_data(year, month)
    prev_month = (month - 1) if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = (month + 1) if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    context = {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'is_admin': True  # Admin nézet
    }
    return render(request, 'admin_calendar.html', context)


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
            return redirect("sikeresmail.html")

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
                send_mail(subject, message,  body['email_address'], ['info@nagipix.hu'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")

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
    
def sikeresmail(request):
    return render(request, 'sikeresmail.html', {'title': 'sikeres email küldés'})
