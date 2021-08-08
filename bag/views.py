from django.shortcuts import redirect, render

# Create your views here.
def view_bag(request):  
    """ A view that renders the shopping bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag. """
    
    quantity = int(request.POST.get('quantity')) # convert string from template to integer
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {}) # check if user in session has a bag & if not, create one (dictionary)
    
    if item_id in list(bag.keys()): # if item already in bag dictionary
        bag[item_id] += quantity # then increment quantity accordingly
    else:
        bag[item_id] = quantity # else add item and quantity to bag
        
    request.session['bag'] = bag # update bag variable in session
    # print(request.session['bag']) # print used for testing 'add to bag' function
    return redirect(redirect_url)