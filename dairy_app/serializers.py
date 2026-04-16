from rest_framework import serializers
from .models import DailySupply, BakeryProduct, Customer,MilkRecord,Vendor

class BakeryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BakeryProduct
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class DailySupplySerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(source="customer.name", read_only=True)

    product_name = serializers.SerializerMethodField()

    quantity = serializers.SerializerMethodField()

    rate = serializers.SerializerMethodField()

    total_amount = serializers.SerializerMethodField()


    class Meta:
        model = DailySupply
        fields = [
            "id",
            "supply_type",
            "customer",
            "customer_name",
            "bakery_product",
            "product_name",
            "milk_quantity",
            "bakery_quantity",
            "price",
            "date",
            "quantity",
            "rate",
            "total_amount",
        ]


    def get_product_name(self, obj):

        if obj.supply_type == "milk":
            return "Milk"

        if obj.bakery_product:
            return obj.bakery_product.name

        return "-"


    def get_quantity(self, obj):

        if obj.supply_type == "milk":
            return obj.milk_quantity

        return obj.bakery_quantity


    def get_rate(self, obj):

        return obj.price


    def get_total_amount(self, obj):

        quantity = self.get_quantity(obj)

        if quantity and obj.price:
            return float(quantity) * float(obj.price)

        return 0


# ✅ Add this missing serializer
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class MilkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkRecord
        fields = '__all__'

from .models import CustomerPayment
class CustomerPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerPayment
        fields = "__all__"