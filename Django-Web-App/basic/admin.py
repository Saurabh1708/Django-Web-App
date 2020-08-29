from django.contrib import admin
from basic.models import Supplier,Cart, Customer,CustomUser,CustomerDetails,SupplierDetails,Product,ProductDetails,Booking, ProductListingLog,Country,State,City,Pincode, ProductDetailsImages, Session, Post, CartItem

# Registering all models here.


admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(CustomerDetails)

admin.site.register(SupplierDetails)
admin.site.register(Product)
admin.site.register(ProductDetails)
admin.site.register(Booking)
admin.site.register(ProductListingLog)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Pincode)
admin.site.register(ProductDetailsImages)
admin.site.register(Session)
admin.site.register(Post)
admin.site.register(Cart)
admin.site.register(CartItem)


from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


#form is used to add a user in django admin
class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """

    #Takes in password twice to confirm
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


    #method to check if the passwords are same
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password', 'first_name', 'last_name', 'is_active',
            'is_staff'
        )

    def clean_password(self):
# Password can't be changed in the admin
        return self.initial["password"]


class CustomUserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()



admin.site.register(CustomUser, CustomUserAdmin)
