from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from products.models import Product

# Create your views here.


def view_bag(request):
    """ A view that renders the shopping bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag. """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    # convert string from template to integer
    redirect_url = request.POST.get('redirect_url')
    size = None # set size to none
    if 'product_size' in request.POST:
        # then if size is in request.post, set it equal to that
        size = request.POST['product_size']
    bag = request.session.get('bag', {})
    # check if user in session has a bag & if not, create one (dictionary)

    # check if product with sizes is being added to bag
    if size:
        if item_id in list(bag.keys()):
            # if item already in bag
            # check if another item with same id & size exists
            if size in bag[item_id]['items_by_size'].keys(): # if so
                bag[item_id]['items_by_size'][size] += quantity
                # increment the quantity for that size
                messages.success(request,
                                 f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else: # otherwise, set it equal to the quantity
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        # if item not already in bag
        # #add it using dict with key of items_by_size
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request,
                             f'Added size {size.upper()} {product.name} to your bag')
    # if no size for item
    else:
        if item_id in list(bag.keys()): # if item already in bag dictionary
            bag[item_id] += quantity # then increment quantity accordingly
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')    
        else:
            bag[item_id] = quantity # else add item and quantity to bag
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    # update bag variable in session
    # print(request.session['bag']) # print used for testing 'add to bag' function
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount. 

        This comes from a form on the shopping bag page which will contain the new quantity a user wants. So, if quantity is greater than 0, we will set the items quantity accordingly. Otherwise, we will remove the item. 
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request,
                             f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request,
                                 f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request,
                             f'Updated {product.name} quantity {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag. """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request,
                                 f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
