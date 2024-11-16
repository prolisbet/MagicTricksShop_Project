from django.test import TestCase
from .models import Order, OrderItem
from shopUsers.models import User
from shopGoods.models import Product
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MagicTricksShop.settings')
django.setup()


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test User", email="test@example.com")
        self.product = Product.objects.create(name="Magic Wand", price=100)
        self.order = Order.objects.create(user=self.user, status="pending")
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, "pending")

    def test_order_item_total(self):
        total = self.order_item.quantity * self.order_item.product.price
        self.assertEqual(total, 200)
