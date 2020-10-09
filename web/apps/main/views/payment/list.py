from django.shortcuts import render
from web.apps.main.models import Payment

def list_payment(request):
    payments = Payment.objects.filter(user = request.user)
    return render(request, 'payment/list.html', {'payments':payments})
