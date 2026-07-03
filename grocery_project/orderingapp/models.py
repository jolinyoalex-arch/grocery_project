from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import random
import string

# 1. Custom User Model ya Roles (Customer, Vendor, Admin)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    )
    # Hapa tumeweka max_length pekee (Hakuna max_value)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.username} ({self.get_role_display()})"


# Email Verification Code Model
class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification code for {self.user.email}"
    
    def is_valid(self):
        """Check if the code is still valid and not used"""
        return not self.is_used and timezone.now() < self.expires_at
    
    @staticmethod
    def generate_code():
        """Generate a random 6-digit code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def create_code_for_user(user):
        """Create a new verification code for a user"""
        # Delete old codes if they exist
        VerificationCode.objects.filter(user=user).delete()
        
        code = VerificationCode.generate_code()
        expires_at = timezone.now() + timedelta(minutes=10)
        
        return VerificationCode.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )


# 2. Profaili ya Muuzaji (Vendor Profile)
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'vendor'})
    shop_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    def _str_(self):
        return self.shop_name


# 3. Makundi ya Bidhaa (e.g., Flour, Rice, Cooking Oil)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def _str_(self):
        return self.name


# 4. Model ya Bidhaa
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # max_digits na decimal_places ni sahihi hapa kwa namba
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def _str_(self):
        return f"{self.name} - TZS {self.price} ({self.vendor.shop_name})"


# 5. Oda (Order)
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_address = models.TextField()

    def _str_(self):
        return f"Order #{self.id} by {self.customer.username}"


# 6. Vitu vilivyomo kwenye Oda (Order Items)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.quantity} x {self.product.name} for Order #{self.order.id}"