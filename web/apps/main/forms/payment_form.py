from django.forms import ModelForm
from web.apps.main.models import Payment

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
