from django.shortcuts import render
from .models import Portfolio, Contanct
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .contact import ContactForm
from django.http import HttpResponseRedirect

def port(request):
    projects = Portfolio.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'project.html', context)




def data_contact(request):
    contact_data = Contanct.objects.all()
    context = {
        'contact_data' : contact_data
    }
    return render (request, 'contact.html', context)




def project_detail(request, pk):
    project = Portfolio.objects.get(pk=pk)
    context = {
        'project': project
    }
    return render(request, 'detail.html', context)



def cv(request):
    return render(request, 'cv.html')



def website(request):
    return render(request, 'website.html')

# def user_data(request):
#     if request.method == 'POST':
#         name = request.POST.get('Name')
#         lastname = request.POST.get('Last_name')
#         mobile = request.POST.get('Mobile')
#         subject = request.POST.get('Subject')
#         message = request.POST.get('Message')
#         country = request.POST.get('Country')
#         email = request.POST.get('Email')
#         new_contact = contact(name = name, lastname= lastname, mobile=mobile, subject = subject, message = message, country= country, email = email)
#         new_contact.save()
#     return render(request, 'contact.html')


def contact(request):
    if request.method == 'POST':
        
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            country = form.cleaned_data['country']
            mobile = form.cleaned_data['mobile']
            Contanct.objects.create(name = name, email = email, subject = subject, message = message, country = country, mobile = mobile)
            send_mail(name, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL], fail_silently=False)
            return render(request, "thanks.html")
         
            
    
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'contact.html', context)



def thanks(request):
    return HttpResponseRedirect(request, "thanks.html")
