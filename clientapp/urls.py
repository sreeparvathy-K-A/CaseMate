from django.urls import path # type: ignore
from .import views
from .views import user_logout

urlpatterns = [

path('clientindex/',views.clientindex,name="clientindex"),
path('advocates/',views.advocates,name="advocates"),
path('submit_case/',views.submit_case,name="submit_case"),
    path('view_individual_advocate/<int:id>/', views.view_individual_advocate, name='view_individual_advocate'),
    path('chat_with_advocate/<int:advocate_id>/', views.chat_with_advocate, name='chat_with_advocate'),
   # path('advocate/<int:advocate_id>/cases/', views.case_history, name='case_history'),
    path('user_logout/',views.user_logout, name='user_logout'),

    path('clientchat/', views.clientchat_page_view, name='clientchat'),
    path('clientchat/<int:advocate_id>/', views.clientchat_page_view, name='clientchat'),
     path('clientchat/delete/<int:advocate_id>/', views.delete_conversation, name='delete_conversation'),
     path('clientchat/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

     #review
     path('submit_review/<int:advocate_id>/', views.submit_review, name='submit_review'),
    path('purchase_premium/', views.purchase_premium, name='purchase_premium'),
     path('generate_qr/', views.generate_qr, name='generate_qr'),
 path("get_advocates_by_category/", views.get_advocates_by_category, name="get_advocates_by_category"),
 path('fix_advocate/', views.fix_advocate, name='fix_advocate'),
path('update_payment_status/', views.update_payment_status, name='update_payment_status'),
path('generate_qr_code_advance/<int:case_id>', views.generate_qr_code_advance, name='generate_qr_code_advance'),
 path('schedule/<int:advocate_id>/', views.view_schedule, name='view_schedule'),
    path('book/<int:advocate_id>/<int:availability_id>/', views.book, name='book'),
    path('check_payment_status/', views.check_payment_status, name='check_payment_status'),
]
