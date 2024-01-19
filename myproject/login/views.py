from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from .models import CustomUser,BlacklistedToken
# Create your views here.
from rest_framework import status,generics,serializers,permissions
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import BlacklistedTokenSerializer,LogoutSerializers,RegisterSerializer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, decorators
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout
# @csrf_exempt
#done register

class RegisterView(generics.CreateAPIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # queryset = CustomUser.objects.all()
    # permission_classes = (AllowAny,)
    # serializer_class = RegisterSerializer

# auth_token
# class UserLogin(generics.CreateAPIView):
    # def post(self,request):
    #     if request.method == 'POST':
    #         username = request.data.get('username')
    #         password = request.data.get('password')
    #         user = authenticate(username=username, password=password)

    #     if '@' in username:
    #         try:
    #             user = CustomUser.objects.get(email=username)
    #         except ObjectDoesNotExist:
    #             pass

    #     if user:
    #         token, _ = Token.objects.get_or_create(user=user)
    #         return Response({'token': token.key}, status=status.HTTP_200_OK)

    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

#jwt token done
class UserLogin(APIView):
    def post(self,req):
        username = req.data.get('username')
        password = req.data.get('password')
        user = authenticate(username = username, password = password)
        # if user is not None:
        refresh = RefreshToken.for_user(user)
        Token.objects.get_or_create(user=user)
        # return JsonResponse({'refresh':str(username),'access':str(refresh.access_token)})
        return JsonResponse({'refresh':str(refresh),'access':str(refresh.access_token)})
        # return Response(user, status=status.HTTP_400_BAD_REQUEST)
    

#todo logout jwt token
class LogoutAPI(generics.GenericAPIView):
    serializer_class = LogoutSerializers

    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    
#todo refresh token
class TokenRefreshView(APIView):
    def post(self,request):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        try:
            access_token = str(token.access_token)
            refresh_token = str(token)
            return Response({'access': access_token, 'refresh': refresh_token})
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
        
        
class ViewHome(View):
    def get(self,request):
        return render(request,'account/base.html')