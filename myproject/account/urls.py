from django.urls import path
from .views import RegisterView, UserLogin, ViewProduct,TokenRefreshView,LogoutAPI,ViewHome

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('product/<int:product_id>', ViewProduct.as_view(), name='product'),
    path('product/', ViewProduct.as_view(), name='product'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh-token'),
    path('viewhome/',ViewHome.as_view(),name='viewhome')
]