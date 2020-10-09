from django.shortcuts import render

def add_invoice(request):
    return render(request, 'payment/add_invoice.html')
