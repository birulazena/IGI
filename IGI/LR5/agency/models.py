from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_age_18_plus, validate_belarus_phone


class Profile(models.Model):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('employee', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    patronymic = models.CharField(max_length=100, blank=True, null=True, help_text="Middle name / Patronymic")
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, validators=[validate_belarus_phone])
    birth_date = models.DateField(validators=[validate_age_18_plus])

    def __str__(self):
        last_name = self.user.last_name
        first_name = self.user.first_name
        patronymic_name = self.patronymic or ""

        full_name = f"{last_name} {first_name} {patronymic_name}".strip()

        if full_name:
            return f"{full_name} ({self.get_role_display()})"
        return f"{self.user.username} ({self.get_role_display()})"

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    climate_summer = models.CharField(max_length=100, help_text = "summer climate")
    climate_winter = models.CharField(max_length=100, help_text = "winter climate")

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='hotels')
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"{self.name} {self.stars}* ({self.country.name})"

class Tour(models.Model):
    DURATION_CHOICES = (
        (1, 'One week'),
        (2, 'Two weeks'),
        (4, 'Four weeks'),
    )

    title = models.CharField(max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tours')
    duration_weeks = models.PositiveSmallIntegerField(choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.duration_weeks} нед. ({self.price} BYN)"

class Order(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client_orders', limit_choices_to={'role': 'client'})
    employee = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='employee_orders', limit_choices_to={'role': 'employee'})
    tours = models.ManyToManyField(Tour, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    departure_date = models.DateField()

    def __str__(self):
        return f"Заказ #{self.id} от {self.client.user.username}"

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=255, help_text="One sentence summary")
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    history_by_years = models.TextField(help_text="History by years (e.g. 2010 - founded, 2015 - expanded)")
    requisites = models.TextField(help_text="Company requisites (UNP, Address, etc.)")
    logo_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Company Information"

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question

class EmployeeContact(models.Model):
    full_name = models.CharField(max_length=150)
    job_description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name

class Vacancy(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} - {self.rating}/5"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        status = "Active" if self.is_active else "Archived"
        return f"{self.code} ({self.discount_percentage}%) - {status}"