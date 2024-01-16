from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from .models import CustomUser,Product,BlacklistedToken
# Create your views here.
from rest_framework import status,generics,serializers,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, ProductSerializer,BlacklistedTokenSerializer,LogoutSerializers

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, decorators
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
#done register
class RegisterView(generics.CreateAPIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
#auth_token
# @api_view(['POST'])
# class UserLogin(generics.CreateAPIView):
#     def post(self,request):
#         if request.method == 'POST':
#             username = request.data.get('username')
#             password = request.data.get('password')
#             user = authenticate(username=username, password=password)

#         if '@' in username:
#             try:
#                 user = CustomUser.objects.get(email=username)
#             except ObjectDoesNotExist:
#                 pass

#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)

#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

#jwt token done
class UserLogin(APIView):
    def post(self,req):
        username = req.data.get('username')
        password = req.data.get('password')
        user = authenticate(username = username, password = password)
        refresh = RefreshToken.for_user(user)
        Token.objects.get_or_create(user=user)
        return JsonResponse({'refresh':str(refresh),'access':str(refresh.access_token)})
    

#done logout auth token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        refresh_token = request.data.get('refresh_token')
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#todo logout jwt token
class LogoutAPI(generics.GenericAPIView):
    serializer_class = LogoutSerializers

    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    

#done viewproduct
class ViewProduct(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        queryset = Product.objects.all()
        serializers = ProductSerializer(queryset,many=True)
        return Response(serializers.data)
    

#done push product
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_product(req):
    mydata = ProductSerializer(data=req.data)
    if not mydata.is_valid():
        return Response('sai du lieu', status=status.HTTP_400_BAD_REQUEST)
    id = mydata.data['id']
    name = mydata.data['name']
    describe = mydata.data['describe']
    pr = Product.objects.create(id=id,name=name,describe=describe)
    return Response(data=pr.id,status=status.HTTP_201_CREATED)


#todo refresh token
class TokenRefreshView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        try:
            access_token = str(token.access_token)
            refresh_token = str(token)
            return Response({'access': access_token, 'refresh': refresh_token})
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)