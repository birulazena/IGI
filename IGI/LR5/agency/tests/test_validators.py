import pytest
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
from agency.validators import validate_age_18_plus, validate_belarus_phone


class TestValidators:

    def test_validate_age_18_plus_valid(self):
        """Test that a 25-year-old passes validation."""
        today = timezone.now().date()
        valid_date = date(today.year - 25, today.month, today.day)

        validate_age_18_plus(valid_date)

    def test_validate_age_18_plus_invalid(self):
        """Test that a 10-year-old raises a ValidationError."""
        today = timezone.now().date()
        invalid_date = date(today.year - 10, today.month, today.day)

        with pytest.raises(ValidationError, match="Must be at least 18 years old"):
            validate_age_18_plus(invalid_date)

    def test_validate_belarus_phone_valid(self):
        """Test valid phone number formats."""
        valid_phones = [
            "+375 (29) 123-45-67",
            "+375 (44) 987-65-43",
            "+375 (33) 111-22-33",
            "+375 (25) 000-00-00",
        ]
        for phone in valid_phones:
            validate_belarus_phone(phone)

    def test_validate_belarus_phone_invalid(self):
        """Test invalid phone number formats raise ValidationError."""
        invalid_phones = [
            "+375 29 123-45-67",
            "+375 (29) 1234567",
            "80291234567",
            "+375 (99) 123-45-67",
        ]
        for phone in invalid_phones:
            with pytest.raises(ValidationError, match="The phone number must be in the format"):
                validate_belarus_phone(phone)