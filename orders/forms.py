from django import forms
import re


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    address = forms.CharField()
    note = forms.CharField()
    payment = forms.CharField()

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        pattern = re.compile(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
        if not pattern.match(data):
            raise forms.ValidationError("Номер телефона должен содержать только цифры")

        # pattern = re.compile(r"^\d(10)$")
        # if not pattern.match(data):
        #     raise forms.ValidationError("Неверный формат номера")

        return data
