# After creating models in models.py, register them here
from django.contrib import admin
from .models import User, Profile

admin.site.register(User)
admin.site.register(Profile)
