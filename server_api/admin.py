from django.contrib import admin
from .models import User, Auth, Session, Chips

# Register your models here.

admin.site.register(User)
admin.site.register(Auth)
admin.site.register(Session)
admin.site.register(Chips)
