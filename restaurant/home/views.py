from django.shortcuts import render

# Create your views here.
def index(request): # link this one with url: locsalhots/
    """
    This view renders the landing page
    
    
    """
    return render(request, 'index.html')


# one function to insert data <-> url create dish
# one function to remove data <-> url delete a dish
 # one function to search
# one function to update