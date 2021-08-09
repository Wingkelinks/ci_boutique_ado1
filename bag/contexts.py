# decimal better than float for money as float susceptible to rounding errors
from boutique_ado.settings import FREE_DELIVERY_THRESHOLD
from decimal import Decimal  
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


""" Rather than return a template, this function will return a dictionary called context. This is known as a context processor which serves to make the dictionary available to all templates across the entire application (by putting it in settings.py) """

def bag_contents(request):
    
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    
    for item_id, item_data in bag.items(): # for each item & quantities in bag in session
        if isinstance(item_data, int):
            
            product = get_object_or_404(Product, pk=item_id) # get the product 
            total += item_data * product.price # add quantity and multiply by price
            product_count += item_data # increment product count by quantity
            # add a dictionary to list of bag items containing id, quantity & product object to be able to access other product fields
            bag_items.append({ 
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
        })
        else:
            product = get_object_or_404(Product, pk=item_id) # get the product 
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })
    
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0 
        
    grand_total = delivery + total 
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context
