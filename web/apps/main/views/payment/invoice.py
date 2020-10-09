from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from web.apps.main.forms import PaymentForm
from web.apps.main.models import Payment

class Invoice(TemplateView):

    def post(self, request, *args, **kwargs):
        try:
            form = PaymentForm(request.POST)
            username = request.user
            amount = request.POST['amount']
            if form.is_valid():
                invoice = form.save(commit=False)
                invoice.user = username
                invoice.save()
                form.save_m2m()
                id = invoice.pk
                tax = (int(amount) * 9) / 100
                total = int(amount) + int(tax)

            else:
                messages.error(request, form.errors)

            # payment = Payment.objects.latest(id)
            return render(request, 'payment/invoice.html', {'id': id, 'amount': amount, 'tax': tax, 'total': total})

        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect("/")