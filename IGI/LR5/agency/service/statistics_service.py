import statistics
from datetime import date
from django.db.models import Sum
from agency.models import Profile, Order

class StatisticsService:
    """Service for calculating business statistics"""

    @staticmethod
    def get_sales_stats() -> dict:
        """Calculates mean, median, and mode for sales amounts."""
        orders = Order.objects.annotate(total_price=Sum('tours__price'))
        prices = [float(order.total_price) for order in orders if order.total_price]

        if not prices:
            return {"mean": 0, "median": 0, "mode": 0}

        mode_val = 0
        try:
            mode_val = statistics.mode(prices)
        except Exception:
            mode_val = "No unique mode"

        return {
            "mean": round(statistics.mean(prices), 2),
            "median": round(statistics.median(prices), 2),
            "mode": mode_val
        }

    @staticmethod
    def get_clients_age_stats() -> dict:
        """Calculates mean and median for clients' ages."""
        clients = Profile.objects.filter(role='client')
        today = date.today()

        ages = []
        for c in clients:
            age = today.year - c.birth_date.year - ((today.month, today.day) < (c.birth_date.month, c.birth_date.day))
            ages.append(age)

        if not ages:
            return {"mean": 0, "median": 0}

        return {
            "mean": round(statistics.mean(ages), 1),
            "median": round(statistics.median(ages), 1)
        }

