from django.test import TestCase
from kitchen.forms import (
    LoginForm,
    SignUpForm,
    CookCreationForm,
    CookUpdateForm,
    DishForm
)
from kitchen.models import Cook, Dish_type, Ingredient


class LoginFormTest(TestCase):
    def test_valid_data(self):
        form = LoginForm(data={"username": "john", "password": "secret"})
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())


class SignUpFormTest(TestCase):
    def test_valid_data(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 5,
            "password1": "Strongpass123",
            "password2": "Strongpass123",
        })
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "user@example.com",
            "password1": "pass1",
            "password2": "pass2",
        })
        self.assertFalse(form.is_valid())


class CookCreationFormTest(TestCase):
    def test_missing_experience(self):
        form = CookCreationForm(data={
            "username": "testuser",
            "password1": "pass123456",
            "password2": "pass123456",
        })
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form = CookCreationForm(data={
            "username": "chef",
            "password1": "Strongpass123",
            "password2": "Strongpass123",
            "years_of_experience": 3,
            "email": "chef@test.com",
            "first_name": "Chef",
            "last_name": "Gordon",
        })
        self.assertTrue(form.is_valid())


class CookUpdateFormTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create_user(username="cook", password="test123")

    def test_valid_update(self):
        form = CookUpdateForm(data={
            "username": "cook",
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@email.com",
            "years_of_experience": 2,
        }, instance=self.cook)
        self.assertTrue(form.is_valid())


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = Dish_type.objects.create(name="Main")
        self.ingredient = Ingredient.objects.create(name="Tomato")
        self.cook = Cook.objects.create_user(username="chef", password="12345")

    def test_valid_form(self):
        form = DishForm(data={
            "name": "Pizza",
            "description": "Tasty",
            "price": 10.00,
            "dish_type": self.dish_type.id,
            "ingredients": [self.ingredient.id],
            "cooks": [self.cook.id],
        })
        self.assertTrue(form.is_valid())
