import datetime

from push_notifications.models import GCMDevice

from villa.models import Calendar


def reminder_register():
    reserved_rows = Calendar.objects.filter(start_date__gte=datetime.datetime.now().date())
    for reserved_row in reserved_rows:
        if reserved_row.start_date - datetime.datetime.now().date() <= 1:
            try:
                customer_device = GCMDevice.objects.get(user=reserved_row.customer)
                host_device = GCMDevice.objects.get(user=reserved_row.villa.owner)

                customer_device.send_message(title=f"Hey, your reservation starts from tomorrow!",
                                             message=f"You've reserved '{reserved_row.villa.name}' in "
                                                     f"{reserved_row.villa.country}, {reserved_row.villa.state}, "
                                                     f"{reserved_row.villa.city} "
                                                     f"for {reserved_row.start_date}, {reserved_row.end_date}"
                                             )

                host_device.send_message(title=f"Hey, your guest comes tomorrow!",
                                         message=f"'{reserved_row.customer.__str__()}' has reserved your villa for "
                                                 f"{reserved_row.start_date},{reserved_row.end_date}"
                                         )
            except Exception as e:
                print(f"Error: {e}")


def reminder_cancel_reservation():
    reserved_rows = Calendar.objects.filter(start_date__gte=datetime.datetime.now().date())
    for reserved_row in reserved_rows:
        if reserved_row.start_date - datetime.datetime.now().date() >= 10:
            try:
                customer_device = GCMDevice.objects.get(user=reserved_row.customer)

                customer_device.send_message(title=f"You can cancel your reservation "
                                                   f"without loosing money until tonight!",
                                             message=f"You've reserved '{reserved_row.villa.name}' in "
                                                     f"{reserved_row.villa.country}, {reserved_row.villa.state}, "
                                                     f"{reserved_row.villa.city} "
                                                     f"for {reserved_row.start_date}, {reserved_row.end_date}"
                                             )

            except Exception as e:
                print(f"Error: {e}")

