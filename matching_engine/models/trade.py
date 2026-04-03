from django.db import models
from .order import Order
from django.utils import timezone



class Trade(models.Model):
    maker_order = models.ForeignKey(Order, related_name='maker_trades', on_delete=models.CASCADE)
    taker_order = models.ForeignKey(Order, related_name='taker_trades', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=18, decimal_places=8)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    created_at = models.DateTimeField(default=timezone.now)