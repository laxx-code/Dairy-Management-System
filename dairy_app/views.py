from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Sum, DecimalField
from decimal import Decimal
from .models import CustomerPayment

from .models import (
    Customer,
    BakeryProduct,
    DailySupply,
    Vendor,
    MilkRecord,
)
from .serializers import (
    CustomerSerializer,
    BakeryProductSerializer,
    DailySupplySerializer,
    VendorSerializer,
    MilkRecordSerializer,
    CustomerPaymentSerializer
)


# -----------------------
# Normal ViewSets
# -----------------------

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class BakeryProductViewSet(viewsets.ModelViewSet):
    queryset = BakeryProduct.objects.all().order_by("-created_at")
    serializer_class = BakeryProductSerializer


class DailySupplyViewSet(viewsets.ModelViewSet):
    serializer_class = DailySupplySerializer

    def get_queryset(self):
        queryset = DailySupply.objects.all().order_by("-date")
        supply_type = self.request.query_params.get("type")
        date = self.request.query_params.get("date")

        if supply_type:
            queryset = queryset.filter(supply_type=supply_type)
        if date:
            queryset = queryset.filter(date=date)

        return queryset


class MilkRecordViewSet(viewsets.ModelViewSet):
    queryset = MilkRecord.objects.all().order_by("-date_time")
    serializer_class = MilkRecordSerializer


# -----------------------
# Billing ViewSet
# -----------------------


class BillingViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def monthly(self, request):

        customer_id = request.query_params.get("customer")
        month_param = request.query_params.get("month")

        if not customer_id or not month_param:
            return Response({"error": "Missing parameters"}, status=400)

        year, month = month_param.split("-")
        year = int(year)
        month = int(month)

        supplies = DailySupply.objects.filter(
            customer_id=customer_id,
            date__year=year,
            date__month=month
        )

        total_amount = Decimal("0")
        transactions = []

        for s in supplies:

            milk_qty = Decimal(str(s.milk_quantity or 0))
            bakery_qty = Decimal(str(s.bakery_quantity or 0))
            price = Decimal(str(s.price or 0))

            amount = (milk_qty * price) + (bakery_qty * price)
            total_amount += amount

            transactions.append({
                "date": s.date,
                "product": s.supply_type,
                "quantity": float(milk_qty + bakery_qty),
                "amount": float(amount),
            })

        # Payments
        payments = CustomerPayment.objects.filter(
            customer_id=customer_id,
            payment_date__year=year,
            payment_date__month=month
        )

        paid = payments.aggregate(total=Sum("amount"))["total"] or 0
        paid_amount = Decimal(str(paid))

        balance = total_amount - paid_amount

        return Response({
            "total_amount": float(total_amount),
            "paid_amount": float(paid_amount),
            "balance": float(balance),
            "transactions": transactions
        })
    

class CustomerPaymentViewSet(viewsets.ModelViewSet):
    queryset = CustomerPayment.objects.all()
    serializer_class = CustomerPaymentSerializer