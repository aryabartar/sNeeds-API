from django.contrib import admin

from .models import PayPayment, ConsultantDepositInfo

# Register your models here.
admin.site.register(PayPayment)
admin.site.register(ConsultantDepositInfo)
