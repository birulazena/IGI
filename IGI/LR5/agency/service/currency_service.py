import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class CurrencyService:
    """Service to handle National Bank of the Republic of Belarus API"""

    @staticmethod
    def get_usd_rate() -> float:
        """
        Fetches the current USD to BYN exchange rate.
        Returns 0.0 if the request fails.
        """

        url = f"{settings.NBRB_API_URL}/431"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return float(data.get('Cur_OfficialRate', 0.0))
        except requests.RequestException as e:
            logger.error(f"Failed to fetch currency rate: {e}")
            return 0.0