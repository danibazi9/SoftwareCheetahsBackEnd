from django.contrib import admin

# Register your models here.
from account.models import Account
from villa.models import *


class VillaAdmin(admin.ModelAdmin):
    list_display = ['villa_id', 'name', 'type', 'country', 'city', 'get_owner']
    search_fields = ['name', 'country', 'city']
    list_filter = ['type']

    def get_owner(self, obj):
        result = Account.objects.get(id=obj.id)
        return result.__str__()

    class Meta:
        model = Villa


admin.site.register(Villa, VillaAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'title', 'get_villa', 'default']
    search_fields = ['title']
    list_filter = ['default']

    def get_villa(self, obj):
        result = Villa.objects.get(villa_id=obj.id)
        return result.__str__()

    class Meta:
        model = Image


admin.site.register(Image, ImageAdmin)
