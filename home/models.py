from django.db import models
from authen.models import User

STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )


ORDER_TYPE = (
    ('DINE IN' , 'Dine In'),
    ('DELIVERY' , 'Delivery'),
    ('PICK UP' , 'Pick UP'),
)

PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('ONLINE', 'Online Payment'),
    )
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

class Floorname(TimeStampedModel):
    floorname = models.CharField(max_length=100 , blank=True)
    def __str__(self):
        return self.floorname
    

class Table(TimeStampedModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True ,  related_name="user")
    floor = models.ForeignKey(Floorname , on_delete=models.CASCADE , blank=True ,  related_name="tables")
    table_number = models.IntegerField(default=0)
    
   


class Menucategroy(TimeStampedModel):   
      name = models.CharField(max_length=150 , blank=True)
      def __str__(self):
          return self.name
      

class MenuItem(TimeStampedModel):
     
      menucategory = models.ForeignKey(Menucategroy , on_delete=models.CASCADE , null=True ,  related_name="menucategroy")
      item_name = models.CharField(max_length=150, blank=True)
      description = models.TextField(blank=True)
      item_price = models.DecimalField(max_digits=10,decimal_places=2)
      is_avaiable = models.BooleanField(default=True)

      def __str__(self):
          return self.item_name
      

class Order(TimeStampedModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True ,  related_name="order_user")
    table_order = models.ForeignKey(Table, on_delete=models.CASCADE , related_name="order_tables")
    floor = models.ForeignKey(Floorname , on_delete=models.CASCADE  ,  related_name="floors")
    order_type = models.CharField(max_length=250 , choices=ORDER_TYPE , default='Dine In')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.status
      

class OrderItem(TimeStampedModel):
    order_item= models.ForeignKey(Order , on_delete=models.CASCADE , related_name="orderitems")
    menu_item = models.ForeignKey(MenuItem , on_delete=models.CASCADE , related_name="items")
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return super().__str__()     
    

 
class Payment(models.Model):    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
   
    def __str__(self):
        return self.payment_method