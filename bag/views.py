from django.shortcuts import redirect, render

# Create your views here.
def view_bag(request):  
    """ A view that renders the shopping bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag. """
    
    quantity = int(request.POST.get('quantity')) # convert string from template to integer
    redirect_url = request.POST.get('redirect_url')
    size = None # set size to none
    if 'product_size' in request.POST: # then if size is in request.post, set it equal to that
        size = request.POST['product_size']    
    bag = request.session.get('bag', {}) # check if user in session has a bag & if not, create one (dictionary)
    
    # check if product with sizes is being added to bag
    if size: 
        if item_id in list(bag.keys()): # if item already in bag, check if another item with same id & size exists
            if size in bag[item_id]['items_by_size'].keys(): # if so
                bag[item_id]['items_by_size'][size] += quantity # increment the quantity for that size
            else: # otherwise, set it equal to the quantity
                bag[item_id]['items_by_size'][size] = quantity
        else: # if item not already in bag, add it using dict with key of    items_by_size
            bag[item_id] = {'items_by_size': {size: quantity}}
    # if no size for item 
    else: 
        if item_id in list(bag.keys()): # if item already in bag dictionary
            bag[item_id] += quantity # then increment quantity accordingly
        else:
            bag[item_id] = quantity # else add item and quantity to bag
        
    request.session['bag'] = bag # update bag variable in session
    # print(request.session['bag']) # print used for testing 'add to bag' function
    return redirect(redirect_url)