from datetime import datetime
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from appointments.models import Appointment, Stylist, Customer

class Command(BaseCommand):
    help = "Export salon to stylists.json and customers.json"

    def handle(self, *args, **kwargs):
        self.export_stylists()
        self.export_customers()

    def export_stylists(self):
        stylists = Stylist.objects.all()
        stylist_data = []

        for stylist in stylists:
            stylist_data.append({
                'first_name': stylist.first_name,
                'last_name': stylist.last_name,
                'phone_number': stylist.phone_number,
                'email': stylist.email,
                'image': stylist.image,
                'position': stylist.position,
                'specialization': stylist.specialization,
                'years_of_experience': stylist.years_of_experience,
                'description': stylist.description,
            })

        file_path_stylists = settings.BASE_DIR / 'data/stylists.json'
        with open(file_path_stylists, 'w') as json_file:
            json.dump(stylist_data, json_file, indent=4, default=str)

        self.stdout.write(self.style.SUCCESS('Successfully exported stylists'))

    def export_customers(self):
        customers = Customer.objects.all()
        customer_data = []

        for customer in customers:
            customer_data.append({
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone_number': customer.phone_number,
                'email': customer.email,
                'address': customer.address,
                'date_of_birth': customer.date_of_birth.strftime('%Y-%m-%d') if customer.date_of_birth else None,
                'gender': customer.gender,
                'notes': customer.notes,
            })

        file_path_customers = settings.BASE_DIR / 'data/customers.json'
        with open(file_path_customers, 'w') as json_file:
            json.dump(customer_data, json_file, indent=4, default=str)

        self.stdout.write(self.style.SUCCESS('Successfully exported customers'))