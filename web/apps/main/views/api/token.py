from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token

class ViewToken(TemplateView):
    def get(self, request, *args, **kwargs):
        token = Token.objects.filter(user=request.user)
        return render(request, 'token/view.html', {'token': token})

def regenerate(request):
    token = Token.objects.filter(user=request.user)
    if token:
        Token.objects.get(user=request.user).delete()
    Token.objects.create(user=request.user)
    return redirect('/token/view')
