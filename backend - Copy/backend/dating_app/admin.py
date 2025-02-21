# After creating models in models.py, register them here
from django.contrib import admin
from .models import User, Profile
from django.contrib import admin
from .models import User, Profile, Match, Message, Notification 


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Match)
admin.site.register(Message)
admin.site.register(Notification)