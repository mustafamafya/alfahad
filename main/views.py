# for handling views and rendering templates
from django.shortcuts import render ,get_object_or_404, redirect
# models
from .models import Loaner ,Payment
# for handling decimal values
from decimal import Decimal
# for handling forms and messages
from django.views.decorators.http import require_POST
from django.contrib import messages
# for pagination and search functionality
from django.core.paginator import Paginator
# for handling query parameters
from django.db.models import Q
# login functionality
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# for supporting arabic language in recipts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(APP_DIR, 'fonts')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')  # Already logged in

    next_url = request.GET.get('next', 'main')  # Redirect after login

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة")

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def main(request):
    # Handle form submission
    if request.method == 'POST':
        name = request.POST.get('name')
        total_amount = request.POST.get('total_amount')
        if name and total_amount:
            Loaner.objects.create(name=name, total_amount=total_amount)
        return redirect('main')  # Prevent resubmission on refresh

    # for search functionality and pagination
    query = request.GET.get('q', '')
    loaners = Loaner.objects.all()

    if query:
        loaners = loaners.filter(name__icontains=query)

    loaners = loaners.order_by('-id')  # Newest first
    paginator = Paginator(loaners, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main.html', {
        'page_obj': page_obj,
        'query': query
    })


def delete_loaner(request, pk):
    loaner = get_object_or_404(Loaner, pk=pk)
    loaner.delete()
    return redirect('main')

def payment(request, pk):
    loaner = get_object_or_404(Loaner, pk=pk)

    if request.method == 'POST':
        try:
            recieved = Decimal(request.POST.get('recieved'))
            if recieved > 0:
                # Get total paid so far before this payment
                total_paid = sum(p.recieved for p in loaner.payments.all())
                if total_paid + recieved > loaner.total_amount:
                    messages.error(request, "المبلغ المدفوع يتجاوز المبلغ الكلي.")
                    return redirect('payment', pk=loaner.id)
                new_remaining = max(loaner.total_amount - total_paid - recieved, 0)

                # Create new payment record
                Payment.objects.create(
                    loaner=loaner,
                    recieved=recieved,
                    remaining=new_remaining,
                    payment_date=request.POST.get('payment_date', None)  # Use the provided date or None
                )
        except Exception as e:
            print("Error creating payment:", e)

        return redirect('payment', pk=loaner.id)

    # Always define payments and total_received for GET requests
    payments = loaner.payments.order_by('-id')
    total_received = sum(p.recieved for p in payments)

    return render(request, 'payment.html', {
        'loaner': loaner,
        'payments': payments,
        'total_received': total_received
    })





def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    loaner_id = payment.loaner.id
    payment.delete()
    return redirect('payment', pk=loaner_id)



# arabic support for pdf
@login_required
def print_card(request, pk):
    loan = get_object_or_404(Loaner, pk=pk)
    payments = loan.payments.order_by('-payment_date')  # or '-id' if no date field


    return render(request, 'receipt.html', {
        'loan': loan,
        'payments': payments,
    })

    