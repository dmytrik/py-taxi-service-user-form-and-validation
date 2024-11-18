from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverValidationLicenseNumber:
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        condition_ = (len(license_number) == 8
                      and license_number[:3].isupper()
                      and license_number[:3].isalpha()
                      and license_number[3:].isnumeric())
        if not condition_:
            raise ValidationError("License number invalid")

        return license_number


class DriverCreationForm(UserCreationForm, DriverValidationLicenseNumber):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number"))


class DriverLicenseUpdateForm(forms.ModelForm, DriverValidationLicenseNumber):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
