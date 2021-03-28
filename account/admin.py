import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account
from persiantools.jdatetime import JalaliDateTime


class AccountAdmin(UserAdmin):
	list_display = ('user_id', 'first_name', 'last_name', 'email', 'get_date_joined', 'role', 'is_admin')
	search_fields = ('first_name', 'last_name', 'email')
	list_filter = ('role',)
	exclude = ('password',)
	readonly_fields = ('date_joined', 'last_login')
	ordering = ('email',)

	filter_horizontal = ()
	fieldsets = ()

	def get_date_joined(self, obj):
		timestamp = datetime.datetime.timestamp(obj.date_joined)
		jalali_datetime = JalaliDateTime.fromtimestamp(timestamp)
		return jalali_datetime.strftime("%Y/%m/%d - %H:%M")


admin.site.register(Account, AccountAdmin)
