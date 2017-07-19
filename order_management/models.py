from entity_management.models import Product
from customer_profile.models import Customer
from django.db.models import (
    Model,
    ForeignKey,
    PROTECT,
    CASCADE,
    PositiveIntegerField,
    DateTimeField,
    CharField,
    FloatField
)


class Order(Model):
    ORDER_STATUSES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('S', 'Shipped'),
        ('C', 'Cancelled')
    )

    date_ordered = DateTimeField(auto_now=True)
    customer = ForeignKey(Customer, on_delete=CASCADE)
    status = CharField(max_length=2, choices=ORDER_STATUSES, default='P')

    def total_price(self):
        order_items = self.orderlineitems_set.all()
        total_price = 0
        for order_item in order_items:
            total_price += order_item.line_price()
        return total_price

    def has_products(self, *products):
        for product in products:
            print(product)
            if not self.has_product(product):
                return False
        return True

    def has_product(self, product):
        order_items = self.orderlineitems_set.all()
        for order_item in order_items:
            if order_item.product == product:
                return True
        return False


class OrderLineItems(Model):
    # TODO: Prevent product deletion when ordered
    product = ForeignKey(Product, on_delete=PROTECT)
    quantity = PositiveIntegerField(),
    parent_order = ForeignKey(Order, on_delete=CASCADE)

    def line_price(self):
        return self.product.price * self.quantity

class ProductAssociation(Model):
    root_product = ForeignKey(Product, on_delete=PROTECT, related_name="root_product")
    associated_product = ForeignKey(Product, on_delete=PROTECT,related_name="associated_product")
    probability = FloatField()

    def __str__(self):
        return f"{self.root_product.name} to {self.associated_product.name} - {self.probability}"