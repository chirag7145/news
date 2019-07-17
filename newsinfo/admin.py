from django.contrib import admin
from .models import *
# Register your models here.


class likedModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'added_on', 'title',
                    'country', 'category', 'source')
    search_fields = ('title', 'source')
    list_display_links = ('title',)
    list_filter = ('added_on', 'user', 'country', 'category', 'source')

    class Meta:
        model = liked


admin.site.register(liked, likedModelAdmin)


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_confirmed')
    search_fields = ('user', 'email_confirmed')
    list_display_links = ('user',)
    list_filter = ('user', 'email_confirmed')

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileModelAdmin)
