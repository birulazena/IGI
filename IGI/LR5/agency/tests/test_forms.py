import pytest
from agency.forms import ReviewForm, OrderForm, UserRegisterForm


@pytest.mark.django_db
class TestAgencyForms:

    def test_review_form_valid(self):
        form = ReviewForm(data={'rating': 5, 'text': 'Great tour!'})
        assert form.is_valid() is True

    def test_review_form_invalid(self):
        form = ReviewForm(data={'rating': 6, 'text': ''})
        assert form.is_valid() is False
        assert 'rating' in form.errors
        assert 'text' in form.errors

    def test_order_form_valid(self):
        form = OrderForm(data={'departure_date': '2026-07-01'})
        assert form.is_valid() is True

    def test_order_form_invalid(self):
        form = OrderForm(data={})
        assert form.is_valid() is False
        assert 'departure_date' in form.errors

    def test_user_register_form_missing_fields(self):
        form = UserRegisterForm(data={
            'username': 'newuser',
            'first_name': 'Test',
            'last_name': 'User'
        })
        assert form.is_valid() is False
        assert 'address' in form.errors
        assert 'phone' in form.errors
        assert 'email' in form.errors