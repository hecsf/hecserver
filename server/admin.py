from django.contrib import admin

# Register your models here.
from server.models import *

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Survey)
