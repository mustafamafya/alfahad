from django.urls import path
from .views import main, delete_loaner ,payment, delete_payment, print_card , login_view , logout_view

urlpatterns = [
    path('', main, name='main'),
    path('delete/<int:pk>/', delete_loaner, name='delete_loaner'),
    path('payment/<int:pk>/', payment, name='payment'),
    path('delete_payment/<int:pk>/', delete_payment, name='delete_payment'),
    path('print_card/<int:pk>/', print_card, name='print_card'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]