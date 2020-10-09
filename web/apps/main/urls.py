from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views.signup import signup, activate
from web.apps.main.views import *
from .views.dashboard import dashboard


urlpatterns = [
    path('', login_required(dashboard), name='dashboard'),

    path('profile/', login_required(EditProfile.as_view()), name='edit_profile'),
    path('changePassword/', login_required(change_password), name='change_password'),

    path('token/view/', login_required(ViewToken.as_view()), name='view_token'),
    path('token/regenerate/', login_required(regenerate), name='generate_token'),

    path('credit/add/', login_required(add_invoice), name='add_invoice'),
    path('credit/invoice/', login_required(Invoice.as_view()), name='invoice'),
    path('invoice/<int:id>/pay/', login_required(send_request), name='pay'),
    path('verify/', verify, name='verify'),
    path('payment/view/', login_required(list_payment), name='list_payment'),

    url(r'^accounts/signup/$', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
