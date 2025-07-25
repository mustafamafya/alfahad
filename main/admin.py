from django.contrib import admin
from .models import Loaner, Payment
# Register your models here.


admin.site.register(Loaner)
admin.site.register(Payment)