from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', views.ProductView)
router.register('categories', views.CategoryView)

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("menu/", views.menu, name="menu"),
    path("buy/", views.buy, name="buy"),
    path("orderConfirmation/", views.orderConfirmation, name="orderConfirmation"),
    path("saveCartItem/", views.saveCartItem, name="saveCartItem"),
    path("removeCartItem/", views.removeCartItem, name="removeCartItem"),
    path("isUsernameAvailable/", views.isUsernameAvailable, name="isUsernameAvailable"),
    path("", include(router.urls))
]