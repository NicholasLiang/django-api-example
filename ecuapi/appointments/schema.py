from datetime import datetime
from ninja import Schema

class CustomerSchema(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    address: str
    date_of_birth: datetime
    gender: str
    notes: str

class StylistSchema(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    image: str
    position: str
    specialization: str
    years_of_experience: int
    description: str


class StylistName(Schema):
    first_name: str
    last_name: str

class CustomerName(Schema):
    first_name: str
    last_name: str

class AppointmentSchema(Schema):
    hair_dresser: StylistName
    customer: CustomerName
    start_date_time: datetime
    duration_in_minutes: int
    service_type: str
    stylist_preference: str = None
    additional_request: str = None
    receive_sms_reminder: bool = False
    receive_email_reminder: bool = False


class NotFoundSchema(Schema):
    message: str

