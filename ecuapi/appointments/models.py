from django.db import models

class Stylist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    years_of_experience = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    hair_dresser = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    duration_in_minutes = models.IntegerField()
    service_type = models.CharField(max_length=100)
    stylist_preference = models.CharField(max_length=100, blank=True)
    additional_request = models.TextField(blank=True)
    receive_sms_reminder = models.BooleanField(default=False)
    receive_email_reminder = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=[('booked', 'Booked'), ('completed', 'Completed'), ('canceled', 'Canceled')],
        default='booked'
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('paid', 'Paid'), ('canceled', 'Canceled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment on {self.start_date_time.date()} at {self.start_date_time.time()} with {self.hair_dresser}"
