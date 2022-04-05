from django import template
from order.models import Cart, Order


register = template.Library()


# all cart filter
@register.filter
def cart_view(user):
    cart = Cart.objects.filter(user=user, purchased=False)
    if cart.exists():
        return cart
    else:
        return ValueError("You haven't an active cart!")


# total price filter
@register.filter
def cart_total_price(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].get_total_price()
    else:
        return 0


# total quantity filter
@register.filter
def product_quantity_total(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].get_quantity()
    else:
        return 0

# total item filter


@register.filter
def cart_count(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0
