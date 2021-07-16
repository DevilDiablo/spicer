
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([
    tester,machine,
    assembly,
    part,
    checkpoint,
    standard_binary,
    standard_range,
    standard_value,
    frequency,standard,
    range_value,
    standard_ryb,
    reviewer,
    mainhodlogindata,
])