from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Order
from .tasks import order_created


# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # Usunięcie zawartości koszyka na zakupy.
            cart.clear()
            # Uruchomienie zadania asynchronicznego.
            order_created.delay(order.id) # Umieszczenie zamówienia w sesji.
            request.session['order_id'] = order.id # Przekierowanie do płatności.
            return redirect(reverse('payment:process'))


    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
