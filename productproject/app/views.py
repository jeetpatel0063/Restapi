from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view (["GET"])
def Apioverview(req):
    api_urls={
        "all_products":"/AllProductview",
        "add_product":"/AddProduct",
        "update_product":"/UpdateProduct/update/pk",
        "delete_product":"/DeleteProduct/delete/pk",
        "searh by category":"/searchbycategory/?category=category_name"
    }
    return Response(api_urls)


class AllProductview(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UpdateProduct(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    partial = True

class DeleteProduct(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

from rest_framework import status

# @api_view(["GET"])
# def searchbycategory(req):
#     if req.query_params:
#         items=Product.objects.filter(**req.query_params.dict())
#         serializers=ProductSerializer(items,many=True)
#         return Response(serializers.data)

#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
from django.db.models import Q 

@api_view(["GET"])
def searchbycategory(req):
    query_params=req.query_params
    filter=Q()

    if "category" in query_params:
        filter &= Q(category=query_params["category"])

    min_price=query_params.get("min_price")
    max_price=query_params.get("max_price")

    if min_price and min_price.isdigit():
        filter &= Q(price__gte=min_price)

    if max_price and max_price.isdigit():
        filter &= Q(price__lte=max_price)

    items=Product.objects.filter(filters)

    if not items.exists():
        return Response({"message":"No products found"}, status=status.HTTP_404_NOT_FOUND)

    serializers=ProductSerializer(items, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
