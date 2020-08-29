from django.conf.urls import url, include
from rest_framework import routers
from basic import views

app_name='basic'




urlpatterns=[
    #url for customer listing page
    url(r'^customers/$', views.CustomerListView.as_view(), name='customerlist'),
    #url for Supplier listing page
    url(r'^supplier/$', views.SupplierListPage.as_view(), name='supplierlist'),
    #url for customer Details page
    url(r'^customers/(?P<pk>\d+)/$', views.CustomerInfo.as_view(), name="customers"),
    #url for supplier Details page
    url(r'^supplier/(?P<pk>\d+)/$',views.SupplierDetailsPage.as_view(), name="supplier"),
    #url for index page
    url(r'^$', views.UserRegistrationView, name='register'),
    #url for supplier Registation
    url(r"^supplier_registration/$", views.SupplierRegistrationView, name='supplier_registration'),
    #url for customer Registation
    url(r'^customer_registration/$', views.CustomerRegistrationView, name="customer_registration"),
    #url for products listing page
    url(r'^products/$', views.ProductListingPage.as_view(), name="products"),
    #url for products Details page
    url(r'^products/(?P<pk>\d+)/$', views.ProductDetailsPage.as_view(), name="product_details"),
    #url for products Details page
    url(r'^cart/$', views.CartPage.as_view(), name="cart"),




]
