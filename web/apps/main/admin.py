from django.contrib import admin
from web.apps.jwt_store.models import User
from web.apps.main.models import Payment

admin.site.register(User)
admin.site.register(Payment)