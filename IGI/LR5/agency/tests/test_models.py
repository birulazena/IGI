import pytest
from datetime import date
from django.contrib.auth.models import User
from agency.models import (
    Profile, Country, Hotel, Tour, Order, NewsArticle,
    CompanyInfo, FAQ, EmployeeContact, Vacancy, Review, PromoCode
)


@pytest.mark.django_db
class TestAgencyModels:

    def test_profile_str_with_full_name(self):
        user = User.objects.create(username="ivan_c", first_name="Ivan", last_name="Ivanov")
        profile = Profile.objects.create(
            user=user, role='client', patronymic='Ivanovich',
            address='Minsk', phone='+375291112233', birth_date=date(2000, 1, 1)
        )
        assert str(profile) == "Ivanov Ivan Ivanovich (Client)"

    def test_profile_str_without_full_name(self):
        user = User.objects.create(username="guest_user")
        profile = Profile.objects.create(
            user=user, role='client',
            address='Brest', phone='+375299998877', birth_date=date(1995, 5, 5)
        )
        assert str(profile) == "guest_user (Client)"

    def test_tour_hotel_country_relations(self):
        country = Country.objects.create(name="Turkey", climate_summer="Hot", climate_winter="Mild")
        hotel = Hotel.objects.create(name="Rixos", country=country, stars=5)
        tour = Tour.objects.create(title="Summer Break", hotel=hotel, duration_weeks=2, price=1500.00)

        assert str(country) == "Turkey"
        assert str(hotel) == "Rixos 5* (Turkey)"
        # Matching the exact string format from your models.py
        assert str(tour) == "Summer Break - 2 нед. (1500.0 BYN)"

    def test_order_creation(self):
        user = User.objects.create(username="order_client")
        client_profile = Profile.objects.create(
            user=user, role='client', address='Gomel',
            phone='+375291231212', birth_date=date(1990, 1, 1)
        )
        order = Order.objects.create(client=client_profile, departure_date=date(2026, 6, 1))

        assert str(order) == f"Заказ #{order.id} от order_client"
        assert order.employee is None

    def test_news_article(self):
        article = NewsArticle.objects.create(
            title="Great News", summary="Short text", content="Long text"
        )
        assert str(article) == "Great News"

    def test_company_info(self):
        info = CompanyInfo.objects.create(history_by_years="2020: Opened", requisites="UNP 12345")
        assert str(info) == "Company Information"

    def test_faq(self):
        faq = FAQ.objects.create(question="How to book?", answer="Click the button.")
        assert str(faq) == "How to book?"

    def test_employee_contact(self):
        emp = EmployeeContact.objects.create(
            full_name="Anna Smith", job_description="Manager", phone="123", email="anna@test.com"
        )
        assert str(emp) == "Anna Smith"

    def test_vacancy(self):
        vac = Vacancy.objects.create(title="Tour Guide", description="Must speak English")
        assert str(vac) == "Tour Guide"

    def test_review(self):
        review = Review.objects.create(client_name="Max", rating=5, text="Amazing tour!")
        assert str(review) == "Review by Max - 5/5"

    def test_promo_code_active_and_archived(self):
        promo_active = PromoCode.objects.create(code="SUMMER26", discount_percentage=10, is_active=True)
        promo_archived = PromoCode.objects.create(code="OLD25", discount_percentage=5, is_active=False)

        assert str(promo_active) == "SUMMER26 (10%) - Active"
        assert str(promo_archived) == "OLD25 (5%) - Archived"