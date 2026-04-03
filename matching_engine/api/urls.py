from django.urls import path
from .views import OrderCreateView, OrderBookView, OrderListView, TradeListView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/list/', OrderListView.as_view(), name='order-list'),
    path('orderbook/', OrderBookView.as_view(), name='orderbook'),
    path('trades/', TradeListView.as_view(), name='trade-list'),
]
