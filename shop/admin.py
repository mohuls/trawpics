from ast import Or
from django.contrib import admin

from .models import *

admin.site.register(Home)
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(Review)
admin.site.register(Order)