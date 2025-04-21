from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('veterinarian', 'Veterinarian')
    ]

    USER_LOCATION_CHOICES = [
        ('hq', 'Headquarters'),
        ('tps_moshi', 'TPS Moshi'),
        ('dodoma', 'Dodoma'),
        ('iringa', 'Iringa'),
        ('all', 'All Locations')
    ]

    role = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    location = models.CharField(max_length=20, choices=USER_LOCATION_CHOICES, default='hq')

    def __str__(self):
        return self.username


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} - {self.action}"


class BaseAnimal(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]

    microchip_id = models.CharField(max_length=200, blank=True, null=True)
    behavioral_notes = models.TextField(blank=True, null=True)
    breed = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    work = models.CharField(max_length=200, blank=True, null=True)
    training_details = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    treatment_details = models.TextField(blank=True, null=True)
    transfer_details = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class HQDog(BaseAnimal): pass
class TpsMoshiDog(BaseAnimal): pass
class DodomaDog(BaseAnimal): pass
class IringaDog(BaseAnimal): pass
class HQHorse(BaseAnimal): pass
class TpsMoshiHorse(BaseAnimal): pass
class DodomaHorse(BaseAnimal): pass
class IringaHorse(BaseAnimal): pass


class Picture(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('horse', 'Horse'),
        ('other', 'Other'),
    ]

    LOCATION_CHOICES = [
        ('hq', 'HQ'),
        ('tps_moshi', 'TPS Moshi'),
        ('dodoma', 'Dodoma'),
        ('iringa', 'Iringa'),
    ]

    image = models.ImageField(upload_to='pictures/')
    title = models.CharField(max_length=255, blank=True)
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPE_CHOICES, default='dog')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='hq')

    age_description = models.CharField(max_length=100, blank=True)
    related_object_id = models.IntegerField(null=True, blank=True)
    related_object_name = models.CharField(max_length=255, blank=True)

    force_no = models.CharField("Force Number", max_length=50, blank=True)
    name = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    work = models.TextField(blank=True)
    training_details = models.TextField(blank=True)
    medical_records = models.TextField(blank=True)
    weight = models.CharField(max_length=50, blank=True)
    vaccination_record = models.TextField(blank=True)
    treatment_record = models.TextField(blank=True)
    deworming_record = models.TextField(blank=True)
    transfer_detail = models.TextField(blank=True)

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='uploaded_pictures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.title:
            return self.title
        return f"{self.get_animal_type_display()} {self.name or self.related_object_name or f'#{self.id}'}"

    def get_absolute_url(self):
        return reverse('picture_detail', kwargs={'pk': self.pk})

    @property
    def related_object_type(self):
        if self.animal_type == 'other':
            return 'other'
        return f"{self.location}_{self.animal_type}"


class MedicalRecord(models.Model):
    dog = models.ForeignKey(HQDog, on_delete=models.CASCADE, related_name='medical_records', null=True, blank=True)
    horse = models.ForeignKey(HQHorse, on_delete=models.CASCADE, related_name='medical_records', null=True, blank=True)
    date = models.DateField()
    description = models.TextField()
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='medical_records')

    def __str__(self):
        if self.dog:
            return f"Medical Record for {self.dog.name} on {self.date}"
        elif self.horse:
            return f"Medical Record for {self.horse.name} on {self.date}"
        return f"Medical Record on {self.date}"


# Add to your models.py
from django.db import models
from django.utils import timezone


class AnimalTransfer(models.Model):
    date = models.DateField(default=timezone.now)
    animal_name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    reason = models.TextField()
    handled_by = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.animal_name} transferred from {self.from_location} to {self.to_location} on {self.date}"