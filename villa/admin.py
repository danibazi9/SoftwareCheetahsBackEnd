from django.contrib import admin

from villa.models import *


# Register your models here.
class VillaAdmin(admin.ModelAdmin):
    list_display = ['villa_id', 'name', 'type', 'country', 'city', 'get_owner', 'visible']
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
    list_display = ['document_id']

    class Meta:
        model = Document


admin.site.register(Document, DocumentAdmin)


class FacilityAdmin(admin.ModelAdmin):
    list_display = ['facility_id', 'name']
    search_fields = ['name']

    class Meta:
        model = Facility


admin.site.register(Facility, FacilityAdmin)


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['calendar_id', 'customer', 'villa', 'start_date', 'end_date', 'closed']
    list_filter = ['villa']

    class Meta:
        model = Calendar


admin.site.register(Calendar, CalendarAdmin)


class RuleAdmin(admin.ModelAdmin):
    list_display = ['rule_id', 'text']
    list_filter = ['text']

    class Meta:
        model = Rule


admin.site.register(Rule, RuleAdmin)
