from django.contrib import admin
from .models import Profile
from .models import CustomUser
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
    raw_id_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser)
