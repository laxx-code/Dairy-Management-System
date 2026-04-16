from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone= models.CharField(max_length=10,          unique=True)
    address= models.TextField()

    def __str__(self):
        return self.name


class BakeryProduct(models.Model):
    CATEGORY_CHOICES = [ ('Dairy','dairy '), ('Bakery','bakery'),]
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DailySupply(models.Model):
    SUPPLY_TYPE_CHOICES = (
        ("milk", "Milk"),
        ("bakery", "Bakery"),
    )

    supply_type = models.CharField(max_length=10, choices=SUPPLY_TYPE_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    milk_quantity = models.FloatField(null=True, blank=True)

    bakery_product = models.ForeignKey(BakeryProduct, null=True, blank=True, on_delete=models.SET_NULL)
    bakery_quantity = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    date = models.DateField()



class Vendor(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class MilkRecord(models.Model):
    MILK_TYPE_CHOICES = (
        ("cow", "Cow"),
        ("buffalo", "Buffalo"),
        ("mixed", "Mixed"),
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    milk_type = models.CharField(max_length=10, choices=MILK_TYPE_CHOICES)

    quantity = models.FloatField()      # in liters or kg
    fat = models.FloatField()
    snf = models.FloatField()
    clr = models.FloatField(blank=True, null=True)
    water = models.FloatField(blank=True, null=True)

    rate_per_liter = models.FloatField()
    total_amount = models.FloatField()

    def save(self, *args, **kwargs):
        # Auto-calc total to avoid cheating/bugs from frontend
        self.total_amount = self.quantity * self.rate_per_liter
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor.name} - {self.date_time}"

class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    note = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - ₹{self.amount}"