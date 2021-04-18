from django.contrib import admin

from villa.models import *


# Register your models here.
class VillaAdmin(admin.ModelAdmin):
    list_display = ['villa_id', 'name', 'type', 'country', 'city', 'get_owner']
    search_fields = ['name', 'country', 'city']
    list_filter = ['type']

    def get_owner(self, obj):
        result = Villa.objects.get(villa_id=obj.villa_id)
        return result.owner.first_name + ' ' + result.owner.last_name

    class Meta:
        model = Villa


admin.site.register(Villa, VillaAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'title', 'get_villa', 'default']
    search_fields = ['title']
    list_filter = ['default']

    def get_villa(self, obj):
        result = Villa.objects.get(images__image_id=obj.image_id)
        return result.__str__()

    class Meta:
        model = Image


admin.site.register(Image, ImageAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['document_id', 'get_user']
    list_filter = ['user']

    def get_user(self, obj):
        result = Account.objects.get(user_id=obj.user_id)
        return result.__str__()

    class Meta:
        model = Document


admin.site.register(Document, DocumentAdmin)


class FacilityAdmin(admin.ModelAdmin):
    list_display = ['facility_id', 'name']
    search_fields = ['name']

    class Meta:
        model = Facility


admin.site.register(Facility, FacilityAdmin)
