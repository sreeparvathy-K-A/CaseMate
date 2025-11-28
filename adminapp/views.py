#from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout
from legaladvocapp.models import tbladvocate,Contact
from legaladvocapp.models import tblUser_Reg
from .models import *
from .forms import *
from clientapp.models import advocate_case,client_case,PremiumUser

# Create your views here.
def admindex(request):
    return render(request,'admindex.html')




def add_category(request):
    if request.method == 'POST':
        categoryname = request.POST.get('categoryname')
        description = request.POST.get('description')
        
        # Create the category
        category = Category.objects.create(categoryname=categoryname, description=description)
        
        # Return the category data as JSON for the client to update the page
        return JsonResponse({
            'id': category.id,
            'categoryname': category.categoryname,
            'description': category.description,
        })
    categories = Category.objects.all()  # Get all IPC sections
    #return render(request, 'ipc.html', {'ipcsection': ipcsection})
    return render(request, 'category.html',{'categories': categories})

def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        category.delete()

        return JsonResponse({'message': 'Category deleted successfully'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
#add ipc section
def add_section(request):
    if request.method == 'POST':
        section_name = request.POST.get('sections')
        description = request.POST.get('description')
        
        # Create the new section
        new_section = ipcsections.objects.create(
            sections=section_name,
            description=description
        )
        
        # Redirect back to the page to show the updated list
        return redirect('ipc_sections_view')  # Replace 'your_view_name' with the name of the view that renders the IPC section list
    
    return redirect('ipc_sections_view') # Replace with your template if needed

def delete_section(request):
    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        ipcsection = ipcsections.objects.get(id=section_id)
        ipcsection.delete()

        # Redirect back to the page to show the updated list
        return redirect('ipc_sections_view')  # Replace 'your_view_name' with the name of the view that renders the IPC section list
    
    return redirect('ipc_sections_view') 
def ipc_sections_view(request):
    ipcsection = ipcsections.objects.all()  # Get all IPC sections
    return render(request, 'ipc.html', {'ipcsection': ipcsection})

#add court
def add_court(request):
    if request.method == 'POST':
        courtname = request.POST.get('court')
        
        
        # Create the new section
        new_court = court.objects.create(
            courtname=courtname,
            
        )
        
        # Redirect back to the page to show the updated list
        return redirect('court_view')  # Replace 'your_view_name' with the name of the view that renders the court list
    
    return redirect('court_view')  # Replace with your template if needed

def delete_court(request):
    if request.method == 'POST':
        court_id = request.POST.get('court_id')
        courtname = court.objects.get(id=court_id)
        courtname.delete()

        # Redirect back to the page to show the updated list
        return redirect('court_view')  # Replace 'your_view_name' with the name of the view that renders the IPC section list
    
    return redirect('court_view') 
def court_view(request):
    courtname = court.objects.all()  # Get all court
    return render(request, 'court.html', {'court': courtname})


#feedback

# def delete_feddback(request):
#     if request.method == 'POST':
#         feedback_id = request.POST.get('feedback_id')
#         feedbackname = feedback.objects.get(id=feedback_id)
#         feedbackname.delete()

#         # Redirect back to the page to show the updated list
#         return redirect('feedback_view')  # Replace 'your_view_name' with the name of the view that renders the IPC section list
    
#     return redirect('feedback_view') 
def feedback_view(request):
    feedbackname = Contact.objects.all()  # Get all court
    return render(request, 'feedback.html', {'feedbacks': feedbackname})


#view advocate

def adminadvocate_list(request):
    advocates = tbladvocate.objects.filter(status="pending")
    return render(request, 'adminadvocateview.html', {'advocates': advocates})
def approvedadv_list(request):
    advocates = tbladvocate.objects.filter(status="approved")
    return render(request, 'adminadvocateview.html', {'advocates': advocates})
def rejectedadv_list(request):
    advocates = tbladvocate.objects.filter(status="rejected")
    return render(request, 'adminadvocateview.html', {'advocates': advocates})
# View for approving an advocate
def approve_advocate(request, id):
    advocate = tbladvocate.objects.get(id=id)
    advocate.status = 'approved'
    advocate.save()
    return redirect('adminadvocate_list')

# View for rejecting an advocate
def reject_advocate(request, id):
    advocate = tbladvocate.objects.get(id=id)
    advocate.status = 'rejected'
    advocate.save()
    return redirect('approvedadv_list')

# View to display the list of clients
def client_list(request):
    clients = tblUser_Reg.objects.all()  # Fetch all clients
    return render(request, 'clientview.html', {'clients': clients})

# View to display all help entries (FAQs)
def help_view(request):
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        if question and answer:
            Help.objects.create(question=question, answer=answer)
        return redirect("help_list")

    help_items = Help.objects.all()
    return render(request, "help.html", {"help_items": help_items})

def delete_help(request, help_id):
    Help.objects.filter(id=help_id).delete()
    return redirect("help_list")


#logout
def admin_logout(request):
    logout(request)
    return render(request,'index.html') 

def admin_case_list(request):
    caselist = advocate_case.objects.select_related('case', 'advocate').order_by('-created_at')
    print (caselist)
    return render(request,'case_list.html',{'caselist':caselist})
def payment_dashboard(request):
    premium_users = PremiumUser.objects.all()
    completed_advocates = tbladvocate.objects.filter(payment_status='Completed')
    pending_advocates = tbladvocate.objects.filter(payment_status='Pending')

    context = {
        'premium_users': premium_users,
        'completed_advocates': completed_advocates,
        'pending_advocates': pending_advocates
    }
    return render(request, 'admin_view_payment.html', context)

