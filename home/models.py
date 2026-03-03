from django.db import models
from authen.models import User
from decimal import Decimal, getcontext

STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('PROCESSING', 'Processing'),
    ('SUCCESS', 'Success'),    
    ('FAILED', 'Failed'),  
    ('COMPLETED','Completed'),     
    ('CANCELLED', 'Cancelled'),
)



ORDER_TYPES = (
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

    orderType = models.CharField(max_length=20, choices=ORDER_TYPES , default='DINE IN')
    tableID = models.ForeignKey(Table, on_delete=models.CASCADE , null=True , related_name="order_tables")
    waiterId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="waiter_orders"
    )
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grandTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    person = models.IntegerField(default=0)


    def update_totals(self):
     
        items = self.items.all()
        subtotal = sum(item.totalPrice for item in items)
        tax = subtotal * Decimal(0.10)
        grand_total = subtotal + tax - self.discount
        self.subtotal = subtotal
        self.tax = tax
        self.grandTotal = grand_total
        self.save(update_fields=["subtotal", "tax", "grandTotal"])

    def __str__(self):
        return f"{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items",  null=True ,  on_delete=models.CASCADE)
    itemId = models.ForeignKey(MenuItem , on_delete=models.CASCADE , related_name="items")
    quantity = models.IntegerField(default=1)
    sent_quantity = models.IntegerField(default=0)
    

    @property
    def itemName(self):
        return self.itemId.item_name

    @property
    def price(self):
        return self.itemId.item_price

    @property
    def totalPrice(self):
        return self.price * self.quantity

    def __str__(self):
        return self.itemName
    
    
    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        if order:
            order.update_totals()


  

class KOT(models.Model):

    STATUS_CHOICES = (
    ("NEW", "New"),
    ("PREPARING", "Preparing"),
    ("READY", "Ready"),
    )

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="kots"
    )

    kot_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NEW"
    )
  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ("order", "kot_number")  

  
class KOTItem(models.Model):
    kot = models.ForeignKey(
        KOT,
        on_delete=models.CASCADE,
        related_name="items"
    )

    items = models.ForeignKey(
        "MenuItem",
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)
    is_sent_kot = models.BooleanField(default=False)
    class Meta:
        verbose_name = "KOT Item"
        verbose_name_plural = "KOT Items"


      
class Payment(models.Model):    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES ,  default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
   
    def __str__(self):
        return self.payment_method
    
