from django import forms

# import model
from .models import CustomerProfile

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields =['first_name', 'last_name', 'street', 'city', 'post_code', 'phone_number']

        def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)
            if self.isinstance:
                for field_name, field in self.fields.items(): #=> key value pair first_mname: jose, city: cardiff
                    value = getattr(self.instance, field_name)
                    field.widget.attrs['placeholder'] = value