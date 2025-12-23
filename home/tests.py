class KOT(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="kots")
    kot_number = models.IntegerField()   # 1, 2, 3, ...
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KOT #{self.kot_number} for Order {self.order.id}"


class KOTItem(models.Model):
    kot = models.ForeignKey(KOT, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def item_name(self):
        return self.item.item_name

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"


def create(self, validated_data):
    order = validated_data.get("order")
    item = validated_data.get("itemId")
    quantity = validated_data.get("quantity", 1)

    # STEP A: create or update order item
    existing_item = OrderItem.objects.filter(order=order, itemId=item).first()

    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
        order_item = existing_item
    else:
        order_item = super().create(validated_data)

    # STEP B: Generate new KOT
    last_kot = order.kots.order_by("-kot_number").first()
    kot_number = 1 if last_kot is None else last_kot.kot_number + 1

    kot = KOT.objects.create(order=order, kot_number=kot_number)

    # STEP C: Add items to KOT
    KOTItem.objects.create(
        kot=kot,
        item=item,
        quantity=quantity   # IMPORTANT: only NEW quantity
    )

    # STEP D: Update totals
    order.update_totals()

    return order_item


class KOTItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = KOTItem
        fields = ["id", "item", "item_name", "quantity"]


class KOTSerializer(serializers.ModelSerializer):
    items = KOTItemSerializer(many=True, read_only=True)

    class Meta:
        model = KOT
        fields = ["id", "kot_number", "created_at", "items"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    kots = KOTSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'orderType', 'tableID', 'userId', 'status', 'created_at',
            'subtotal', 'tax', 'discount', 'grandTotal', 'person',
            'items', 'kots'
        ]



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    kots = KOTSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'orderType', 'tableID', 'userId', 'status', 'created_at',
            'subtotal', 'tax', 'discount', 'grandTotal', 'person',
            'items', 'kots'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        # Create items for the new order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # Update order main fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If "items" present → update/append items
        if items_data is not None:
            for item in items_data:
                OrderItem.objects.update_or_create(
                    order=instance,
                    item_id=item.get('item_id'),
                    defaults=item
                )

        return instance

class KitchenKOTStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            kot = KOT.objects.get(pk=pk)
        except KOT.DoesNotExist:
            return Response({"status": False, "message": "KOT not found"}, status=404)

        status_value = request.data.get("status")
        if status_value not in ["PENDING", "COOKING", "READY"]:
            return Response({"status": False, "message": "Invalid status"}, status=400)

        kot.status = status_value
        kot.save()

        return Response({
            "status": True,
            "message": f"KOT marked {status_value}"
        })
