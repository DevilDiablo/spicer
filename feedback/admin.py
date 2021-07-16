from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([
    stafflogindata,
    userlogindata,
    department,
    HODlogindata,
    championdata,
    complaint,
    issues,
    attempts,
])