from django.urls import path
from .views import RegisterView, UserLogin, user_logout, ViewProduct,post_product,TokenRefreshView,LogoutAPI

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('product/', user_logout, name='product'),
    path('product-post/', post_product, name='product-post'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh-token')
]