# Create the cart and every time we add, update or remove a dish we are going to save our cart

from menu.models import MenuItem

def get_cart(request):
    """
    Get the cart from the session:
    The cart will be a dictionary: (key value pair)
        - key: dish id -> will be a string
        - value: number of dishes ordered
    return: the cart session
    """
    # We are going to check if the cart exists in the session
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    return request.session['cart']



def save_cart(request, cart): # cart updated
    """
    save the changes in the cart
    """
    try:
        request.session['cart'] = cart
        request.session.modified = True
    except Exception as e:
        print(f"Error: {e}")