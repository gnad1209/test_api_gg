from django.urls import path
from .views import ViewProduct
    
urlpatterns = [
    path('<int:product_id>/', ViewProduct.as_view(), name='product-post'),
    path('', ViewProduct.as_view(), name='product'),
]    
