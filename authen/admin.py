from django.contrib import admin
from authen.models import User 
from home.models import Floorname , Table , Menucategroy , MenuItem , Order , OrderItem ,  KOT , KOTItem ,  Payment 

# Register your models here.
admin.site.register(User)
# Register your models here.
admin.site.register(Floorname)
admin.site.register(Table)
admin.site.register(Menucategroy)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(KOT)
admin.site.register(KOTItem)
admin.site.register(Payment)