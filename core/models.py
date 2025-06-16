from django.db import models
from django.db.models import F, Sum

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=200, blank=True)

    @property
    def total_amount(self):
        return self.saleitem_set.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

    def __str__(self):
        return f"Sale #{self.id}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of sale

    @property
    def subtotal(self):
        return self.quantity * self.price