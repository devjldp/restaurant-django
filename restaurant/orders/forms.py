from django import forms

# import the model from customer app
from customers.models import CustomerProfile


# Create the form with personal customer data

class OrderForm(forms.ModelForm):
    model = CustomerProfile
    fields = ['first_name', 'street', 'postal_code', 'city', 'phone_number'] # field in the model

    #  constructor to render the form with values from the customer
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        if self.isinstance:
            for field_name, field in self.fields.items():
                value = getattr(self.instance, field_name)
                field.widget.attrs['value'] = value


# Create a from to proccess the payment: credit/debit card details

