from django.db import transaction
from ..models.order import Order
from ..models.trade import Trade

from ..core.engine import MatchingEngine

class OrderRepository:
    @staticmethod
    def get_active_orders(side):
        return Order.objects.filter(
            side=side, 
            status__in=['PENDING', 'PARTIAL']
        ).select_for_update()

    @staticmethod
    def save_order(order):
        order.save()

    @staticmethod
    def create_trade(maker, taker, price, qty):
        return Trade.objects.create(
            maker_order=maker,
            taker_order=taker,
            price=price,
            quantity=qty
        )
