from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import logout
from adminapp.models import *
from legaladvocapp.models import *
from clientapp.models import Chat,Review,advocate_case,Booking
from .forms import CaseHistoryForm,AdvocateAvailabilityForm
import qrcode
import base64
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.
def advocateindex(request):
    obj=tbladvocate.objects.get(id=request.session['advocateid'])
    payment_status=obj.payment_status
    return render(request,'advocateindex.html',{'payment_status':payment_status})
def add_case_history(request):
    return render(request,'casehistory.html')

def view_request(request):
    return render(request,'request.html')

def start_chat(request):
    return render(request,'chat.html')

def view_review(request):
    return render(request,'review.html')

def edit_profile(request):
     return render(request,'profile.html')



def add_case_history(request):
    advocates = tbladvocate.objects.all()
    categories = Category.objects.all()
    courts = court.objects.all()

    if request.method == "POST":
        form = CaseHistoryForm(request.POST)
        if form.is_valid():
            case_history = form.save(commit=False)
            # Assuming the advocate's id is stored in session under 'advocate_id'
            advocate_id = request.session.get('advocateid')
            case_history.advocate_id = advocate_id  # Set the advocate id field
            case_history.save()
            return redirect('advocateindex')  # Redirect to a success page or case list page

    else:
        form = CaseHistoryForm()

    return render(request, "case_history.html", {
        "form": form,
        "advocates": advocates,
        "categories": categories,
        "courts": courts
    })

#logout

def advocate_logout(request):
    logout(request)
    return render(request,'index.html') 
def chat_page_view(request, client_id=None):
    advocate_id = request.session.get('advocateid')
    if not advocate_id:
        return redirect('login_view')

    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    chats = Chat.objects.filter(advocate=advocate).order_by('timestamp')
    
    # Prepare a dictionary to group chats by client
    clients_data = {}
    for chat in chats:
        if chat.client.id not in clients_data:
            clients_data[chat.client.id] = {
                'client': chat.client,
                'last_message': chat
            }
        elif chat.timestamp > clients_data[chat.client.id]['last_message'].timestamp:
            clients_data[chat.client.id]['last_message'] = chat

    client_threads = list(clients_data.values())
    client_threads.sort(key=lambda x: x['last_message'].timestamp, reverse=True)

    selected_client = None
    messages = None
    if client_id:
        selected_client = get_object_or_404(tblUser_Reg, id=client_id)
        if request.method == "POST":
            message_text = request.POST.get("message")
            file_upload = request.FILES.get('attachment', None)
            if message_text:
                # If you have a sender field in your model, specify it:
                # For example, if the logged-in user is the advocate:
                Chat.objects.create(
                    advocate=advocate,
                    client=selected_client,
                    message=message_text,
                    attachment=file_upload,
                    sender='advocate'  # or 'client' if appropriate
                )
                # After saving, redirect to avoid form resubmission
                return redirect('chat', client_id=client_id)

        messages = Chat.objects.filter(advocate=advocate, client=selected_client).order_by('timestamp')

    context = {
        'advocate': advocate,
        'client_threads': client_threads,
        'selected_client': selected_client,
        'messages': messages,
    }
    return render(request, 'chat_list.html', context)

def delete_conversation(request, client_id):
    advocate_id = request.session.get('advocateid')
    if not advocate_id:
        return redirect('login_view')

    client = get_object_or_404(tblUser_Reg, id=client_id)
    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    
    # Delete all chat messages between this client and advocate
    Chat.objects.filter(client=client, advocate=advocate).delete()
    
    # Redirect back to the chat list page after deletion
    return redirect('chat')
def delete_message(request, message_id):
    advocate_id = request.session.get('advocateid')
    if not advocate_id:
        return redirect('login_view')
    
    # Ensure that the advocate has permission to delete this message
    message = get_object_or_404(Chat, id=message_id, advocate__id=advocate_id)
    message.delete()
    # Redirect back to the chat conversation. If you need to redirect to the conversation,
    # you might extract the client_id from message and then redirect.
    return redirect('chat', client_id=message.client.id)
