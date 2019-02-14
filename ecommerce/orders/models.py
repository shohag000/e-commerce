from django.db import models
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save,post_save
from decimal import Decimal
from billing.models import BillinigProfile
from addresses.models import Address

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True,status="created")
        if qs.exists():
            obj = qs.first()
        else:
            print("Order object created")
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj)
            created = False
        return obj , created

class Order(models.Model):
    billing_profile = models.ForeignKey(BillinigProfile,on_delete=models.CASCADE,null=True,blank=True)
    shipping_address= models.ForeignKey(Address,null=True,blank=True,on_delete=models.CASCADE,
                                        related_name="shipping_address")
    billing_address = models.ForeignKey(Address, null=True, blank=True,on_delete=models.CASCADE,
                                        related_name="billing_address")
    order_id        = models.CharField(max_length=120,blank=True)
    cart            = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status          = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=10.00, max_digits=100, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active          = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = Decimal(cart_total) + Decimal(shipping_total)
        self.total=new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0 :
            return True
        else:
            return False

    def mark_paid(self):
        if self.check_done():
            self.status="paid"
            self.save()
        return self.status


def order_id_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    old_order_qs = Order.objects.filter(cart=instance.cart, active=True).exclude(
        billing_profile=instance.billing_profile)
    if old_order_qs.exists():
        old_order_qs.update(active=False)
        print("Old order query: ")
        print(old_order_qs)


pre_save.connect(order_id_pre_save_receiver,sender=Order)


def post_save_cart_total(sender,instance,created,*args,**kwargs):
    print("Running post_save_cart_total")
    if not created: # For only existing model object(Cart)
        print("Updating post_save_cart_total")
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.exists(): # qs.count()==1 (According to tutorial)
            order_obj = qs.last()   # order_obj = qs.first() (According to tutorial)
            order_obj.update_total()


post_save.connect(post_save_cart_total,sender=Cart)


def post_save_order(sender,instance,created,*args,**kwargs):
    print("Running post_save_order")
    if created: # For only new model object(Order)
        print("Updating post save order")
        instance.update_total()


post_save.connect(post_save_order,sender=Order)