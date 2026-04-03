from django.test import TestCase
from decimal import Decimal
from ..models.order import Order
from ..core.engine import MatchingEngine

class MatchingEngineTest(TestCase):
    def test_basic_match(self):
        # Setup bids and asks
        bid = Order(price=Decimal('100'), remaining_quantity=Decimal('10'), side='BUY')
        ask = Order(price=Decimal('100'), remaining_quantity=Decimal('5'), side='SELL')
        
        engine = MatchingEngine(bids=[bid], asks=[])
        result = engine.match(ask)
        
        self.assertEqual(len(result.trades), 1)
        self.assertEqual(result.trades[0]['quantity'], Decimal('5'))
        self.assertEqual(result.remaining_qty, Decimal('0'))
