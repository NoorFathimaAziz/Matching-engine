from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, TradeSerializer
from ..services.matching_service import MatchingService
from ..models.order import Order
from ..models.trade import Trade


class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(remaining_quantity=serializer.validated_data['quantity'])
            
            service = MatchingService()
            processed_order = service.process_new_order(order)
            
            return Response(OrderSerializer(processed_order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(APIView):
    def get(self, request):
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = Order.objects.filter(status=status_filter.upper()).order_by('-created_at')
        else:
            orders = Order.objects.all().order_by('-created_at')
            
        return Response(OrderSerializer(orders, many=True).data)

class OrderBookView(APIView):
    def get(self, request):
        bids = Order.objects.filter(side='BUY', status__in=['PENDING', 'PARTIAL']).order_by('-price', 'created_at')
        asks = Order.objects.filter(side='SELL', status__in=['PENDING', 'PARTIAL']).order_by('price', 'created_at')
        
        return Response({
            'bids': OrderSerializer(bids, many=True).data,
            'asks': OrderSerializer(asks, many=True).data
        })

class TradeListView(APIView):
    def get(self, request):
        trades = Trade.objects.all().order_by('-created_at')
        return Response(TradeSerializer(trades, many=True).data)
