from django.shortcuts import render,get_object_or_404,redirect # type: ignore
from django.contrib.auth import logout
from legaladvocapp.models import *
from adminapp.models import *
from .forms import *
from .models import client_case,PremiumUser,advocate_case,Booking
from django.contrib import messages
from advocate.models import CaseHistory,AdvocateAvailability
from django.utils.timezone import now, timedelta
from io import BytesIO
import qrcode
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from django.utils.text import capfirst
from datetime import datetime
# Create your views here.
def clientindex(request):
    context={
                    'categories':Category.objects.all(),
                    'advocates':tbladvocate.objects.all(),
                    'faqs':Help.objects.all()
                }
    return render(request,'clientindex.html',context)

def advocates(request):
    category_id = request.GET.get('category', None)
    if category_id:
        advocates = tbladvocate.objects.filter(category_id=category_id, status='approved')
    else:
        advocates = tbladvocate.objects.filter(status='approved')

    context = {
        'advocates': advocates,
        'categories': Category.objects.all(),
        'selected_category': category_id
    }
    return render(request, 'advocates.html', context)

def view_individual_advocate(request, id):
    user_id = request.session.get('clientid')  # Get the logged-in user ID
   
    is_premium = PremiumUser.objects.filter(client=user_id).exists()
    context={
    'advocate' : get_object_or_404(tbladvocate, id=id),
    'case_history':CaseHistory.objects.filter(advocate_id=id),
    'reviews':Review.objects.filter(advocate_id=id),
    'schedule':AdvocateAvailability.objects.filter(advocate_id=id),
    "is_premium": is_premium

    }
    
    return render(request, 'individual_advocate.html', context)
def purchase_premium(request):
   user_id = request.session.get('clientid')  # Get the logged-in user ID
   if request.method == "POST":
        if not PremiumUser.objects.filter(client_id=user_id).exists():
            premium = PremiumUser(client_id=user_id)  # 30-day validity
            premium.save()
        return redirect("clientindex")  # Redirect after purchase

   return render(request, "purchase_premium.html")
def chat_with_advocate(request, advocate_id):
    advocate = tbladvocate.objects.get(id=advocate_id)  # Get the specific advocate
    client = tblUser_Reg.objects.get(id=request.session['clientid'])  # Assuming the client is the logged-in user

    # Fetch all cases for the logged-in client
    client_cases = client_case.objects.filter(client=client)

    case = None
    if request.method == "POST":
        # If an existing case is selected
        if 'selected_case' in request.POST and request.POST['selected_case']:
            case_id = request.POST['selected_case']
            case = client_case.objects.get(id=case_id)  # Fetch the selected case
        
        # If a new case description is provided (we are not adding new cases, but the form needs to handle it)
        # we are skipping case creation, as per the request
        if 'message' in request.POST:
            message = request.POST['message']
            # Create a chat message related to the selected case or no case at all
            if case:
                Chat.objects.create(client=client, advocate=advocate, message=message, case=case)
            else:
                Chat.objects.create(client=client, advocate=advocate, message=message)

    # Fetch all chats between the client and advocate
    chats = Chat.objects.filter(client=client, advocate=advocate).order_by('timestamp')

    return render(request, 'chat.html', {
        'advocate': advocate,
        'chats': chats,
        'client_cases': client_cases,  # Pass the client's cases to the template
        'case': case,
    })



