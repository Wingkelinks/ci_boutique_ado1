# decimal better than float for money as float susceptible to rounding errors
from boutique_ado.settings import FREE_DELIVERY_THRESHOLD
from decimal import Decimal  
from django.conf import settings 


""" Rather than return a template, this function will return a dictionary called context. This is known as a context processor which serves to make the dictionary available to all templates across the entire application (by putting it in settings.py) """

def bag_contents(request):
    
    bag_items = []
    total = 0
    product_count = 0
    
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
