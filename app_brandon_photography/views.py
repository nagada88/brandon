from django.shortcuts import render,redirect
from .models import *
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# Create your views here.

def bio(request):
    return render(request, 'bio.html', {})

def video(request):
    return render(request, 'video.html', {})

def foto(request):
    categories = PhotoCategory.objects.all().order_by('priority')
    # for category in categories:
    #     category.get_category_cover()
    return render(request, 'foto.html', {'categories': categories})

def gallery(request):

    category_id = request.GET.get('gallery_id')
    if category_id:
        pictures = Photos.objects.filter(category=category_id)
    else:
        pictures = Photos.objects.filter(main_site_visibility=True)

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


    return render(request, 'gallery.html', {'pictures': pictures, 'breakpnumber': breakpnumber, 'bplist': bplist})

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