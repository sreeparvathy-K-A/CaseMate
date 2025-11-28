from django.urls import path
from .import views
from .views import advocate_logout
from .views import add_case_history
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('advocateindex/',views.advocateindex,name="advocateindex"),
    path('add_case_history', views.add_case_history, name='add_case_history'),
    path('view_request', views.view_request, name='view_request'),
    path('start_chat', views.start_chat, name='start_chat'),
   path('view_review', views.view_review, name='view_review'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('advocate_logout/',views.advocate_logout, name='advocate_logout'),
 path('chat/', views.chat_page_view, name='chat'),
    path('chat/<int:client_id>/', views.chat_page_view, name='chat'),
    path('chat/delete/<int:client_id>/', views.delete_conversation, name='delete_conversation'),
     path('chat/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
      path('payment_view/', views.payment_view, name='payment_view'),
      path('my_review/', views.my_review, name='my_review'),
     path('my_cases/', views.my_cases, name='my_cases'),
     
path('approve-case/', views.approve_case, name='approve_case'),
    path('reject-case/', views.reject_case, name='reject_case'),
     path('add_availability/', views.add_availability, name='add_availability'),
    path('view_availability/', views.view_availability, name='view_availability'),
    path('advocate_bookings/', views.advocate_bookings, name="advocate_bookings"),
 path('advocate_booking_page/', views.advocate_booking_page, name="advocate_booking_page"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
