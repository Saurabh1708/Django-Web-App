from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from basic.models import Supplier, Customer,CustomerDetails,SupplierDetails, CustomUser
from basic.forms import UserForm, CustomerForm, SupplierForm, CustomerDetailsForm,SupplierDetailsForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from rest_framework import viewsets, filters
from .serializers import ProductSerializer, ProductDetailsSerializer,ProductDetailsImagesSerializer,SupplierTypeSerializer, SupplierSerializer , SupplierDetailsSerializer, CitySerializer, PincodeSerializer, StateSerializer, CountrySerializer, PricingSerializer, CartSerializer, CartItemSerializer
from .models import Product, ProductDetails, City, Pincode, State, Country, Supplier, SupplierType, Customer, SupplierDetails,CustomerDetails, Pricing, ProductDetailsImages,Cart, CartItem
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
'''
superuser
username-saurabh@gmail.com
pwd- 123
User:
username- ranjit@workoplex.com
pwd-Workoplex@123
'''


#template view to render home page
class BasicIndexView(TemplateView):
    template_name="basic/basic_index.html"
    context_object_name="basic_index"

#method to register user
def UserRegistrationView(request):

    #registered value is added to the context so that we know whether the user is registered or not
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)

        #checking if form data is valid
        if user_form.is_valid():
            #saving the user form but not adding changes to the database
            user=user_form.save(commit=False)
            #adding password to the user
            user.set_password(user.password)
            #saving user's data to the database
            user.save()

            registered=True
        else:
            print(user_form.errors)
    else:
        #rendering empty form
        user_form=UserForm()

    context={"user_form": user_form, "registered": registered}
    return render(request, "basic/basic_index.html", context)


#Method to create Customer Registration
def CustomerRegistrationView(request):

    if request.method=="POST":
        customer_form=CustomerForm(data=request.POST)
        customer_details_form=CustomerDetailsForm(data=request.POST)
        #checking if the customer data is valid or not
        if customer_form.is_valid() and customer_details_form.is_valid()  :

            customer=customer_form.save(commit=False)
            customer.user=request.user
            customer.save()
            customer_details_form=customer_details_form.save(commit=False)
            customer_details_form.customer_id=customer
            customer_details_form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print( customer_details_form.errors, customer_form.errors)

    else:
        customer_details_form=CustomerDetailsForm()
        customer_form=CustomerForm()

    context={'customer_form': customer_form,'customer_details_form':customer_details_form}
    return render(request,'basic/customer_registration_form.html',context)


def SupplierRegistrationView(request):
    supplier_registration=False
    if request.method=="POST":
        supplier_form=SupplierForm(data=request.POST)
        supplier_details_form=SupplierDetailsForm(data=request.POST)

        if supplier_form.is_valid() and supplier_details_form.is_valid():
            s=supplier_form.save()
            supplier_details_form.save(commit=False)
            supplier_details_form.supplier_id=s.id
            print(supplier_details_form.supplier_id)
            supplier_details_form.save()
            supplier_registration=True
        else:
            print("error found")

    else:
        supplier_details_form=SupplierDetailsForm()
        supplier_form=SupplierForm()
    context={'supplier_form': supplier_form,'supplier_registration': supplier_registration,'supplier_details_form':supplier_details_form}
    return render(request,'basic/supplier_registration_form.html',context)


#creates a Template View for the home or the index page
class IndexView(TemplateView):
    template_name="basic/index.html"
    context_object_name='index'

#creates the customer list view
class CustomerListView(ListView):
    context_object_name='customer_list'
    template_name="basic/customer_list.html"
    model=Customer

    def get_queryset(self):
        return Customer.objects.filter(user__is_staff=False)


#creates the customer Details view
class CustomerInfo(DetailView):
    model=Customer
    context_object_name="customer"
    template_name="basic/customer_details.html"

#creates the customer Details table's Details view
class CustomerDetailsInfo(DetailView):
    model=CustomerDetails
    context_object_name='customer_details'
    template_name="basic/customer_details.html"

