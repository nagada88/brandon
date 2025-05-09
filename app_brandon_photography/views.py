from django.shortcuts import render,redirect
from .models import *
from .forms import ContactForm
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from calendar import Calendar
from datetime import date
from django.views.generic.detail import DetailView

HUNGARIAN_MONTH_NAMES = [
    "", "Január", "Február", "Március", "Április", "Május", "Június",
    "Július", "Augusztus", "Szeptember", "Október", "November", "December"
]

def get_month_name(month):
    return HUNGARIAN_MONTH_NAMES[month]

def generate_calendar_context(year, month, is_admin=False):
    """Naptár kontextus létrehozása."""
    cal = Calendar(firstweekday=0)
    month_days = list(cal.itermonthdates(year, month))

    availability_map = {
        a.date: a.status for a in Availability.objects.filter(date__year=year, date__month=month)
    }

    calendar_data = []
    for day in month_days:
        status = 'green' if day.month == month else 'empty'
        if day.month == month:
            status = availability_map.get(day, 'green')
        calendar_data.append({'date': day, 'status': status})

    calendar_data = [calendar_data[i:i + 7] for i in range(0, len(calendar_data), 7)]

    return {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'month_name': get_month_name(month),
        'days_of_week': ["H", "K", "Sz", "Cs", "P", "Szo", "V"],
        'prev_month': (month - 1) if month > 1 else 12,
        'prev_year': year - 1 if month == 1 else year,
        'next_month': (month + 1) if month < 12 else 1,
        'next_year': year + 1 if month == 12 else year,
        'is_admin': is_admin
    }

def calendar_view(request):
    """Vált a publikus és az admin naptár között."""
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    context = generate_calendar_context(year, month, is_admin=request.user.is_authenticated)
    template = 'admin_calendar.html' if request.user.is_authenticated else 'public_calendar.html'
    

    return render(request, template, context)

@login_required
def mark_days_unavailable(request):
    if request.method == 'POST':
        selected_dates = request.POST.getlist('selected_dates[]', [])
        if not selected_dates:
            return JsonResponse({'status': 'error', 'message': 'Nincsenek kijelölt dátumok.'}, status=400)

        for date_str in selected_dates:
            try:
                date_obj = date.fromisoformat(date_str)
                availability, created = Availability.objects.get_or_create(date=date_obj)
                availability.status = 'red' 
                availability.save()
            except ValueError:
                return JsonResponse({'status': 'error', 'message': f'Érvénytelen dátum: {date_str}'}, status=400)

        return JsonResponse({'status': 'success', 'message': f'{len(selected_dates)} nap foglaltra állítva.'})
    return JsonResponse({'status': 'error', 'message': 'Hibás kérés.'}, status=405)

@login_required
def mark_days_available(request):
    if request.method == 'POST':
        selected_dates = request.POST.getlist('selected_dates[]', [])
        if not selected_dates:
            return JsonResponse({'status': 'error', 'message': 'Nincsenek kijelölt dátumok.'}, status=400)

        for date_str in selected_dates:
            try:
                date_obj = date.fromisoformat(date_str)
                availability = Availability.objects.get(date=date_obj)
                availability.status = 'green'
                availability.delete()

            except ValueError:
                return JsonResponse({'status': 'error', 'message': f'Érvénytelen dátum: {date_str}'}, status=400)

        return JsonResponse({'status': 'success', 'message': f'{len(selected_dates)} nap szabadra állítva.'})
    return JsonResponse({'status': 'error', 'message': 'Hibás kérés.'}, status=405)


def main_site(request):
    packages = Package.objects.all()
    pictures = Photos.objects.filter(category__name="kutyafotózás")
    studiopictures = Photos.objects.filter(category__name="studio")
    reviews = load_more_reviews(request)
    return render(request, 'kutyafotozas.html',  {'pictures': pictures, 'studiopictures': studiopictures, 'title': 'szabadtéri kutyafotózás Budapesten és környékén', 'reviews': reviews, 'packages': packages})


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

    return render(request, 'intro.html', {'categories': categories, 'form': form, 'title': 'nagipix fotó és video | Budapest | kutyafotózás, esküvő és portré'})

def kapcsolat(request):
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "nagipix - érdeklődés weboldalon keresztül"
            body = {
                'name': 'Feladó: ' + form.cleaned_data['name'] + '\n',
                'email_address': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }

            message = (
                f"Üzenet érkezett a nagipix űrlapon keresztül:\n\n"
                f"{body['name']}"
                f"Email: {body['email_address']}\n\n"
                f"Üzenet:\n{body['message']}"
            )


            try:
                email = EmailMessage(
                            subject=subject, 
                            body=message,
                            from_email='brandbehozunk@gmail.com',
                            to=['info@nagipix.hu'],
                            reply_to=[body['email_address']],
                          )
                email.send()    
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")
        
    else:
        form = ContactForm()
        
    context = generate_calendar_context(year, month, is_admin=request.user.is_authenticated)
    context.update({'form': form})

    return render(request, "kapcsolat.html", context)
    
def blog(request):
    bloglist = BlogPost.objects.all().order_by('-created_at')
    
    return render(request, "blog.html", {"bloglist": bloglist, 'title': 'blog, blogposztok, értekezések és elmélkedések fotózásról'})

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost.html'
    context_object_name = 'blogpost'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        # Ezzel hozzáadhatod a címadatot a kontextushoz
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context
    
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
    
def calendar_partial_view(request):
    """A naptár részleges nézete, HTMX-hez."""
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    context = generate_calendar_context(year, month)
    return render(request, 'calendar_partial.html', context)

def sikeresmail(request):
    return render(request, 'sikeresmail.html', {'title': 'sikeres email küldés'})
