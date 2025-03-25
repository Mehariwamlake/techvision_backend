
from rest_framework import  viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import  PurchaseSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import Purchase





class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete_purchase(self, request, pk=None):
        """Complete the purchase and associate courses with the user"""
        purchase = self.get_object()
        purchase.associate_courses_with_user()
        return Response({"message": "Purchase completed and courses are now available."}, status=200)
