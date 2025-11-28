from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from adminapp.models import *
from legaladvocapp.models import *
from django.contrib import messages
from clientapp.models import client_case
# Create your views here.
def index(request):
    context={
        'categories':Category.objects.all()
    }
    return render(request,'index.html',context)

def userreg(request):
    return render(request,'user_reg.html')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the data in tblUser_Log
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usertype = "client"  # As you mentioned, we save this as a default
            user_log = tblUser_Log.objects.create(email=email, password=password, keyuser=usertype)
            
            # Save the data in tblUser_Reg (including the login_id reference)
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            purpose=form.cleaned_data['purpose']
            tblUser_Reg.objects.create(name=name, phone_number=phone_number, login=user_log,purpose=purpose)

            # Redirect to a success page or login page
            return render(request,'login.html')  # Adjust with your actual URL name for the login page

    else:
        form = UserRegistrationForm()

    return render(request, 'user_reg.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if the email exists in the tblUser_Log (login table)
            try:
                user_log = tblUser_Log.objects.get(email=email)
            except tblUser_Log.DoesNotExist:
                form.add_error('email', 'Email does not exist')
                return render(request, 'login.html', {'form': form})
            
            # Check if the password matches
            if user_log.password != password:
                form.add_error('password', 'Incorrect password')
                return render(request, 'login.html', {'form': form})
            
            # Determine the user type (client, advocate, or admin)
            user = None
            
            if user_log.keyuser == 'client':
                try:
                    user = tblUser_Reg.objects.get(login_id=user_log.id)
                except tblUser_Reg.DoesNotExist:
                    form.add_error('email', 'Client account not found.')
                    return render(request, 'login.html', {'form': form})
                # Redirect to client dashboard or appropriate page
                request.session['clientid'] = user.id
                context={
                    'categories':Category.objects.all(),
                    'advocates':tbladvocate.objects.all(),
                    'faqs':Help.objects.all()
                }
                return render(request, 'clientindex.html',context)

            elif user_log.keyuser == 'Advocate':
                try:
                    user = tbladvocate.objects.get(login_id=user_log.id)
                    
                    if user.status == "Pending":
                        form.add_error('email', 'You are not approved yet. Please try again later.')
                        return render(request, 'login.html', {'form': form})
                    elif user.status != "approved":
                        form.add_error('email', 'Advocate account not found or not approved.')
                        return render(request, 'login.html', {'form': form})

                except tbladvocate.DoesNotExist:
                    form.add_error('email', 'Advocate account not found.')
                    return render(request, 'login.html', {'form': form})

                # Redirect to advocate dashboard
                request.session['advocateid'] = user.id
                payment_status = user.payment_status
                return render(request, 'advocateindex.html', {'payment_status': payment_status})

            elif user_log.keyuser == 'admin':
                # Handle admin login and redirect to admin home
                context = {
            'total_clients': tblUser_Reg.objects.count(),
            'total_advocates': tbladvocate.objects.count(),
            'total_cases':client_case.objects.count(),
            'total_feedback':Contact.objects.count()
        }
                return render(request, 'admindex.html',context)

            # If user is not found or keyuser is unrecognized
            form.add_error('email', 'Invalid user type or account.')
            return render(request, 'login.html', {'form': form})

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



#register advocate
def register_advocate(request):
    if request.method == 'POST':
        user_log_form = UserLogForm(request.POST)
        advocate_form = AdvocateForm(request.POST, request.FILES)

        if user_log_form.is_valid() and advocate_form.is_valid():
            user_log = user_log_form.save(commit=False)
            user_log.keyuser = 'Advocate'
            user_log.save()

            advocate = advocate_form.save(commit=False)
            advocate.login = user_log
            advocate.status = 'pending'
            advocate.save()

            return render(request,'login.html')
        else:
            print("User Log Form Errors:", user_log_form.errors)
            print("Advocate Form Errors:", advocate_form.errors)
    else:
        user_log_form = UserLogForm()
        advocate_form = AdvocateForm()

    return render(request, 'advocate_reg.html', {
        'user_log_form': user_log_form,
        'advocate_form': advocate_form
    })
def about(request):
    return render(request,'about.html')
def index_ipc_section(request):
    obj=ipcsections.objects.all()
    return render(request,'ipc_section.html',{'sections':obj})
def index_advocates(request):
    obj=tbladvocate.objects.filter(status="Approved")
    return render(request,'advocateview.html',{'advocates':obj})
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})
def faqs_view(request):
    faqs = Help.objects.all()
    return render(request, 'view_help.html', {'faqs': faqs})
