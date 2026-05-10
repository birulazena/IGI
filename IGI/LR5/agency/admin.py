from django.contrib import admin
from .models import (
    Profile, Country, Hotel, Tour, Order,
    NewsArticle, CompanyInfo, FAQ, Vacancy, Review, PromoCode,
    EmployeeContact
)

admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(Hotel)
admin.site.register(Tour)
admin.site.register(Order)
admin.site.register(NewsArticle)
admin.site.register(CompanyInfo)
admin.site.register(FAQ)
admin.site.register(EmployeeContact)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)