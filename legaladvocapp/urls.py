from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name=""),
   path('userreg',views.userreg,name='userreg'),
   path('register/', views.register, name='register'),
  path('about',views.about,name='about'),
  path('index_ipc_section',views.index_ipc_section,name='index_ipc_section'),
 path('index_advocates',views.index_advocates,name='index_advocates'),
path("contact/", views.contact_view, name="contact"),
path("faqs_view/", views.faqs_view, name="faqs_view"),
   path('login',views.login_view,name='login_view'),
    path('register_advocate/', views.register_advocate, name='register_advocate'),
    
   # path('success/', views.success, name='success'),  # A placeholder for success page

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)