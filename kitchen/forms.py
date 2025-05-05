from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator

from .models import (
    Cook,
    Dish_type,
    Ingredient,
    Dish
)

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cook


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        )
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "First name", "class": "form-control"}
        )
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Last name", "class": "form-control"}
        )
    )
    years_of_experience = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": "Years of experience", "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta:
        model = Cook
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "years_of_experience",
            "password1",
            "password2",
        )


class GenericSearchForm(forms.Form):
    search_field_name = "name"
    placeholder = "Search"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.search_field_name] = forms.CharField(
            max_length=255,
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={
                    "placeholder": self.placeholder
                }
            )
        )


class IngredientSearchForm(GenericSearchForm):
    placeholder = "Search by Ingredient"


class DishTypeSearchForm(GenericSearchForm):
    placeholder = "Search by Dish type"


class CookSearchForm(GenericSearchForm):
    search_field_name = "username"
    placeholder = "Search by username"


class DishSearchForm(GenericSearchForm):
    placeholder = "Search by Dish name"


class CookCreationForm(UserCreationForm):
    years_of_experience = forms.IntegerField(
        validators=[MaxValueValidator(100)],
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "email",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Username",
            "email": "Email address",
            "first_name": "First name",
            "last_name": "Last name",
            "password1": "Password",
            "password2": "Password confirmation",
            "years_of_experience": "Years of experience",
        }

        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = placeholders.get(field_name, "")
            field.label = ""

class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["username", "first_name", "last_name", "email", "years_of_experience"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control"}),
        }



class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "ingredients": forms.SelectMultiple(attrs={"class": "select2 form-control"}),
            "cooks": forms.SelectMultiple(attrs={"class": "select2 form-control"}),
            "dish_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 1,
                "placeholder": "Enter description...",
            }),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }
