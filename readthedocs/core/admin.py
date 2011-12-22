"""Django admin interface for core models.
"""

from django.contrib import admin

from core.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'whitelisted', 'homepage')
    search_fields = ('user__username', 'homepage')
    list_editable = ('whitelisted',)
    raw_id_fields = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)
