from django.contrib import admin
from .models import UserProfile,Document,PersonalInfo
# Register your models here.

admin.site.register([UserProfile,Document,PersonalInfo])