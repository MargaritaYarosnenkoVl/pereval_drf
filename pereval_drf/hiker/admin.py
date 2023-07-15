from django.contrib import admin

from hiker.models import Hiker


class HikerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fam', 'name', 'otc', 'phone', 'email',)


admin.site.register(Hiker, HikerAdmin)
