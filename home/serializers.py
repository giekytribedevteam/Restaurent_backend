from rest_framework import serializers
from django.utils import timezone
from .models import User ,  Floorname , Table , Menucategroy , MenuItem , Order , OrderItem , Payment , KOT , KOTItem
from decimal import Decimal 


class TableSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Table
        fields = ['id' , 'user' , 'floor' , 'table_number']
        read_only_fields = ['id' , 'floor']

class FloorSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True , required=False) 
    table_count = serializers.IntegerField(write_only=True , required=False)

   
    class Meta:
        model = Floorname
        fields = ['id', 'floorname' , 'tables' , 'table_count' ]
            
    def create(self , validated_data):
        table_counts = validated_data.pop("table_count" ,[])
        floor = Floorname.objects.create(**validated_data)
        for i in range(1 , table_counts + 1 ):
          Table.objects.create(floor=floor , 
                                table_number=f"{i}")

        return floor 
    

    def update(self, instance, validated_data):
        table_counts = validated_data.pop("table_count" , None)
        instance.floorname = validated_data.pop('floorname' , instance.floorname)
        instance.save()
        
        if table_counts:
            exiting_table = instance.tables.count()
            for i in range(exiting_table + 1 , exiting_table + table_counts + 1):
                Table.objects.create(floor=instance , table_number=f"{i}")
        
        return instance
    

class MenucategroySerializer(serializers.ModelSerializer):
        class Meta:
            model = Menucategroy
            fields = ['id', 'name']


class MenuItemSerializer(serializers.ModelSerializer):
        category = MenucategroySerializer(required=False , source="menucategory")
        class Meta:
            model = MenuItem
            fields = ['id'  , 'menucategory'  , "category"  ,'item_name' , 'description' , 'item_price' , 'is_avaiable']  



class OrderItemSerializer(serializers.ModelSerializer):
   
    item_name = serializers.CharField(source="itemId.item_name" , read_only=True)
    item_price = serializers.CharField(source="itemId.item_price" , read_only=True)
    totalPrice = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'itemId', 'item_name',      
            'item_price', 'quantity', 'totalPrice'
        ]

    def get_totalPrice(self, obj):
        return obj.price * obj.quantity

    def create(self, validated_data):
        order = validated_data.get("order")
        item = validated_data.get("itemId")
        quantity = validated_data.get("quantity", 1)

       
        existing_item = OrderItem.objects.filter(order=order, itemId=item).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            order.update_totals() 
            return existing_item


        order_item = super().create(validated_data)
        order.update_totals()  
        return order_item
    
    def update(self, instance, validated_data):
        qty = validated_data.get('quantity', instance.quantity)   
        
        if qty < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        instance.quantity = qty
        instance.save()
        if instance.order:
            instance.order.update_totals()
        return instance


class KOTItemSerializer(serializers.ModelSerializer):
    
    item_name = serializers.CharField(
        source="items.item_name",
        read_only=True
    )

    class Meta:
        model = KOTItem
        fields = [
            "item_name" ,"quantity" , "is_sent_kot"
        ]

class KOTSerializer(serializers.ModelSerializer):
    items = KOTItemSerializer(many=True , read_only=True)
    order_id = serializers.CharField(source="order")
    order_type = serializers.CharField(source="order.orderType")
    table = serializers.SerializerMethodField()
    notes = serializers.CharField(source="order.notes")
    kot_number = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%I:%M %p")
    time_since = serializers.SerializerMethodField()
    class Meta:
        model = KOT
        fields = [
            "id" , "kot_number" , "order_id" ,"order_type" , "table" ,"status" , "created_at" , "notes"  , "time_since" ,"items"
        ]
    
    def get_kot_number(self , obj):
        return f"KOT-{obj.kot_number}"
    
     
    def get_table(self, obj):
        if obj.order.tableID:
            return f"T{obj.order.tableID.table_number}"
        return ""

  

    def get_time_since(self, obj):
      delta = timezone.now() - obj.created_at
      return int(delta.total_seconds() / 60) 
    



class OrderSerializer(serializers.ModelSerializer):
    # kots = KOTSerializer(many=True , read_only=True)
    items_detail = OrderItemSerializer(many=True , required=False , source="items")
    waiterName = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id', 'orderType', 'tableID', 'waiterId', 'waiterName' ,  'status', 'created_at',"notes",
            'subtotal', 'tax', 'discount', 'grandTotal', 'person','items_detail'
        ]   
     
    def get_items_detail(self, obj):    
        return OrderItemSerializer(obj.items.all(), many=True).data
    
    def get_waiterName(self, obj):
     waiter = obj.waiterId
     if not waiter:
        return None

     return f"{waiter.first_name} {waiter.last_name}".strip()

class PaymentSerializer(serializers.ModelSerializer):
     order = OrderSerializer(read_only = True)
     order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all() , source="order" , write_only=True)
     class Meta:
         model = Payment
         fields = ['id' , 'order_id' , 'order'  , 'payment_method' , 'payment_status','transaction_id']




