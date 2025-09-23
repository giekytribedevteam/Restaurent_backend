from rest_framework import serializers
from .models import User ,  Floorname , Table , Menucategroy , MenuItem , Order , OrderItem , Payment



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




