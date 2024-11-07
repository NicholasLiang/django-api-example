from datetime import datetime
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from appointments.models import Appointment, Stylist, Customer

class Command(BaseCommand):
    help = "Export appointments to a JSON file"

    def handle(self, *args, **kwargs):
        appointments = Appointment.objects.all()
        appointment_data = []

        for appointment in appointments:
            stylist = Stylist.objects.get(first_name=appointment.hair_dresser.first_name, last_name=appointment.hair_dresser.last_name)
            customer = Customer.objects.get(first_name=appointment.customer.first_name, last_name=appointment.customer.last_name)
            appointment_data.append({
                'hair_dresser': {
                    'first_name': stylist.first_name,
                    'last_name': stylist.last_name,
                },
                'customer': {
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                },
                'start_data_time': appointment.start_data_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_in_minutes': appointment.duration_in_minutes,
                'service_type': appointment.service_type,
                'stylist_preference': appointment.stylist_preference,
                'additional_request': appointment.additional_request,
                'receive_sms_reminder': appointment.receive_sms_reminder,
                'receive_email_reminder': appointment.receive_email_reminder,
                'status': appointment.status,
                'payment_status': appointment.payment_status,
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        file_path = settings.BASE_DIR / 'data/appointments.json'
        with open(file_path, 'w') as json_file:
            json.dump(appointment_data, json_file, indent=4, default=str)

        self.stdout.write(self.style.SUCCESS('Successfully exported appointments'))
