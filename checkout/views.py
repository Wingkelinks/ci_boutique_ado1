from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JQoRzHrWnDXRtorpqNZRclQqwK1mQfhIhTNULauqhCjv4B83oeMURhLARrtwiAM548atfSbEGCkFYxabsgHb57D00sDPm0cRS',
        'client_secret': 'test client secret',
    }
    
    return render(request, template, context)