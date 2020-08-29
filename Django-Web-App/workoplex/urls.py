"""workoplex URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from basic import views
from django.conf.urls import url
from rest_framework import routers
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


#Registering the routers for all the api views
router = routers.DefaultRouter()
router.register(r'products',views.ProductViewSet, basename='Product')
router.register(r'product_details', views.ProductDetailsViewSet)
router.register(r'supplier', views.SupplierViewSet)
router.register(r'supplier_details', views.SupplierDetailsViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'pincode', views.PincodeViewSet)
router.register(r'state', views.StateViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'supplier_type', views.SupplierTypeViewSet)
router.register(r'pricing', views.PricingViewSet)
router.register(r'product_images', views.ProductDetailsImagesViewSet)
router.register(r'cart', views.CartViewSet,)
router.register(r'cart_item', views.CartItemViewSet,)





urlpatterns = [
    path("admin/", admin.site.urls), #url of admin
    url(r"^$", views.IndexView.as_view(),name="index"), #index page of website
    url(r'^basic/', include("basic.urls")),
    url(r'^api/', include(router.urls)), # url for api
    #this url is used to provide user authentication while accessing the api
    #currently all users allowed to access the api
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("", include("django.contrib.auth.urls")),


]

#this helps add the path to the media and static files
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
