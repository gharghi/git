from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
# from web.apps.api.views import CdrList, CdrDetail

urlpatterns = [
    # path('call/', CdrList.as_view()),
    # path('call/<int:pk>', CdrDetail.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)