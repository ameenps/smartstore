from django.shortcuts import render,redirect
from .models import Order,OrderdItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from products.models import Product


# Create your views here.

def show_cart(request):
    user=request.user
    customer=user.customer_profile
    
    
    cart_obj,created=Order.objects.get_or_create(
            
            owner=customer,
            order_status=Order.CART_STAGE
        )
   
  
    context={ 'cart' :cart_obj}
    
    return render(request,'cart.html',context)


def remove_item_from_cart(request,pk):
    item=OrderdItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')   


def checkout_cart(request):
    if request.POST:
        try:
            user=request.user
            customer=user.customer_profile
            total=float(request.POST.get('total'))  
            
            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.save()
                status_message='Your order is processed.Your item will be deliverd in 2 days' 
                messages.success(request,status_message) 
            else:
                status_message='unable to processed. No items in the cart'
                messages.error(request,status_message)
        except Exception as e:
               status_message='unable to processed. No items in the cart'
               messages.error(request,status_message)
    return redirect('cart')

@login_required(login_url='account')
def show_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request,'orders.html',context)


@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))  
        product_id=request.POST.get('product_id')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product=Product.objects.get(pk=product_id)
        orderd_item, created = OrderdItem.objects.get_or_create(
            Product= product,
            owner=cart_obj,
        )
        
        if  created:
            orderd_item.quantity = quantity
            orderd_item.save()
        else:
            orderd_item.quantity = orderd_item.quantity+quantity
        
        orderd_item.save()

    return redirect('cart')   