from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
import random
import string

from . manager import UserManager


class User(AbstractUser):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    is_manager = models.BooleanField(verbose_name="Is Manger", default=False)
    is_client = models.BooleanField(verbose_name="Is Client", default=False)
    phone_number = PhoneNumberField(verbose_name="Phone Number", blank=True, null=True)
    location = models.CharField(verbose_name="Location", max_length=100, blank=True, null=True)
    picture = models.ImageField(
        verbose_name="Profile Picture",
        upload_to="users/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    # update django about user model
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def image(self):
        return mark_safe('<img src="/../../media/%s" width="80" />' % (self.picture))

    image.allow_tags = True



class ServiceCategory(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='bland/category/',
        verbose_name="bland images",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )

    def __str__(self):
        return self.title

    def bland_image(self):
        return mark_safe('<img src="/../../media/%s" width="80" />' % (self.image))

    bland_image.allow_tags = True



class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    hours = models.CharField(max_length=50)

    def __str__(self):
        return self.service_name


class TeamMember(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
        
    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    phone = PhoneNumberField(verbose_name="Phone Number", blank=True, unique=True)
    work_id = models.CharField(max_length=255)
    picture = models.ImageField(
        verbose_name="Picture",
        upload_to="team/members/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def image(self):
        return mark_safe('<img src="/../../media/%s" width="80" />' % (self.picture))

    image.allow_tags = True



class Team(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_teams')
    team_name = models.CharField(max_length=255)
    members = models.ManyToManyField(TeamMember, related_name='teams')

    def __str__(self):
        return self.team_name


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    booking_no = models.CharField(max_length=100, unique=True, blank=False, null=False)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    service_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    manager_comment = models.TextField(blank=True, null=True)
    assigned_to_team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='bookings', blank=True, null=True)
    
    def __str__(self):
        return self.booking_no

    def generate_booking_no(self):
        # Generate a random booking number
        length = 20  # You can adjust the length of the booking number
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def save(self, *args, **kwargs):
        # Generate a booking number if it doesn't exist
        if not self.booking_no:
            self.booking_no = self.generate_booking_no()
        super().save(*args, **kwargs)
        


class ServiceReview(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField()
    client_comment = models.TextField()
    
    def __str__(self):
        return self.client_comment

    class Meta:
        unique_together = ('booking', 'rating', 'client_comment')