#ViewSet for the Supplier api
class SupplierViewSet(viewsets.ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializer

#ViewSet for the Supplier Details api
class SupplierDetailsViewSet(viewsets.ModelViewSet):
    queryset=SupplierDetails.objects.all()
    serializer_class=SupplierDetailsSerializer

#ViewSet for the products api
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    filter_backends = [filters.SearchFilter]
    #Provides search filter to search with product_name, supplier's first and last name, supplier type, pincode, state and city
    search_fields = ['product_name',
                    'productdetails__supplier_id__first_name',
                    'productdetails__supplier_id__last_name',
                    'productdetails__supplier_id__supplier_type__supplier_type',
                    'productdetails__supplier_id__supplierdetails__city__name',
                    'productdetails__supplier_id__supplierdetails__state__name',
                    'productdetails__supplier_id__supplierdetails__pincode__pincode'
                    ]


    def get_queryset(self):
        #taking the values sent by the api specified in the data received from ajax
        pincode=self.request.query_params.get('pincodes', None)
        city=self.request.query_params.get('city', None)
        state=self.request.query_params.get('state', None)
        supplier_type=self.request.query_params.get('supplier_type', None)
        supplier=self.request.query_params.get('supplier', None)
        pricing=self.request.query_params.get('pricing', None)
        #all objects of Product Table
        result=Product.objects.all()
        # all objects of Supplier table
        qs=SupplierDetails.objects.all()
        if pincode:
            #getting Pincode object with matching pincode from Pincode Table
            queryset=Pincode.objects.filter(pk=pincode)
            #getting supplier details object with the matching pincode.Using slicing to get only 1 object from queryset
            queryset=qs.filter(pincode=queryset[0])
            #checking if there is an empty supplierdetail corresponding to the pincode
            if not queryset:
                #if empty returning empty queryset
                return Product.objects.none()
            #taking first object from queryset
            obj=queryset[0]
            result=Product.objects.filter(productdetails__supplier_id=obj.supplier_id)
        elif city:
            #getting the city object with matching city name from City table
            queryset=City.objects.get(pk=city)
            queryset=qs.filter(city=queryset)
            if not queryset:
                return Product.objects.none()
            #filtering Product table with the objects having matching supplier_id
            obj=queryset[0]
            result=Product.objects.filter(productdetails__supplier_id=obj.supplier_id)

        elif state:
            #getting state object with the required state
            queryset=State.objects.filter(pk=state)
            #since it is a queryset we have to use the first object of the queryset
            queryset=qs.filter(state=queryset[0])
            #if queryset is empty or there is not matching state
            if not queryset:
                return Product.objects.none()
            #filtering Product table with the objects having matching supplier_id
            obj=queryset[0]
            result=Product.objects.filter(productdetails__supplier_id=obj.supplier_id)

        #checking if a supplier type is provided or not
        if supplier_type:
            #Getting Supplier Type objects which has the required supplier type
            queryset=SupplierType.objects.get(pk=supplier_type)
            #getting the Suppliers which have the above supplier type
            supp=Supplier.objects.filter(supplier_type=queryset)
            #if there are no suppliers with the given supplier type
            if not supp:
                #returning No products as there no suppliers for the corresponding supplier type
                return Product.objects.none()
            #result is the filtered queryset of Products with the given supplier type
            result=result.filter(productdetails__supplier_id=supp[0])

        #checking if the supplier is provided or not
        if supplier:
            #getting the first and last name of the supplier
            first_name, last_name=supplier.split()
            #finding suppliers with the above first and last name
            supplier=Supplier.objects.get(first_name=first_name, last_name=last_name)
            #filtering Products with the above matching supplier queryset
            result=result.filter(productdetails__supplier_id=supplier)

        #checking if the pricing filter value is provided
        if pricing:
            #splitting the price range between low and high
            low,high=pricing.split("-")
            #converting string data into float data
            low=float(low)
            high=float(high)
            #Getting those objects from Price Table which have prices between low and high value
            prices=Pricing.objects.filter(total_price__gte=low, total_price__lte=high)
            #if there are no objects with the matching price filter
            if not prices:
                #returning Empty queryset
                return result.none()
            #filtering Product queryset corresponding to  the prices
            result=result.filter(pk=prices[0].product_details.product_id.id)

        #returning the final queryset after applying all the filters
        return result

#Creating viewset for ProductDetails Images
class ProductDetailsImagesViewSet(viewsets.ModelViewSet):
    queryset=ProductDetailsImages.objects.all()
    serializer_class=ProductDetailsImagesSerializer

#Creating viewset for ProductDetails
class ProductDetailsViewSet(viewsets.ModelViewSet):
    queryset=ProductDetails.objects.all()
    serializer_class=ProductDetailsSerializer

#template for displaying the list of products
class ProductListingPage(TemplateView):
    template_name="basic/products.html"

#template for displaying the products details
class ProductDetailsPage(TemplateView):
    template_name="basic/product_details.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated :
            return {}

        customer=Customer.objects.get(user=self.request.user)
        context['cart']=Cart.objects.get(customer_id=customer)
        return context

#template for displaying the Supplier list
class SupplierListPage(TemplateView):
    template_name="basic/supplier_list.html"

#template for displaying the Supplier details
class SupplierDetailsPage(TemplateView):
    template_name="basic/supplier_detail.html"

#Creating viewset for Supplier Type
class SupplierTypeViewSet(viewsets.ModelViewSet):
    queryset=SupplierType.objects.all()
    serializer_class=SupplierTypeSerializer

#Creating viewset for Pincode api
class PincodeViewSet(viewsets.ModelViewSet):
    queryset=Pincode.objects.all()
    serializer_class=PincodeSerializer

#Creating viewset for City api
class CityViewSet(viewsets.ModelViewSet):
    queryset=City.objects.all()
    serializer_class=CitySerializer

#Creating viewset for State api
class StateViewSet(viewsets.ModelViewSet):
    queryset=State.objects.all()
    serializer_class=StateSerializer

#Creating viewset for Country api
class CountryViewSet(viewsets.ModelViewSet):
    queryset=Country.objects.all()
    serializer_class=CountrySerializer

#Creating viewset for Pricing api
class PricingViewSet(viewsets.ModelViewSet):
    queryset=Pricing.objects.all()
    serializer_class=PricingSerializer

#creating viewset for cart api
class CartViewSet(viewsets.ModelViewSet):
    serializer_class=CartSerializer
    queryset=Cart.objects.all()

#creating Booking View set
class CartItemViewSet(viewsets.ModelViewSet):
    queryset=CartItem.objects.all()
    serializer_class=CartItemSerializer

class CartPage(TemplateView):
    template_name="basic/cart.html"

    #context is set to get cart value for customer
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context = {}
            return context
        customer=Customer.objects.get(user=self.request.user)
        context['cart']=Cart.objects.get(customer_id=customer)
        return context
