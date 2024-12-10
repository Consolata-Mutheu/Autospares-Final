from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="user.jpg")
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = []
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    fname = models.CharField(max_length=200, null=False)
    lname = models.CharField(max_length=200, null=False)
    email = models.EmailField(unique=True)
    employee_id =models.CharField(max_length=20, unique=True, null=False)
    joining_date = models.DateField(null=True)
    phone_no = models.CharField(max_length=15, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    avatar = models.ImageField(null=True, default="user.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return self.fname
    
    def get_department_name(self):
        return self.department.name if self.department else "--"


#customer
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} "


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, related_name="supplied_products", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.quantity > 0

#0rders
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        PROCESSING = 'Processing', _('Processing')
        COMPLETED = 'Completed', _('Completed')
        CANCELED = 'Canceled', _('Canceled')

    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name="orders"
    )
    product = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} for {self.customer.name}"


    #sales report
class SalesReport(models.Model):
    report_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_products_sold = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Sales Report')
        verbose_name_plural = _('Sales Reports')

    def __str__(self):
        return f"{self.report_name} ({self.start_date} - {self.end_date})"

    def calculate_totals(self):
        """Calculate total sales and products sold within the date range."""
        orders = Order.objects.filter(order_date__range=[self.start_date, self.end_date], status=Order.Status.COMPLETED)
        self.total_sales = sum(order.price * order.quantity for order in orders)
        self.total_products_sold = sum(order.quantity for order in orders)
        self.save()








    