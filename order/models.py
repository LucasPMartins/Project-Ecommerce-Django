from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Accepted'),
            ('C', 'Created'),
            ('R', 'Rejected'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        )
    )
    def __str__(self):
        return f'Order {self.id} of {self.user.username}'
    
    def save(self, *args, **kwargs):
        super_save = super().save(*args, **kwargs)
        self.total = sum([item.price * item.quantity for item in self.items.all()]) if self.items.all() else 0
        return super_save

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    price_promotional = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item {self.product} of {self.order}'
