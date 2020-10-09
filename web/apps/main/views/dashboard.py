from django.shortcuts import render
import datetime


def dashboard(request):
    today = datetime.datetime.now() - datetime.timedelta(minutes=1440)
    return render(request, 'dashboard.html')

