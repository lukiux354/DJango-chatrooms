from django.contrib import admin
from .models import User, Channel, Message, Membership
# Register your models here.

admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(Membership)