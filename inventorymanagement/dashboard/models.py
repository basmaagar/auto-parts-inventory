from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# CATALOG
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Part(models.Model):
    name = models.CharField(max_length=100)
    reference = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100 ,null=True)
    price = models.IntegerField(default=100, verbose_name="Price")
    technical_specs = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantityinstock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='part_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.reference})"


class Compatibility(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    vehicle_brand = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    year_start = models.IntegerField()
    year_end = models.IntegerField()

    def __str__(self):
        return f"{self.vehicle_brand} {self.vehicle_model} ({self.year_start}-{self.year_end})"


class Order(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_quantity = models.PositiveBigIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.part.name} ordered by {self.user.username} -quantity: {self.order_quantity}"

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} for order {self.order.id}"
