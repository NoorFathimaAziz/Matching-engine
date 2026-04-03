from decimal import Decimal
from dataclasses import dataclass
from typing import List

@dataclass
class MatchResult:
    trades: List[dict]
    remaining_qty: Decimal

class MatchingEngine:
   
    def __init__(self, bids: List[any], asks: List[any]):
        self.bids = sorted(bids, key=lambda x: (-x.price, x.created_at))
        self.asks = sorted(asks, key=lambda x: (x.price, x.created_at))

    def match(self, taker_order) -> MatchResult:
        trades = []
        remaining_qty = taker_order.remaining_quantity
        
        opposite_side = self.asks if taker_order.side == 'BUY' else self.bids
        
        for maker_order in opposite_side[:]:
            if remaining_qty <= 0:
                break
                
            # Price Check
            can_match = (taker_order.side == 'BUY' and taker_order.price >= maker_order.price) or \
                        (taker_order.side == 'SELL' and taker_order.price <= maker_order.price)
            
            if not can_match:
                break
                
            # Calculate Fill
            fill_qty = min(remaining_qty, maker_order.remaining_quantity)
            
            trades.append({
                'maker_order': maker_order,
                'price': maker_order.price,
                'quantity': fill_qty
            })
            
            remaining_qty -= fill_qty
            maker_order.remaining_quantity -= fill_qty
            
        return MatchResult(trades=trades, remaining_qty=remaining_qty)
