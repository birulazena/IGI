import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from agency.models import (
    Profile, Country, Hotel, Tour, Order, Review, NewsArticle
)
from datetime import date
from unittest.mock import patch


# Mocking external APIs for ALL tests in this class to prevent real network requests
@pytest.mark.django_db
@patch('agency.views.WeatherService.get_current_weather', return_value={'temp': 20, 'description': 'Clear'})
@patch('agency.views.CurrencyService.get_usd_rate', return_value=3.25)
class TestAgencyViews:

    @pytest.fixture(autouse=True)
    def setup_data(self, client):
        """Sets up test data before each test runs."""
        self.client = client

        # 1. Create a Client user
        self.client_user = User.objects.create_user(username='client1', password='password123')
        self.client_profile = Profile.objects.create(
            user=self.client_user, role='client', address='A', phone='1', birth_date=date(2000, 1, 1)
        )

        # 2. Create an Employee user
        self.emp_user = User.objects.create_user(username='emp1', password='password123')
        self.emp_profile = Profile.objects.create(
            user=self.emp_user, role='employee', address='B', phone='2', birth_date=date(2000, 1, 1)
        )

        # 3. Create a Superuser (Admin)
        self.admin_user = User.objects.create_superuser(username='admin1', password='password123')

        # 4. Create base database objects for views
        self.country = Country.objects.create(name='TestCountry', climate_summer='H', climate_winter='C')
        self.hotel = Hotel.objects.create(name='TestHotel', country=self.country, stars=5)
        self.tour = Tour.objects.create(title='TestTour', hotel=self.hotel, duration_weeks=1, price=100)

    def test_public_views_return_200(self, mock_usd, mock_weather):
        """Ensure all public pages load successfully without login."""
        urls = [
            'agency:home', 'agency:about', 'agency:news_list', 'agency:faq',
            'agency:contacts', 'agency:privacy', 'agency:vacancies',
            'agency:reviews', 'agency:promocodes', 'agency:tours', 'agency:register'
        ]
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            assert response.status_code == 200

    def test_news_detail_view(self, mock_usd, mock_weather):
        """Test the regex path for news details."""
        article = NewsArticle.objects.create(title="T", summary="S", content="C")
        response = self.client.get(reverse('agency:news_detail', kwargs={'pk': article.id}))
        assert response.status_code == 200
        assert response.context['article'] == article

    def test_tour_list_filtering(self, mock_usd, mock_weather):
        """Test the get_queryset filter logic in TourListView."""
        response = self.client.get(reverse('agency:tours'), {'country': 'Test', 'max_price': 150, 'stars': 5})
        assert response.status_code == 200
        assert len(response.context['tours']) == 1

    def test_role_based_access_controls(self, mock_usd, mock_weather):
        """Test Mixins (ClientRequired, EmployeeRequired, SuperuserRequired)."""
        # 1. Anonymous user should be redirected to login
        assert self.client.get(reverse('agency:client_dashboard')).status_code == 302

        # 2. Employee trying to access Client Dashboard -> 403 Forbidden
        self.client.login(username='emp1', password='password123')
        assert self.client.get(reverse('agency:client_dashboard')).status_code == 403

        # 3. Client trying to access Employee Dashboard -> 403 Forbidden
        self.client.login(username='client1', password='password123')
        assert self.client.get(reverse('agency:employee_dashboard')).status_code == 403

        # 4. Client trying to access Admin Statistics -> 403 Forbidden
        assert self.client.get(reverse('agency:admin_statistics')).status_code == 403

        # 5. Admin accessing Admin Statistics -> 200 OK
        self.client.login(username='admin1', password='password123')
        assert self.client.get(reverse('agency:admin_statistics')).status_code == 200

    def test_order_creation_and_acceptance(self, mock_usd, mock_weather):
        """Test the full workflow: Client books a tour -> Employee accepts it."""
        # 1. Client books the tour
        self.client.login(username='client1', password='password123')
        response = self.client.post(reverse('agency:book_tour', kwargs={'tour_id': self.tour.id}), {
            'departure_date': '2026-10-10'
        })
        assert response.status_code == 302  # Redirects to dashboard on success

        order = Order.objects.first()
        assert order.client == self.client_profile
        assert order.employee is None  # Pending status

        # 2. Employee accepts the order
        self.client.login(username='emp1', password='password123')
        response = self.client.post(reverse('agency:accept_order', kwargs={'pk': order.id}))
        assert response.status_code == 302

        order.refresh_from_db()
        assert order.employee == self.emp_profile  # Employee assigned

    def test_review_crud_operations(self, mock_usd, mock_weather):
        """Test Create, Update, Delete for reviews."""
        self.client.login(username='client1', password='password123')

        # Create
        self.client.post(reverse('agency:add_review'), {'rating': 5, 'text': 'Awesome!'})
        review = Review.objects.first()
        assert review.text == 'Awesome!'
        assert review.client_name == 'client1'  # Based on our form_valid logic

        # Update
        self.client.post(reverse('agency:edit_review', kwargs={'pk': review.id}), {'rating': 4, 'text': 'Good!'})
        review.refresh_from_db()
        assert review.rating == 4
        assert review.text == 'Good!'

        # Delete
        self.client.post(reverse('agency:delete_review', kwargs={'pk': review.id}))
        assert Review.objects.count() == 0

    def test_user_registration_form_valid(self, mock_usd, mock_weather):
        """Unit test the form_valid method directly to bypass complex password validation."""
        from agency.views import RegisterView
        from unittest.mock import MagicMock

        view = RegisterView()
        view.request = MagicMock()

        mock_form = MagicMock()
        new_user = User.objects.create(username="new_direct_client")
        mock_form.save.return_value = new_user
        mock_form.cleaned_data = {
            'patronymic': 'Ivanovich',
            'address': 'Minsk',
            'phone': '+375291234567',
            'birth_date': date(2000, 1, 1)
        }

        response = view.form_valid(mock_form)

        assert response.status_code == 302
        new_profile = Profile.objects.get(user=new_user)
        assert new_profile.role == 'client'
        assert new_profile.address == 'Minsk'

    def test_profile_detail_view(self, mock_usd, mock_weather):
        """Test the profile page loading for logged-in users."""
        self.client.login(username='client1', password='password123')
        response = self.client.get(reverse('agency:profile_detail'))
        assert response.status_code == 200
        assert response.context['profile'] == self.client_profile

    def test_client_dashboard_success(self, mock_usd, mock_weather):
        """Test successful load of Client Dashboard to cover get_context_data."""
        self.client.login(username='client1', password='password123')
        response = self.client.get(reverse('agency:client_dashboard'))
        assert response.status_code == 200
        assert 'my_orders' in response.context

    def test_employee_dashboard_success(self, mock_usd, mock_weather):
        """Test successful load of Employee Dashboard to cover get_context_data."""
        self.client.login(username='emp1', password='password123')
        response = self.client.get(reverse('agency:employee_dashboard'))
        assert response.status_code == 200
        assert 'pending_orders' in response.context

    def test_admin_statistics_success(self, mock_usd, mock_weather):
        """Test successful load of Admin Statistics to cover get_context_data."""
        self.client.login(username='admin1', password='password123')
        response = self.client.get(reverse('agency:admin_statistics'))
        assert response.status_code == 200
        assert 'sales_stats' in response.context