def clientchat_page_view(request, advocate_id=None):
    client_id = request.session.get('clientid')
    if not client_id:
        return redirect('login_view')

    client = get_object_or_404(tblUser_Reg, id=client_id)
    chats = Chat.objects.filter(client=client).order_by('timestamp')
    
    # Prepare a dictionary to group chats by client
    advocate_data = {}
    for chat in chats:
        if chat.advocate.id not in advocate_data:
            advocate_data[chat.advocate.id] = {
                'advocate': chat.advocate,
                'last_message': chat
            }
        elif chat.timestamp > advocate_data[chat.advocate.id]['last_message'].timestamp:
            advocate_data[chat.advocate.id]['last_message'] = chat

    advocate_threads = list(advocate_data.values())
    advocate_threads.sort(key=lambda x: x['last_message'].timestamp, reverse=True)

    selected_advocate = None
    messages = None
    if advocate_id:
        selected_advocate = get_object_or_404(tbladvocate, id=advocate_id)
        if request.method == "POST":
            message_text = request.POST.get("message")
            file_upload = request.FILES.get('attachment', None)
            if message_text:
                # If you have a sender field in your model, specify it:
                # For example, if the logged-in user is the advocate:
                Chat.objects.create(
                    advocate=selected_advocate,
                    client=client,
                    message=message_text,
                    attachment=file_upload,
                    sender='client'  # or 'client' if appropriate
                )
                # After saving, redirect to avoid form resubmission
                return redirect('clientchat', advocate_id=advocate_id)

        messages = Chat.objects.filter(advocate=selected_advocate, client=client).order_by('timestamp')

    context = {
        'advocate_threads': advocate_threads,
        'client': client,
        'selected_advocate': selected_advocate,
        'messages': messages,
    }
    return render(request, 'clientchat_list.html', context)

def user_logout(request):
    logout(request)
    return render(request,'index.html') 
def delete_conversation(request, advocate_id):
    client_id = request.session.get('clientid')
    if not client_id:
        return redirect('login_view')

    client = get_object_or_404(tblUser_Reg, id=client_id)
    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    
    # Delete all chat messages between this client and advocate
    Chat.objects.filter(client=client, advocate=advocate).delete()
    
    # Redirect back to the chat list page after deletion
    return redirect('clientchat')
def delete_message(request, message_id):
    client_id = request.session.get('clientid')
    if not client_id:
        return redirect('login_view')
    
    # Ensure that the client has permission to delete this message
    message = get_object_or_404(Chat, id=message_id, client__id=client_id)
    message.delete()
    # Redirect back to the chat conversation. If you need to redirect to the conversation,
    # you might extract the advocate_id from message and then redirect.
    return redirect('clientchat', advocate_id=message.advocate.id)

#review
def review_advocate(request, advocate_id):
    # Retrieve the client from session
    client_id = request.session.get('clientid')
    if not client_id:
        return redirect('login_view')  # or your login URL
    
    client = get_object_or_404(tblUser_Reg, id=client_id)
    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    
    # Check if a review already exists for this advocate from the client
    review_instance = Review.objects.filter(client=client, advocate=advocate).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review_instance)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = client
            review.advocate = advocate
            review.save()
            # Redirect to a confirmation page or back to the advocate detail page
            return redirect('advocate', advocate_id=advocate.id)
    else:
        form = ReviewForm(instance=review_instance)
    
    context = {
        'form': form,
        'advocate': advocate,
    }
    return render(request, 'review.html', context)


#for review
def submit_review(request, advocate_id):
    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    user=request.session['clientid']
    
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        if 1 <= rating <= 5:
            Review.objects.create(
                advocate=advocate,
                client_id=user,
                rating=rating,
                review=comment
            )
            messages.success(request, "Your review has been submitted!")
        else:
            messages.error(request, "Invalid rating. Please select between 1 and 5.")

    return redirect('view_individual_advocate', id=advocate_id)
