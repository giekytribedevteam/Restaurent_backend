from rest_framework import serializers
from django.utils import timezone
from .models import User ,  Floorname , Table , Menucategroy , MenuItem , Order , OrderItem , Payment , KOT , KOTItem
from decimal import Decimal 


class   TableSerializer(serializers.ModelSerializer): 
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

    
        last_kot = order.kots.order_by("-kot_number").first()
        kot_number = 1 if last_kot is None else last_kot.kot_number + 1

        kot = KOT.objects.create(order=order, kot_number=kot_number)


        KOTItem.objects.create(
        kot=kot,
        items=item,
        quantity=quantity   
        )

        order_item = super().create(validated_data)
        order.update_totals()  
        return order_item
    
    def update(self, instance, validated_data):
        print("=-=--=-" , validated_data)
        instance.quantity = validated_data.get('quantity', instance.quantity)   
        instance.save()
        if instance.order:
            instance.order.update_totals()

        return instance

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True , required=False)
    # kots = KOTSerializer(many=True , read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'orderType', 'tableID', 'userId', 'status', 'created_at',
            'subtotal', 'tax', 'discount', 'grandTotal', 'person' ,'items'
        ]      
   
    # def to_representation(self, instance):
    #     instance.update_totals()
        

class KOTItemSerializer(serializers.ModelSerializer):
    
    item_name = serializers.CharField(
        source="items.item_name",
        read_only=True
    )

    class Meta:
        model = KOTItem
        fields = [
            "id" , "items" ,"item_name" ,"quantity"
        ]

class KOTSerializer(serializers.ModelSerializer):
    items = KOTItemSerializer(many=True , read_only=True)
    order_type = serializers.CharField(source="order.orderType")
    table = serializers.CharField(source="order.tableID.table_number")
    time_since = serializers.SerializerMethodField()
    class Meta:
        model = KOT
        fields = [
            "id" , "kot_number" , "order_type" , "table" , "status" , "created_at" , "time_since","items"
        ]

    def get_time_since(self, obj):
      delta = timezone.now() - obj.created_at
      return int(delta.total_seconds() / 60) 

class PaymentSerializer(serializers.ModelSerializer):
     order = OrderSerializer(read_only = True)
     order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all() , source="order" , write_only=True)
     class Meta:
         model = Payment
         fields = ['id' , 'order_id' , 'order'  , 'payment_method' , 'payment_status','transaction_id']




