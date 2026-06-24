from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Case, When, Value, IntegerField, Q

from .models import Product
from .serializers import ProductSerializer


# GET /api/products/
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# GET /api/products/<id>/
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


# GET /api/products/search?q=smartphone
class SearchView(APIView):

    def get(self, request):
        q = request.GET.get("q")

        if not q:
            return Response(
                {"error": "Search query is required"},
                status=400
            )

        products = Product.objects.annotate(
            priority=Case(
                When(category__icontains=q, then=Value(1)),
                When(tags__icontains=q, then=Value(2)),
                When(description__icontains=q, then=Value(3)),
                default=Value(4),
                output_field=IntegerField()
            )
        ).filter(
            Q(category__icontains=q) |
            Q(tags__icontains=q) |
            Q(description__icontains=q)
        ).order_by("priority")

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)