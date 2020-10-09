from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render
from zeep import Client
from web.apps.jwt_store.models import User
from web.apps.main.models import Payment
from django.conf import settings


def send_request(request, id):
    try:
        user = User.objects.get(id = request.user.id)
        payment = Payment.objects.get(id = id)
        if payment.user == request.user:
            client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
            amount = payment.amount / 10
            tax = (int(amount) * 9) / 100
            amount = int(amount) + int(tax)
            description = user.username
            email = user.email
            mobile = user.tel
            merchant = settings.MERCHANT
            callback_url = settings.CALLBACK_URL

            result = client.service.PaymentRequest(merchant, amount, description, email, mobile, callback_url)
            if result.Status == 100:
                payment.authority = result.Authority
                payment.save()
                return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
            else:
                return HttpResponse('Error code: ' + str(result.Status))
        else:
            messages.error(request, 'فرم یه درستی ارسال نشده است!')
            return HttpResponseRedirect("/")
    except Exception as e:
        messages.error(request, 'خطایی رخ داده است!')
        return HttpResponseRedirect("/credit/add/")

def verify(request):
    try:
        if request.GET.get('Status') == 'OK':
            merchant = settings.MERCHANT
            payment = Payment.objects.get(authority = request.GET['Authority'])
            client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
            tax = (int(payment.amount) * 9) / 100
            amount = int(payment.amount) + int(tax)
            result = client.service.PaymentVerification(merchant, request.GET['Authority'], amount / 10)
            if not Payment.objects.filter(rfid = result.RefID):
                if result.Status is 100:
                    user = payment.user
                    balance = user.balance
                    user.balance = balance + payment.amount
                    user.save()
                    payment.rfid = result.RefID
                    payment.save()
                    messages.success(request,'پرداخت با موفقیت انجام شد.\nشماره پیگیری: ' + str(result.RefID))
                    return render(request, 'payment/add_invoice.html')

                elif result.Status == 101:
                    messages.info('تراکنش ارسال شد : ' + str(result.Status))
                    return render(request, 'payment/add_invoice.html')

                else:
                    messages.error('تراکنش لغو شد.\nوضعیت: ' + str(result.Status))
                    return render(request, 'payment/add_invoice.html')
            else:
                messages.error('تراکنش قبلا ثبت شده است!')
                return render(request, 'payment/add_invoice.html')
        else:
            messages.error('تراکنش باطل، یا توسط کاربر لغو شد!')
            return render(request, 'payment/add_invoice.html')

    except Exception as e:
        messages.error(request, 'خطایی رخ داده است!')
        return HttpResponseRedirect("/")