
from django.urls import path, include
from . import views
from .views import *

app_name = 'ecomWebApp'

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    # path('signup/', views.signup, name="signup"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/',MyLoginView.as_view() , name="login"),
    path('logout/',MyLogoutView.as_view() , name="logout"),
    path('product-details/<slug>', ProductDetailView.as_view(), name="productDetails"),
    path('add-cart/' ,AddToCartView.as_view(), name="addTocart"),
    path('cart/' , CartListView.as_view(), name="cart"),
    path('remove-cart/<int:pk>' , RemoveCartItemsView.as_view(), name="removeCartItemsView"),



]
