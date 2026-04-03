from django.db import transaction
from ..repositories.order_repository import OrderRepository
from ..core.engine import MatchingEngine

class MatchingService:
    def __init__(self):
        self.repository = OrderRepository()

    def process_new_order(self, order):
        with transaction.atomic():
            # 1. Lock and get opposite side orders for matching
            opposite_side = 'SELL' if order.side == 'BUY' else 'BUY'
            maker_orders = self.repository.get_active_orders(opposite_side)
            
            # 2. Initialize Engine and Match
            engine = MatchingEngine(bids=maker_orders if order.side == 'SELL' else [], 
                                   asks=maker_orders if order.side == 'BUY' else [])
            
            result = engine.match(order)
            
            # 3. Persist Trades and Update Maker Orders
            for trade_data in result.trades:
                maker = trade_data['maker_order']
                self.repository.create_trade(
                    maker=maker,
                    taker=order,
                    price=trade_data['price'],
                    qty=trade_data['quantity']
                )
                
                # Update Maker Status
                maker.status = 'FILLED' if maker.remaining_quantity == 0 else 'PARTIAL'
                maker.save()
            
            # 4. Update Taker Order
            order.remaining_quantity = result.remaining_qty
            order.status = 'FILLED' if order.remaining_quantity == 0 else ('PARTIAL' if len(result.trades) > 0 else 'PENDING')
            self.repository.save_order(order)
            
            return order
