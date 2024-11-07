import json
from django.core.management.base import BaseCommand
from appointments.models import Stylist, Customer, Appointment

class Command(BaseCommand):
    help = 'Ingest appointments from JSON files'

    def handle(self, *args, **kwargs):
        with open('data/appointments.json', 'r') as file:
            appointments_data = json.load(file)
            for appointment_data in appointments_data:
                stylist = Stylist.objects.get(first_name=appointment_data['hair_dresser']['first_name'], last_name=appointment_data['hair_dresser']['last_name'])
                customer = Customer.objects.get(first_name=appointment_data['customer']['first_name'], last_name=appointment_data['customer']['last_name'])
                Appointment.objects.update_or_create(
                    hair_dresser=stylist,
                    customer=customer,
                    start_date_time=appointment_data['start_date_time'],
                    defaults={
                        'duration_in_minutes': appointment_data.get('duration_in_minutes', 0),
                        'service_type': appointment_data.get('service_type', ''),
                        'stylist_preference': appointment_data.get('stylist_preference', ''),
                        'additional_request': appointment_data.get('additional_request', ''),
                        'receive_sms_reminder': appointment_data.get('receive_sms_reminder', False),
                        'receive_email_reminder': appointment_data.get('receive_email_reminder', False),
                        'status': appointment_data.get('status', 'booked'),
                        'payment_status': appointment_data.get('payment_status', 'pending')
                    }
                )