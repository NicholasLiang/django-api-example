from typing import List, Optional
from ninja import NinjaAPI
from appointments.models import Appointment, Customer, Stylist
from appointments.schema import AppointmentSchema, CustomerSchema, StylistSchema, NotFoundSchema

api = NinjaAPI()

@api.get("/customers", response=List[CustomerSchema])
def customers(request, first_name: Optional[str] = None, last_name: Optional[str] = None, phone_number: Optional[str] = None, email: Optional[str] = None):
    queryset = Customer.objects.all()
    if first_name:
        queryset = queryset.filter(first_name__icontains=first_name)
    if last_name:
        queryset = queryset.filter(last_name__icontains=last_name)
    if phone_number:
        queryset = queryset.filter(phone_number__icontains=phone_number)
    if email:
        queryset = queryset.filter(email__icontains=email)
    return queryset

@api.post("/customers", response={201: CustomerSchema})
def create_customer(request, customer: CustomerSchema):
    return Customer.objects.create(**customer.dict())

# @api.put("/customers/{customer_id}", response=CustomerSchema)
# def update_customer(request, customer_id: int, customer: CustomerSchema):
#     customer = Customer.objects.get(id=customer_id)
#     for attr, value in customer.dict().items():
#         setattr(customer, attr, value)
#     customer.save()
#     return customer

# @api.delete("/customers/{customer_id}")
# def delete_customer(request, customer_id: int):
#     customer = Customer.objects.get(id=customer_id)
#     customer.delete()
#     return 204

@api.get("/stylists", response=List[StylistSchema])
def stylists(request, first_name: Optional[str] = None, last_name: Optional[str] = None, phone_number: Optional[str] = None, email: Optional[str] = None):
    queryset = Stylist.objects.all()
    if first_name:
        queryset = queryset.filter(first_name__icontains=first_name)
    if last_name:
        queryset = queryset.filter(last_name__icontains=last_name)
    if phone_number:
        queryset = queryset.filter(phone_number__icontains=phone_number)
    if email:
        queryset = queryset.filter(email__icontains=email)
    return queryset


@api.post("/stylists", response={201: StylistSchema})
def create_stylist(request, stylist: StylistSchema):
    return Stylist.objects.create(**stylist.dict())

# @api.put("/stylists/{stylist_id}", response=StylistSchema)
# def update_stylist(request, stylist_id: int, stylist: StylistSchema):
#     stylist = Stylist.objects.get(id=stylist_id)
#     for attr, value in stylist.dict().items():
#         setattr(stylist, attr, value)
#     stylist.save()
#     return stylist

# @api.delete("/stylists/{stylist_id}")
# def delete_stylist(request, stylist_id: int):
#     stylist = Stylist.objects.get(id=stylist_id)
#     stylist.delete()
#     return 204


@api.get("/appointments", response=List[AppointmentSchema])
def appointments(
    request,
    stylist_first_name: Optional[str] = None,
    stylist_last_name: Optional[str] = None,
    customer_first_name: Optional[str] = None,
    customer_last_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    customer_phone_number: Optional[str] = None
):
    queryset = Appointment.objects.all()

    # Filter based on stylist's first and last names
    if stylist_first_name:
        queryset = queryset.filter(hair_dresser__first_name__icontains=stylist_first_name)
    if stylist_last_name:
        queryset = queryset.filter(hair_dresser__last_name__icontains=stylist_last_name)

    # Filter based on customer's first and last names, email, and phone number
    if customer_first_name:
        queryset = queryset.filter(customer__first_name__icontains=customer_first_name)
    if customer_last_name:
        queryset = queryset.filter(customer__last_name__icontains=customer_last_name)
    if customer_email:
        queryset = queryset.filter(customer__email__icontains=customer_email)
    if customer_phone_number:
        queryset = queryset.filter(customer__phone_number__icontains=customer_phone_number)

    return queryset


