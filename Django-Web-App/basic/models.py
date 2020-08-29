from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django import forms
from django.contrib.admin import widgets
from django.utils import timezone
from django.urls import reverse
import decimal
from django.utils.translation import gettext_lazy as _

#Creating custom user manager for registering user with the help of email and password

class UserManager(BaseUserManager):

    #method to create user
    def create_user(
            self, email,first_name, last_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        #hashing password
        user.set_password(password)

        if commit:
            user.save(using=self._db)
        return user

    #method to create superuser
    def create_superuser(self,email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Creating custom user model to register users using email and password
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=('email address'), unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(('first name'), max_length=50, blank=True)
    last_name = models.CharField(('last name'), max_length=50, blank=True)


    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        ('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    #email and password fields are already made required
    REQUIRED_FIELDS = ['first_name', 'last_name' ]


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

#Creating choices for Channels
class Channels(models.TextChoices):
    # first value is one that enters the database while the second value is it's actual value
    mobile= 'M', "Mobile"
    web='W', 'Web'
    android='A', 'Android'
    ios='iOS','iOS'

# Creating choices for Genders
class GenderChoices(models.TextChoices):
    male='Male', 'Male'
    female='Female', 'Female'


# Creating Country Table
class Country(models.Model):
    name=models.CharField(max_length=256, primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Country"

    def __str__(self):
        return self.name

# Creating State Table
class State(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=256,primary_key=True)
    #Foreign key to Country table
    country=models.ForeignKey(Country,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="State"

    def __str__(self):
        return self.name

# Creating City Table
class City(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    district=models.CharField(max_length=256)
    #Foreign key to State table
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    name=models.CharField(max_length=256, primary_key=True)

    class Meta:
        verbose_name_plural="City"

    def __str__(self):
        return self.name

# Creating Pincode Table
class Pincode(models.Model):
    pincode=models.PositiveIntegerField(primary_key=True)
    #Foreign key to City table
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Pincode"

    def __str__(self):
        return str(self.pincode)



# Creating Customer table

class Customer(models.Model):

    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mobile_1=models.CharField(max_length=256)
    mobile_2=models.CharField(max_length=256)
    mobile_3=models.CharField(max_length=256)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural='Customers'

    def __str__(self):
        return self.user.first_name+self.user.last_name

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        cart=Cart(customer_id=self)
        cart.save()
        print(cart)


# Creating customer details table

class CustomerDetails(models.Model):

    id=models.AutoField(primary_key=True)
    #adding foreign key constraint with customer table
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE,)
    gender=models.CharField(max_length=20,choices=GenderChoices.choices)
    age=models.PositiveIntegerField()
    address_1=models.CharField(max_length=256)
    address_2=models.CharField(max_length=256)
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    state=models.ForeignKey(State,  on_delete=models.CASCADE)
    pincode=models.ForeignKey(Pincode, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #adding foreign key constraint with Custom User table
    #created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    creation_channel=models.CharField(choices=Channels.choices, max_length=20)
    customer_ip=models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name_plural='Customer Details'

    def __str__(self):
        return self.customer_id.user.first_name+self.customer_id.user.last_name

# Creating Supplier Type Table

class SupplierType(models.Model):
    supplier_type=models.CharField(max_length=50, primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural='Supplier Type'

    def __str__(self):
        return self.supplier_type

#Creating Supplier Table

class Supplier(models.Model):
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=256)
    last_name=models.CharField(max_length=256)
    mobile_1=models.PositiveIntegerField()
    mobile_2=models.PositiveIntegerField()
    mobile_3=models.PositiveIntegerField(null=True)
    email=models.EmailField()
    supplier_type=models.ForeignKey(SupplierType, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    creation_channel=models.CharField(choices=Channels.choices, max_length=20)
    #ForeignKey attribute to be added later to the this field with the Users model
    created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE,)

    class Meta:
        verbose_name_plural='Supplier'

    def __str__(self):
        name=self.first_name+self.last_name
        return name


#Creating supplier Details
class SupplierDetails(models.Model):

    id=models.AutoField(primary_key=True)
    #adding foreign key constraint with Supplier Table
    supplier_id=models.ForeignKey(Supplier, on_delete=models.CASCADE)
    address_1=models.CharField(max_length=256)
    address_2=models.CharField(max_length=256)
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    state=models.ForeignKey(State,  on_delete=models.CASCADE)
    pincode=models.ForeignKey(Pincode, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    opening_time=models.TimeField()
    closing_time=models.TimeField()

    class Meta:
        verbose_name_plural="Supplier Details"

    def __str__(self):
        name=Supplier.objects.get(pk=self.supplier_id).first_name
        return name


#Creating Product Table
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=256)
    duration_type=models.DurationField()
    product_description=models.CharField(max_length=256)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    tagline=models.CharField(max_length=256)

    class Meta:
        verbose_name_plural="Product"

    def __str__(self):
        return self.product_name

#Creating Product Details Table
class ProductDetails(models.Model):
    id=models.AutoField(primary_key=True)
    #adding foreign key constraint with supplier table
    supplier_id=models.ForeignKey(Supplier, on_delete=models.CASCADE,)
    #adding foreign key constraint with product table
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE,)
    is_active=models.BooleanField(default=True)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    quantity=models.PositiveIntegerField()
    discount_id=models.DecimalField(decimal_places=2,max_digits=10)
    is_published_mobile=models.BooleanField(default=False)
    is_published_web=models.BooleanField(default=True)
    is_published_android=models.BooleanField(default=True)
    is_published_ios=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural='Product Details'

    def __str__(self):
        return str(self.product_id)

class Cart(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.OneToOneField(Customer, on_delete=models.CASCADE,)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    total_price=models.DecimalField(decimal_places=2,max_digits=10, default=0)

    class Meta:
        verbose_name_plural="Cart"

    def __str__(self):
        return self.customer_id.user.first_name +" "+ self.customer_id.user.last_name


    def get_cart_items(self):
        return CartItem.objects.filter(cart_id=self.id)


class CartItem(models.Model):
    id=models.AutoField(primary_key=True)
    product_details_id=models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #getting present object's price object
        p=Pricing.objects.get(product_details=self.product_details_id)
        #getting respective cart object
        obj=Cart.objects.get(id=self.cart_id.id)
        #getting queryset of cart item so that it's quantity can be modified
        qs=CartItem.objects.filter(product_details_id=self.product_details_id)

        #if that product does not exist in the cart then create a new object in the cart
        if not len(qs) :
            #calculating value of total price of cart after item is added
            obj.total_price+=(self.quantity)*(p.total_price)
            #saving total price of object
            obj.save()
            #saving the cart item
            super (CartItem, self).save(*args, **kwargs)


        #since the product was already present in the cart, we modify its quantity
        #also we modify the total cart value
        else:
            #since we changed the quantity of the product the total_price had to be changed
            obj.total_price+=(self.quantity-qs[0].quantity)*p.total_price
            #saving cart object of the user
            obj.save()
            #updating the quantity of the cart item object
            qs.update(quantity=self.quantity)


    #on removing an item from the cart, delete is called
    def delete(self,*args,**kwargs):
        print("delete")
        #getting the pricing object corresponding to the product
        p=Pricing.objects.get(product_details=self.product_details_id)
        #cart object with the corresponding cart id
        obj=Cart.objects.get(id=self.cart_id.id)
        #deleting the cart item object
        super(CartItem, self).delete()
        #modifying the total_price of the cart
        obj.total_price=obj.total_price-p.total_price*self.quantity
        #saving the cart object
        obj.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural='Cart Items'

# Creating choices for Booking
class BookingChoices(models.TextChoices):
    confirmed='C', 'Confirmed'
    pending='F', 'Failed'
    #other choices to be added later

#Creating Booking Table
class Booking(models.Model):
    id=models.AutoField(primary_key=True)
    #adding foreign key with ProductDetails
    product_details_id=models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE)
    #taking choices from BookingChoices class
    booking_stage=models.CharField(choices=BookingChoices.choices, max_length=10)
    booking_datetime=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Booking"

    def __str__(self):
        return str(self.id)



# Creating ProductDetailsId Table
class ProductDetailsImages(models.Model):
    id=models.AutoField(primary_key=True)
    #Foreign Key to Product Details table
    product_details_id=models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/', blank=True,)
    image_type=models.CharField(max_length=256)
    is_default_image=models.BooleanField('default image')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Product Details Id"

    def __str__(self):
        return self.product_details_id

    #this function takes the image_type from the image url and saves the object
    def save(self, *args, **kwargs):
        type=self.image.url
        print(type)
        #on splitting using "." the last entry in the list is the image extension
        type=type.split(".")[-1]
        self.image_type=type
        #saving ProductDetailsImage object
        super(ProductDetailsImages, self).save(*args, **kwargs)


# Creating listing Log table all the columns of product details. ENtry for all changes in the product details table.
class ProductListingLog(models.Model):
    id=models.AutoField(primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)
    #adding foreign key constraint with supplier table
    supplier_id=models.ForeignKey(Supplier, on_delete=models.CASCADE,)
    #adding foreign key constraint with product table
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE,)
    is_active=models.BooleanField(default=True)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    quantity=models.PositiveIntegerField()
    discount_id=models.DecimalField(decimal_places=2,max_digits=10)
    is_published_mobile=models.BooleanField(default=False)
    is_published_web=models.BooleanField(default=True)
    is_published_android=models.BooleanField(default=True)
    is_published_ios=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural="Listing Log"

    def __str__(self):
        return id


class Session(models.Model):
    id=models.AutoField(primary_key=True)
    cookie_id=models.CharField(max_length=256)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    duration=models.DurationField()
    no_of_clicks=models.PositiveIntegerField('clicks')
    no_of_pages_viewed=models.PositiveIntegerField('pages viewed')

    class Meta:
        verbose_name_plural="Sessions"

    def __str__(self):
        return self.id


class Pricing(models.Model):
    id=models.AutoField(primary_key=True)
    product_details=models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    discount_id=models.PositiveIntegerField()
    gst=models.DecimalField(decimal_places=2,max_digits=10)
    total_price=models.DecimalField(decimal_places=2,max_digits=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Pricing"

    def __str__(self):
        return self.product_details.product_id


    #function to determine the total price of the product based upon the gst and discount
    def save(self, *args, **kwargs):
        price=float(self.price)
        #calculating  price after discount
        price_after_discount=(price*(1-float((self.discount_id))/100))
        #calculating price after adding gst
        price_after_gst=(price_after_discount*(1+float(self.gst)/100))
        #converting price to Decimal datatype
        self.total_price=decimal.Decimal(price_after_gst)
        #saving object
        super(Pricing,self).save(*args, **kwargs)


class PricingLog(models.Model):
    id=models.AutoField(primary_key=True)
    product_details_id=models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Pricing Log'

    def __str__ (self):
        return self.product_details_id



class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def __unicode__ (self):
        return self.title
