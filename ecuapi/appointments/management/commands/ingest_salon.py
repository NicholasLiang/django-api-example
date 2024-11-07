import json
from django.core.management.base import BaseCommand
from appointments.models import Stylist, Customer, Appointment

class Command(BaseCommand):
    help = 'Ingest stylists and customers from JSON files'

    def handle(self, *args, **kwargs):
        self.ingest_stylists()
        self.ingest_customers()

    def ingest_stylists(self):
        with open('data/stylists.json', 'r') as file:
            stylists_data = json.load(file)
            for stylist_data in stylists_data:
                Stylist.objects.update_or_create(
                    first_name=stylist_data['first_name'],
                    last_name=stylist_data['last_name'],
                    defaults={
                        'phone_number': stylist_data.get('phone_number', ''),
                        'email': stylist_data.get('email', ''),
                        'position': stylist_data.get('position', ''),
                        'specialization': stylist_data.get('specialization', ''),
                        'years_of_experience': stylist_data.get('years_of_experience', 0),
                        'description': stylist_data.get('description', '')
                    }
                )

    def ingest_customers(self):
        with open('data/customers.json', 'r') as file:
            customers_data = json.load(file)
            for customer_data in customers_data:
                Customer.objects.update_or_create(
                    first_name=customer_data['first_name'],
                    last_name=customer_data['last_name'],
                    defaults={
                        'phone_number': customer_data.get('phone_number', ''),
                        'email': customer_data.get('email', ''),
                        'address': customer_data.get('address', ''),
                        'date_of_birth': customer_data.get('date_of_birth', None),
                        'gender': customer_data.get('gender', ''),
                        'notes': customer_data.get('notes', '')
                    }
                )