@api.post("/appointments", response={201: AppointmentSchema})
def create_appointment(request, appointment: AppointmentSchema):
    try:
        # Fetch the Stylist based on first and last names
        stylist = Stylist.objects.get(
            first_name=appointment.hair_dresser.first_name,
            last_name=appointment.hair_dresser.last_name
        )
    except Stylist.DoesNotExist:
        return {"error": "Stylist not found"}, 404

    # Try to fetch the Customer based on first and last names
    try:
        customer = Customer.objects.get(
            first_name=appointment.customer.first_name,
            last_name=appointment.customer.last_name
        )
    except Customer.DoesNotExist:
        # If the customer does not exist, create a new one
        customer = Customer.objects.create(
            first_name=appointment.customer.first_name,
            last_name=appointment.customer.last_name,
            phone_number=appointment.customer.phone_number,
            email=appointment.customer.email
            # You can add additional fields if available in the schema (like phone number or email)
        )

    # Create the appointment with the fetched stylist and customer
    new_appointment = Appointment.objects.create(
        hair_dresser=stylist,
        customer=customer,
        start_date_time=appointment.start_date_time,
        duration_in_minutes=appointment.duration_in_minutes,
        service_type=appointment.service_type,
        stylist_preference=appointment.stylist_preference,
        additional_request=appointment.additional_request,
        receive_sms_reminder=appointment.receive_sms_reminder,
        receive_email_reminder=appointment.receive_email_reminder,
    )

    return new_appointment


# @api.put("/appointments/{appointment_id}", response={200: AppointmentSchema, 404: NotFoundSchema})
# def update_appointment(request, appointment_id: int, appointment: AppointmentSchema):
#     try:
#         # Fetch the existing appointment
#         existing_appointment = Appointment.objects.get(id=appointment_id)

#         # Update the appointment fields with the new values from the schema
#         if appointment.hair_dresser:
#             # We assume hair_dresser is a nested schema with first_name and last_name
#             stylist = Stylist.objects.get(
#                 first_name=appointment.hair_dresser.first_name,
#                 last_name=appointment.hair_dresser.last_name
#             )
#             existing_appointment.hair_dresser = stylist

#         if appointment.customer:
#             # Same for customer, using first_name and last_name
#             customer = Customer.objects.get(
#                 first_name=appointment.customer.first_name,
#                 last_name=appointment.customer.last_name
#             )
#             existing_appointment.customer = customer

#         # Now, update other fields
#         existing_appointment.date = appointment.date
#         existing_appointment.duration_in_minutes = appointment.duration_in_minutes
#         existing_appointment.service_type = appointment.service_type
#         existing_appointment.stylist_preference = appointment.stylist_preference
#         existing_appointment.additional_request = appointment.additional_request
#         existing_appointment.receive_sms_reminder = appointment.receive_sms_reminder
#         existing_appointment.receive_email_reminder = appointment.receive_email_reminder
#         existing_appointment.status = appointment.status
#         existing_appointment.payment_status = appointment.payment_status

#         # Save the updated appointment
#         existing_appointment.save()

#         # Return the updated appointment
#         return 200, AppointmentSchema.from_orm(existing_appointment)

#     except Appointment.DoesNotExist:
#         return 404, {"message": f"Appointment {appointment_id} not found"}
#     except Stylist.DoesNotExist:
#         return 404, {"message": "Stylist not found"}
#     except Customer.DoesNotExist:
#         return 404, {"message": "Customer not found"}



# @api.delete("/appointments/{appointment_id}", response={204: None, 404: NotFoundSchema})
# def delete_appointment(request, appointment_id: int):
#     try:
#         # Fetch the existing appointment
#         appointment = Appointment.objects.get(id=appointment_id)

#         # Delete the appointment
#         appointment.delete()

#         # Return a 204 response indicating successful deletion
#         return 204, None

#     except Appointment.DoesNotExist:
#         # If the appointment does not exist, return a 404 error with a message
#         return 404, {"message": f"Appointment {appointment_id} not found"}



