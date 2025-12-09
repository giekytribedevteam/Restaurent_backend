
class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "OrderItem list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "OrderItem details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": True,
            "message": "OrderItem created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": True,
            "message": "OrderItem updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "OrderItem deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)
    


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
    

    {
    "non_field_errors": [
        "Invalid data. Expected a dictionary, but got list."
    ]
}
    




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
    