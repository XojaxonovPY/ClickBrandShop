import re

from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms import Form, CharField

from apps.models import User, OrderItem, Order, Payment, Address, Wishlist


class RegisterForm(Form):
    phone_number = CharField(max_length=20)

    def clean_phone_number(self):
        phone_number = f'998{self.cleaned_data.get('phone_number')}'
        phone_number = re.sub(r'\D', '', phone_number)
        query = User.objects.filter(phone_number=phone_number)

        if not query.exists():
            if len(phone_number) >= 10:
                user = User.objects.create(phone_number=phone_number)
                self.user = user
            else:
                raise ValidationError('Phone number must be 10 digits')
        else:
            self.user = query.first()
        return phone_number


class OrderItemModelForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity', 'product', 'user', 'attribute')


class AddressModelForm(ModelForm):
    class Meta:
        model = Address
        fields = ('entrance_hall', 'user', 'floor', 'room', 'description', 'address')


class ProfileModelForm(ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = re.sub(r'\D', '', phone_number)
        return phone_number
