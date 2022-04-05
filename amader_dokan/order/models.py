from django.db import models
from django.contrib.auth.models import User
from store.models import Product, VariationValue


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.quantity} X {self.item}"

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total

    def variation_single_price(self):
        sizes = VariationValue.objects.filter(
            variation='size', product=self.item)
        colors = VariationValue.objects.filter(
            variation='color', product=self.item)
        for size in sizes:
            if colors.exists():
                for color in colors:
                    if color.name == self.color:
                        c_price = color.price
                if size.name == self.size:
                    total = size.price + c_price
                    net_total = total
                    float_total = format(net_total, '0.2f')
                    return float_total
            else:
                if size.name == self.size:
                    total = size.price
                    float_total = format(total, '0.2f')
                    return float_total

    def variation_total(self):
        sizes = VariationValue.objects.filter(
            variation='size', product=self.item)
        colors = VariationValue.objects.filter(
            variation='color', product=self.item)
        for size in sizes:
            if colors.exists():
                for color in colors:
                    if color.name == self.color:
                        c_price = color.price
                        color_quantity_price = c_price * self.quantity
                if size.name == self.size:
                    total = size.price * self.quantity
                    net_total = total + color_quantity_price
                    float_total = format(net_total, '0.2f')
                    return float_total
            else:
                if size.name == self.size:
                    total = size.price * self.quantity
                    float_total = format(total, '0.2f')
                    return float_total


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=255, blank=True, null=True)
    orderId = models.CharField(max_length=255, blank=True, null=True)

    # def get_totals(self):
    #     total = 0
    #     for order_item in self.orderitems.all():
    #         total += float(order_item.get_total())
    #     return total

    def get_total_price(self):
        total_price = 0
        for item_price in self.orderitems.all():
            if item_price.variation_total():
                total_price += float(item_price.variation_total())
            elif item_price.variation_single_price():
                total_price += float(item_price.variation_single_price())
            else:
                total_price += float(item_price.get_total())
        return total_price

    def get_quantity(self):
        total_quantity = 0
        for order_items in self.orderitems.all():
            total_quantity += int(order_items.quantity)
        return total_quantity
