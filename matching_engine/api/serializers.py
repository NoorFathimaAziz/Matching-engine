from rest_framework import serializers
from ..models.order import Order
from ..models.trade import Trade

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'side', 'price', 'quantity', 'remaining_quantity', 'status', 'created_at']
        read_only_fields = ['id', 'remaining_quantity', 'status', 'created_at']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
