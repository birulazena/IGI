from django.urls import path, re_path
from . import views

app_name = 'agency'

urlpatterns = [
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^about/$', views.CompanyInfoView.as_view(), name='about'),
    re_path(r'^news/$', views.NewsListView.as_view(), name='news_list'),
    re_path(r'^news/(?P<pk>\d+)/$', views.NewsDetailView.as_view(), name='news_detail'),

    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('contacts/', views.ContactsListView.as_view(), name='contacts'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('promocodes/', views.PromoCodeListView.as_view(), name='promocodes'),
    path('tours/', views.TourListView.as_view(), name='tours'),
    path('dashboard/client/', views.ClientDashboardView.as_view(), name='client_dashboard'),
    path('dashboard/employee/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('dashboard/statistics/', views.AdminStatisticsView.as_view(), name='admin_statistics'),
    path('reviews/add/', views.ReviewCreateView.as_view(), name='add_review'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='edit_review'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('tours/<int:tour_id>/book/', views.OrderCreateView.as_view(), name='book_tour'),
    path('orders/<int:pk>/accept/', views.OrderAcceptView.as_view(), name='accept_order'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('concurrency/', views.ConcurrencyDemoView.as_view(), name='concurrency'),
]