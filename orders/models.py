from django.db import models
from shop.models import Product

# Create your models here.

class Order(models.Model):
    first_name = models.CharField(('Imię'), max_length=50)
    last_name = models.CharField(('Nazwisko'), max_length=50)
    email = models.EmailField(('E-mail'),)
    address = models.CharField(('Adres'), max_length=250)
    postal_code = models.CharField(('Kod pocztowy'), max_length=20)
    city = models.CharField(('Miejscowość'), max_length=100)
    created = models.DateTimeField(('Utworzone'), auto_now_add=True)
    updated = models.DateTimeField(('Uaktualnione'), auto_now=True)
    paid = models.BooleanField(('Opłacone'), default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product,
                                related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)



    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
