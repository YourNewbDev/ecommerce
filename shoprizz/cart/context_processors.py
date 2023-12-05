from .cart import Cart

# Create context processor so out cart can work on all pages of site
def cart(request):
    # Return default data from our Cart
    return {'cart': Cart(request)}