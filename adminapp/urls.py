from django.urls import path
from .import views
from .views import admin_logout

urlpatterns = [

path('adminhome',views.admindex,name="adminhome"),
 path('add_category', views.add_category, name='add_category'),
    path('delete_category', views.delete_category, name='delete_category'),
    
  path('add_section/', views.add_section, name='add_section'),
    path('delete_section/', views.delete_section, name='delete_section'),
    path('ipc_sections_view/', views.ipc_sections_view, name='ipc_sections_view'),
    
  path('add_court/', views.add_court, name='add_court'),
    path('delete_court/', views.delete_court, name='delete_court'),
    path('court_view/', views.court_view, name='court_view'),

    path('approve_advocate/<int:id>/', views.approve_advocate, name='approve_advocate'),
    path('reject_advocate/<int:id>/', views.reject_advocate, name='reject_advocate'),
    path('adminadvocate_list/', views.adminadvocate_list, name='adminadvocate_list'),
     path('approvedadv_list/', views.approvedadv_list, name='approvedadv_list'),
    path('rejectedadv_list/', views.rejectedadv_list, name='rejectedadv_list'),
    path('client_list/', views.client_list, name='client_list'),
    
    path("help_list/", views.help_view, name="help_list"),
    path("help/delete/<int:help_id>/", views.delete_help, name="delete_help"),

    path("feedback_view/", views.feedback_view, name="feedback_view"),
     path('admin_logout/',views.admin_logout, name='admin_logout'),
     path('admin_case_list/',views.admin_case_list, name='admin_case_list'),
          path('payment_dashboard/',views.payment_dashboard, name='payment_dashboard'),
      ]


    