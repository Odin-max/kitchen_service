from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Cook,
    Dish_type,
    Ingredient,
    Dish
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
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "email",
            "first_name",
            "last_name",
        )

class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ("first_name", "last_name", "years_of_experience", "email")


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Dish
        fields = "__all__"