def generate_qr(request):
    upi_id = "yourupiid@upi"  # Replace with your actual UPI ID
    amount = 200
    upi_url = f"upi://pay?pa={upi_id}&pn=Premium%20Access&am={amount}&cu=INR"

    qr = qrcode.make(upi_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

def get_advocates_by_category(request):
    category_id = request.GET.get("category_id")
    advocates = tbladvocate.objects.filter(category_id=category_id, status="approved",).values("id", "name", "phone_number", "photo")

    # Append the full URL to the photo field
    advocate_list = []
    for advocate in advocates:
        advocate_list.append({
            "id": advocate["id"],
            "name": advocate["name"],
            "phone_number": advocate["phone_number"],
            "photo": f"{settings.MEDIA_URL}{advocate['photo']}" if advocate["photo"] else None
        })

    return JsonResponse({"advocates": advocate_list})

def fix_advocate(request):
    if request.method == "POST":
        advocate_id = request.POST.get("advocate_id")
        case_id = request.POST.get("case_id")

        # Ensure advocate and case exist
        try:
            case = client_case.objects.get(id=case_id)
            advocate = tbladvocate.objects.get(id=advocate_id)

            # Check if the case is already assigned to an advocate
            if advocate_case.objects.filter(case=case).exists():
                return JsonResponse({"status": "warning", "message": "Advocate already assigned for this case!"})

            # Save the advocate selection
            advocate_case.objects.create(
                case=case,
                advocate=advocate
            )

            return JsonResponse({"status": "success", "message": "Request sent successfully!"})

        except client_case.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Case not found!"})
        except tbladvocate.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Advocate not found!"})

    return JsonResponse({"status": "error", "message": "Invalid request!"})
def submit_case(request):
    user_id = request.session.get('clientid')  
    if request.method == 'POST':
        form = ClientCaseForm(request.POST)
        if form.is_valid():
            client_case_form = form.save(commit=False)
            client_case_form.client_id = user_id  
            client_case_form.save()
            return redirect('submit_case')  

    else:
        form = ClientCaseForm()

    categories = Category.objects.all()
    mycases = client_case.objects.filter(client_id=user_id).order_by('-id')  

    # Convert dictionary to a list for easier template rendering
    case_advocates = []
    for case in mycases:
        advocate_case_obj = advocate_case.objects.filter(case=case).select_related('advocate').first()
        if advocate_case_obj:
            case_advocates.append({
                "case_id": case.id,
                "advocate": advocate_case_obj.advocate,
                "status": advocate_case_obj.status
            })

    return render(
        request, 
        'client_case_form.html', 
        {'form': form, 'categories': categories, 'mycases': mycases, 'case_advocates': case_advocates}
    )








# def submit_case(request):
#     user_id = request.session.get('clientid')  

#     if request.method == 'POST':
#         form = ClientCaseForm(request.POST)
#         if form.is_valid():
#             client_case_form = form.save(commit=False)
#             client_case_form.client_id = user_id  
#             client_case_form.save()
#             return redirect('submit_case')  
#     else:
#         form = ClientCaseForm()

#     categories = Category.objects.all()
#     mycases = client_case.objects.filter(client_id=user_id).order_by('-id')

#     # Fetch all advocate_case entries for the client's cases
#     case_advocates = advocate_case.objects.filter(case__in=mycases).select_related('advocate')

#     # Convert to dictionary for quick lookup
#     case_advocate_dict = {adv_case.case_id: adv_case for adv_case in case_advocates}

#     return render(
#         request, 
#         'client_case_form.html', 
#         {
#             'form': form, 
#             'categories': categories, 
#             'mycases': mycases, 
#             'case_advocate_dict': case_advocate_dict
#         }
#     )


def update_payment_status(request):
    if request.method == "POST":
        case_id = request.POST.get("case_id")
        try:
            advocate_case_obj = advocate_case.objects.get(case_id=case_id)
            advocate_case_obj.payment_status = "Payment Completed"
            advocate_case_obj.save()
            return JsonResponse({"status": "success", "message": "Payment completed successfully!"})
        except advocate_case.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid case ID"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


def generate_qr_code_advance(request, case_id):
    # Check if payment is already completed for this case
    try:
        advocate_case_obj = advocate_case.objects.get(case_id=case_id)
        if advocate_case_obj.payment_status == "Payment Completed":
            return JsonResponse({"status": "error", "message": "Payment already completed for this case!"})
    except advocate_case.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Case not found!"})

    upi_id = "your_upi_id@upi"  # Replace with actual UPI ID
    amount = "2500"  # Fixed amount for the case payment
    payee_name = "YourName"  # Replace with actual payee name
    transaction_note = f"Payment for Case {case_id}"

    # Generate UPI payment URL
    payment_url = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR&tn={transaction_note}"

    # Generate QR Code
    qr = qrcode.make(payment_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


# def view_schedule(request, advocate_id):
#     advocate = get_object_or_404(tbladvocate, id=advocate_id)
#     schedule = AdvocateAvailability.objects.filter(advocate_id=advocate_id)

#     # Initialize schedule matrix with None values
#     schedule_matrix = {
#         "Monday": {"morning": None, "afternoon": None, "evening": None},
#         "Tuesday": {"morning": None, "afternoon": None, "evening": None},
#         "Wednesday": {"morning": None, "afternoon": None, "evening": None},
#         "Thursday": {"morning": None, "afternoon": None, "evening": None},
#         "Friday": {"morning": None, "afternoon": None, "evening": None},
#         "Saturday": {"morning": None, "afternoon": None, "evening": None},
#         "Sunday": {"morning": None, "afternoon": None, "evening": None},
#     }

#     for slot in schedule:
#         day_name = capfirst(slot.day)  # Capitalize first letter (e.g., 'monday' -> 'Monday')
#         if day_name in schedule_matrix and slot.time_slot in schedule_matrix[day_name]:
#             schedule_matrix[day_name][slot.time_slot] = {
#                 "id": slot.id,  # Store the availability ID
#                 "time": f"{slot.start_time} - {slot.end_time}"
#             }

#     return render(request, 'view_schedule.html', {'advocate': advocate, 'schedule_matrix': schedule_matrix})



def view_schedule(request, advocate_id):
    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    
    today = datetime.today().date()
    schedule_matrix = {}  # Dictionary to store the schedule

    # Loop through the next 7 days (starting from tomorrow)
    for i in range(1, 8):  # Start from 1 to skip today
        future_date = today + timedelta(days=i)
        weekday = future_date.strftime('%A')  # Get full weekday name (e.g., "Friday")
        date_str = future_date.strftime('%d-%m-%Y')  # Format date as DD-MM-YYYY

        # Get available slots for the advocate on this day
        slots = AdvocateAvailability.objects.filter(advocate=advocate, day=weekday).order_by('start_time')

        # Structure data for display
        schedule_matrix[date_str] = {
            "day": weekday,
            "slots": {
                "morning": None,
                "afternoon": None,
                "evening": None
            }
        }

        for slot in slots:
            if slot.start_time.hour < 12:
                schedule_matrix[date_str]["slots"]["morning"] = slot
            elif 12 <= slot.start_time.hour < 17:
                schedule_matrix[date_str]["slots"]["afternoon"] = slot
            else:
                schedule_matrix[date_str]["slots"]["evening"] = slot

    return render(request, 'view_schedule.html', {
        'advocate': advocate,
        'schedule_matrix': schedule_matrix
    })
def book(request, advocate_id, availability_id):
    print("Inside booking function")

    client_id = request.session.get('clientid')
    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    availability = get_object_or_404(AdvocateAvailability, id=availability_id)
    
    # Get date from request
    booking_date = request.GET.get('date')  
    print(f"Received Booking Date: {booking_date}")

    if not booking_date:
        messages.error(request, "Invalid booking date.")
        return redirect('view_schedule', advocate_id=advocate_id)
    
    # Convert DD-MM-YYYY to YYYY-MM-DD
    try:
        booking_date = datetime.strptime(booking_date, "%d-%m-%Y").date()
        print(f"Formatted Booking Date: {booking_date}")  # Debugging
    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect('view_schedule', advocate_id=advocate_id)

    # Check if booking already exists
    if Booking.objects.filter(client_id=client_id, advocate=advocate, availability=availability, date=booking_date).exists():
        messages.error(request, "You have already booked this slot on this date.")
        return redirect('view_schedule', advocate_id=advocate_id)

    # Save booking with date
    Booking.objects.create(client_id=client_id, advocate=advocate, availability=availability, date=booking_date)
    messages.success(request, f"Your appointment has been booked for {booking_date}!")
    
    return redirect('view_schedule', advocate_id=advocate_id)


def check_payment_status(request):
    case_id = request.GET.get("case_id")

    try:
        advocate_case_obj = advocate_case.objects.get(case_id=case_id)
        if advocate_case_obj.payment_status == "Payment Completed":
            return JsonResponse({"status": "error", "message": "Payment already completed for this case!"})
        else:
            return JsonResponse({"status": "success"})  # Allow QR code to be generated
    except advocate_case.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Case not found!"})
