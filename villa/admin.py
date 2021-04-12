from django.contrib import admin

# Register your models here.
from account.models import Account
from villa.models import Villa


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
