from rest_framework import serializers
from .models import User ,  Floorname , Table , Menucategroy , MenuItem , Order , OrderItem , Payment
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
   
    itemName = serializers.CharField(source="itemId.item_name" , read_only=True)
    price = serializers.CharField(source="itemId.item_price" , read_only=True)
    totalPrice = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'itemId', 'itemName', 'created_at',      
            'price', 'quantity', 'totalPrice'
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
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        if instance.order:
            instance.order.update_totals()

        return instance
    


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'orderType', 'tableID', 'userId', 'status', 'created_at',
            'subtotal', 'tax', 'discount', 'grandTotal', 'person' ,  'items'
        ]            



class PaymentSerializer(serializers.ModelSerializer):
     order = OrderSerializer(read_only = True)
     order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all() , source="order" , write_only=True)
     class Meta:
         model = Payment
         fields = ['id' , 'order_id' , 'order'  , 'payment_method' , 'payment_status','transaction_id']



# class OrderItemSerializer(serializers.ModelSerializer):
#       item_name = serializers.CharField(source="menu_itemID.item_name" , read_only=True)
#       class Meta:
#            model = OrderItem
#            fields = ['id' , 'menu_item' ,'item_name' , 'orderId' , 'quantity' , 'order_price']  


# class OderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     class Meta:
#         model = Order
#         fields = ['id' , 'userId' , 'table_orderID' ,  'items',  'order_type' , 'status' , 'discount'  , 'tax' , 'total_amount']
#         extra_kwargs = {
#             'table_order': {'required': False}
#         }

#     def create(self, validated_data):
        
#         items_data = validated_data.pop("items" , [])
#         user = self.context['request'].user
#         order = Order.objects.create( userId=user ,  **validated_data) 

#         total = 0 
#         for items in items_data:
#           menu_item = items['menu_item']
#           quanty = items['quantity']
#           price = menu_item.item_price

#           OrderItem.objects.create(
#             orderId = order,  
#             menu_item =  menu_item,
#             quantity = quanty, 
#             order_price = price
#          ) 
          
#           total += quanty * price  
          
#         order.total_amount = total 
#         order.save()
#         return order 
         

#     def update(self, instance, validated_data):
       
#         items_data = validated_data.pop('items', None)

  
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

        
#         if items_data is not None:
     
#             instance.items.all().delete()

         
#             total = 0
#             for item in items_data:
#                 menu_item = item['menu_item']
#                 quantity = item['quantity']
#                 price = menu_item.item_price

#                 OrderItem.objects.create(
#                     order=instance,
#                     menu_item=menu_item,
#                     quantity=quantity,
#                     order_price=price
#                 )

#                 total += quantity * price

          
#             instance.total_amount = total

#         instance.save()
#         return instance
    


