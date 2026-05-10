import calendar
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    NewsArticle, CompanyInfo, FAQ, EmployeeContact,
    Vacancy, Review, PromoCode, Profile, Tour, Order
)
from .service.weather_service import WeatherService
from .service.currency_service import CurrencyService
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ReviewForm, OrderForm, UserRegisterForm
from .service.statistics_service import StatisticsService
from django.db.models import Count, Sum, Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .service.concurrency_service import ConcurrencyService

import logging

logger = logging.getLogger(__name__)

class BaseContextMixin:
    """
    Mixin to provide common context data required by the assignment:
    Timezones, text calendar, current dates, and external API data.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['current_date'] = now.strftime('%d/%m/%Y')
        context['utc_date'] = datetime.now(dt_timezone.utc).strftime('%d/%m/%Y %H:%M:%S')
        context['user_timezone'] = timezone.get_current_timezone_name()

        cal = calendar.TextCalendar(calendar.MONDAY)
        context['text_calendar'] = cal.formatmonth(now.year, now.month)

        context['usd_rate'] = CurrencyService.get_usd_rate()
        context['weather'] = WeatherService.get_current_weather("Minsk")

        return context

class HomeView(BaseContextMixin, TemplateView):
    template_name = 'agency/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_article'] = NewsArticle.objects.order_by('-created_at').first()
        return context

class CompanyInfoView(BaseContextMixin, TemplateView):
    template_name = 'agency/company_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyInfo.objects.first()
        return context

class NewsListView(BaseContextMixin, ListView):
    model = NewsArticle
    template_name = 'agency/news_list.html'
    context_object_name = 'articles'
    ordering = ['-created_at']

class NewsDetailView(BaseContextMixin, DetailView):
    model = NewsArticle
    template_name = 'agency/news_detail.html'
    context_object_name = 'article'

class FAQListView(BaseContextMixin, ListView):
    model = FAQ
    template_name = 'agency/faq_list.html'
    context_object_name = 'faqs'
    ordering = ['-added_at']

class ContactsListView(BaseContextMixin, ListView):
    model = EmployeeContact
    template_name = 'agency/contacts.html'
    context_object_name = 'employees'

class PrivacyPolicyView(BaseContextMixin, TemplateView):
    template_name = 'agency/privacy_policy.html'

class VacancyListView(BaseContextMixin, ListView):
    model = Vacancy
    template_name = 'agency/vacancies.html'
    context_object_name = 'vacancies'

class ReviewListView(BaseContextMixin, ListView):
    model = Review
    template_name = 'agency/reviews.html'
    context_object_name = 'reviews'
    ordering = ['-date_posted']

class PromoCodeListView(BaseContextMixin, ListView):
    model = PromoCode
    template_name = 'agency/promo_codes.html'
    context_object_name = 'promos'

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'client'

class EmployeeRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'employee'

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class TourListView(BaseContextMixin, ListView):
    model = Tour
    template_name = 'agency/tour_list.html'
    context_object_name = 'tours'

    def get_queryset(self):
        queryset = super().get_queryset()

        country = self.request.GET.get('country')
        max_price = self.request.GET.get('max_price')
        stars = self.request.GET.get('stars')

        if country:
            queryset = queryset.filter(hotel__country__name__icontains=country)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if stars:
            queryset = queryset.filter(hotel__stars=stars)

        return queryset

class ClientDashboardView(LoginRequiredMixin, ClientRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'agency/client_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_orders'] = Order.objects.filter(client=self.request.user.profile)
        context['available_promos'] = PromoCode.objects.filter(is_active=True)
        return context


class EmployeeDashboardView(LoginRequiredMixin, EmployeeRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'agency/employee_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_sales'] = Order.objects.filter(employee=self.request.user.profile)
        context['pending_orders'] = Order.objects.filter(employee__isnull=True)
        return context


class AdminStatisticsView(LoginRequiredMixin, SuperuserRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'agency/admin_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales_stats'] = StatisticsService.get_sales_stats()
        context['age_stats'] = StatisticsService.get_clients_age_stats()
        context['hotels'] = Tour.objects.select_related('hotel', 'hotel__country').all()
        context['client_stats'] = Profile.objects.filter(role='client').annotate(
            tours_count=Count('client_orders__tours'),
            total_spent=Sum('client_orders__tours__price')
        )
        return context

class ReviewCreateView(LoginRequiredMixin, BaseContextMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'agency/review_form.html'
    success_url = reverse_lazy('agency:reviews')

    def form_valid(self, form):
        full_name = f"{self.request.user.first_name} {self.request.user.last_name}".strip()
        form.instance.client_name = full_name or self.request.user.username
        return super().form_valid(form)

class ProfileDetailView(LoginRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'agency/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context

class ReviewUpdateView(LoginRequiredMixin, BaseContextMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'agency/review_form.html'
    success_url = reverse_lazy('agency:reviews')

class ReviewDeleteView(LoginRequiredMixin, BaseContextMixin, DeleteView):
    model = Review
    template_name = 'agency/review_confirm_delete.html'
    success_url = reverse_lazy('agency:reviews')


class OrderCreateView(LoginRequiredMixin, ClientRequiredMixin, BaseContextMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'agency/order_form.html'
    success_url = reverse_lazy('agency:client_dashboard')

    def form_valid(self, form):
        form.instance.client = self.request.user.profile
        response = super().form_valid(form)

        tour_id = self.kwargs.get('tour_id')
        tour = get_object_or_404(Tour, id=tour_id)
        self.object.tours.add(tour)
        logger.info(f"Client '{self.request.user.username}' created a new order for Tour ID: {tour.id}.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tour'] = get_object_or_404(Tour, id=self.kwargs.get('tour_id'))
        return context


class OrderAcceptView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, employee__isnull=True)
        order.employee = request.user.profile
        order.save()
        logger.info(f"Employee '{request.user.username}' accepted Order ID: {order.id}.")
        return redirect('agency:employee_dashboard')


class RegisterView(BaseContextMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        Profile.objects.create(
            user=user,
            role='client',
            patronymic=form.cleaned_data.get('patronymic'),
            address=form.cleaned_data.get('address'),
            phone=form.cleaned_data.get('phone'),
            birth_date=form.cleaned_data.get('birth_date')
        )
        logger.info(f"New user registered: {user.username} as client.")
        return super().form_valid(form)

class ConcurrencyDemoView(BaseContextMixin, TemplateView):
    template_name = 'agency/concurrency.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        texts, time_a = ConcurrencyService.run_task_a_threading()
        context['time_a'] = round(time_a, 4)
        context['articles_downloaded'] = len(texts)

        top_words, time_b = ConcurrencyService.run_task_b_multiprocessing(texts)
        context['time_b'] = round(time_b, 4)
        context['top_words'] = top_words

        results_c, time_c = ConcurrencyService.run_task_c_asyncio()
        context['time_c'] = round(time_c, 4)
        context['async_results'] = results_c

        return context