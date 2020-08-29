from django import forms
from basic.models import CustomUser,Customer,CustomerDetails, Supplier,SupplierDetails, Product


#form to register the user
class UserForm(forms.ModelForm):
    password=forms.CharField(widget= forms.PasswordInput())

    class Meta:
        model=CustomUser
        fields=['first_name', 'last_name', 'email','password']

#form to register as customer
class CustomerForm(forms.ModelForm):

    class Meta:
        model=Customer
        fields=['mobile_1', 'mobile_2',]

#form to register cutomer details
class CustomerDetailsForm(forms.ModelForm):

    class Meta:
        model=CustomerDetails
        fields=['gender','age','address_1','address_2', 'city', 'state', 'pincode']

#form to register suppliers
class SupplierForm(forms.ModelForm):

    class Meta:
        model=Supplier
        fields=['first_name', 'last_name', 'mobile_1', 'mobile_2','email','supplier_type']

#form to register supplier details
class SupplierDetailsForm(forms.ModelForm):

    class Meta:
        model=SupplierDetails
        fields=['opening_time', 'closing_time','address_1','address_2', 'city', 'state', 'pincode']
