from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from .models import Product
# Create your views here.
from rest_framework import status,generics,serializers,permissions
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import ProductSerializer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, decorators
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout
# Create your views here.
class ViewProduct(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        queryset = Product.objects.all()
        serializers = ProductSerializer(queryset,many=True)
        return Response(serializers.data)
    
    # permission_classes = (IsAuthenticated,)
    # def get(self,request):
    #     queryset = Product.objects.all()
    #     serializers = ProductSerializer(queryset,many=True)
    #     return Response(serializers.data)

    permission_classes = (IsAuthenticated,)
    def post(self,request):
        mydata = ProductSerializer(data=request.data)
        if not mydata.is_valid():
            return Response('sai du lieu', status=status.HTTP_400_BAD_REQUEST)
        id = mydata.data['id']
        name = mydata.data['name']
        describe = mydata.data['describe']
        pr = Product.objects.create(id=id,name=name,describe=describe)
        return Response(data=pr.id,status=status.HTTP_201_CREATED)
    
    permission_classes = (IsAuthenticated,)
    def put(self,request,product_id):
        product = Product.objects.get(pk=product_id)
        serializer = ProductSerializer(product,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    permission_classes = (IsAuthenticated,)
    def delete(self,request,product_id):
        product = Product.objects.get(pk=product_id)
        if product is None:
            return Response('sản phẩm ko tồn tại', status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response('xóa thành công', status=status.HTTP_204_NO_CONTENT)