def payment_view(request):
    advocate = tbladvocate.objects.get(id=request.session.get('advocateid'))

    if advocate.payment_status == "Completed":
        return redirect('advocateindex')  # Redirect if payment is already done

    # Generate QR Code (Replace with actual UPI payment link)
    payment_link = "upi://pay?pa=your-upi-id@upi&pn=CaseMate&mc=123456&tid=unique_transaction_id&tr=1000&cu=INR"

    qr = qrcode.make(payment_link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    if request.method == "POST":
        advocate.payment_status = "Completed"
        advocate.save()
        return redirect('payment_view')

    return render(request, 'complete_payment.html', {'qr_code': f"data:image/png;base64,{qr_base64}"})

def my_review(request):
    reviews=Review.objects.filter(advocate_id=request.session.get('advocateid'))
    return render(request,'my_reivews.html',{'reviews':reviews})

def my_cases(request):
    advocate_id = request.session.get('advocateid')
    
    # Fetch cases assigned to this advocate
    cases = advocate_case.objects.filter(advocate=advocate_id)

    # Separate pending and approved cases
    pending_cases = cases.filter(status="Pending")
    approved_cases = cases.exclude(status="Pending")  # Cases that are not pending

    return render(request, 'my_cases.html', {
        'pending_cases': pending_cases,
        'approved_cases': approved_cases
    })
def approve_case(request):
    if request.method == "POST":
        case_id = request.POST.get("case_id")
        try:
            case = advocate_case.objects.get(id=case_id)
            case.status = "Approved"
            case.save()
            return JsonResponse({"status": "success"})
        except advocate_case.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Case not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})

@csrf_exempt
def reject_case(request):
    if request.method == "POST":
        case_id = request.POST.get("case_id")
        try:
            case = advocate_case.objects.get(id=case_id)
            case.status = "Rejected"
            case.save()
            return JsonResponse({"status": "success"})
        except advocate_case.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Case not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


def add_availability(request):
    advocate_id = request.session.get('advocateid')  # Get advocate_id safely

    if not advocate_id:  # Ensure advocate_id is present
        messages.error(request, "Session expired! Please log in again.")
        return redirect('login')

    if request.method == "POST":
        form = AdvocateAvailabilityForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            time_slot = form.cleaned_data['time_slot']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # Check for existing schedule
            if AdvocateAvailability.objects.filter(advocate_id=advocate_id, day=day, time_slot=time_slot).exists():
                messages.error(request, f"Schedule for {day} ({time_slot}) already exists!")
            else:
                AdvocateAvailability.objects.create(
                    advocate_id=advocate_id,
                    day=day,
                    time_slot=time_slot,
                    start_time=start_time,
                    end_time=end_time
                )
                messages.success(request, "Schedule added successfully!")

            return redirect('add_availability')

    else:
        form = AdvocateAvailabilityForm()

    # Fetch all schedules for matrix display
    schedules = AdvocateAvailability.objects.filter(advocate_id=advocate_id)

    # Prepare matrix data
    availability_matrix = {day[0]: {'morning': "-", 'afternoon': "-", 'evening': "-"} for day in WEEKDAYS}
    for schedule in schedules:
        availability_matrix[schedule.day][schedule.time_slot] = f"{schedule.start_time} - {schedule.end_time}"

    return render(request, 'add_availability.html', {'form': form, 'availability_matrix': availability_matrix})

def view_availability(request):
    availabilities = AdvocateAvailability.objects.filter(advocate= request.session('advocateid'))
    return render(request, 'view_availability.html', {'availabilities': availabilities})



#advocate view booking
def advocate_bookings(request):
    advocate_id = request.session.get('advocateid')
    if not advocate_id:
        return JsonResponse([], safe=False)  # Return empty JSON if no advocate found

    advocate = get_object_or_404(tbladvocate, id=advocate_id)
    bookings = Booking.objects.filter(advocate=advocate).select_related('availability')

    # Convert bookings to FullCalendar format
    events = {}
    for booking in bookings:
        booking_date = booking.date.strftime("%Y-%m-%d")
        time_slot = booking.availability.time_slot
        start_time = booking.availability.start_time.strftime("%I:%M %p")  # Format as HH:MM AM/PM
        end_time = booking.availability.end_time.strftime("%I:%M %p")

        if booking_date in events:
            events[booking_date]["extendedProps"]["clients"].append({
                "name": booking.client.name,
                "time_slot": time_slot,
                "start_time": start_time,
                "end_time": end_time
            })
            events[booking_date]["title"] = f"{len(events[booking_date]['extendedProps']['clients'])} Booking(s)"
        else:
            events[booking_date] = {
                "title": "1 Booking(s)",
                "start": booking_date,
                "extendedProps": {
                    "clients": [{
                        "name": booking.client.name,
                        "time_slot": time_slot,
                        "start_time": start_time,
                        "end_time": end_time
                    }]
                }
            }

    return JsonResponse(list(events.values()), safe=False)  # Send JSON response

def advocate_booking_page(request):
    return render(request, "adv_view_booking.html")  