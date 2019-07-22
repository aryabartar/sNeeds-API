from sNeeds.apps.carts.models import Cart
from sNeeds.apps.orders.models import Order, SoldCart


def accept_order_pay(order):
   cart = order.cart
