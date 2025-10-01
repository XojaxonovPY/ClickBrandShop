from apps.urls.market import urlpatterns as market
from apps.urls.log_reg import urlpatterns as log_reg
from apps.urls.orders import urlpatterns as orders
from apps.urls.profile import urlpatterns as profile
from apps.urls.search import urlpatterns as search

urlpatterns = [
    *market,
    *log_reg,
    *orders,
    *profile,
    *search
]
