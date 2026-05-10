from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
import re

def validate_age_18_plus(birth_date: date):
    """Checks that the user is 18 years old"""
    today = timezone.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("Must be at least 18 years old")

def validate_belarus_phone(value: str):
    """Checks the phone format"""
    pattern = r'^\+375\ \((29|44|33|25)\)\ \d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError("The phone number must be in the format +375 (XX) XXX-XX-XX")