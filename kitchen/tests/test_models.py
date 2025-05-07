from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from kitchen.models import Dish_type, Ingredient, Dish

Cook = get_user_model()


class CookModelTest(TestCase):
    def test_string_representation(self):
        cook = Cook(username="chefmax", first_name="Max", last_name="Prykhodko")
        self.assertEqual(str(cook), "chefmax (Max Prykhodko)")

    def test_years_of_experience_validation(self):
        cook = Cook(username="testuser", years_of_experience=150)
        with self.assertRaises(ValidationError):
            cook.full_clean()


class DishTypeModelTest(TestCase):
    def test_string_representation(self):
        dish_type = Dish_type(name="Appetizer")
        self.assertEqual(str(dish_type), "Appetizer")


class IngredientModelTest(TestCase):
    def test_string_representation(self):
        ingredient = Ingredient(name="Tomato")
        self.assertEqual(str(ingredient), "Tomato")


class DishModelTest(TestCase):
    def setUp(self):
        self.dish_type = Dish_type.objects.create(name="Main")
        self.ingredient1 = Ingredient.objects.create(name="Cheese")
        self.ingredient2 = Ingredient.objects.create(name="Bacon")
        self.cook = Cook.objects.create_user(username="chef1", password="pass")

    def test_string_representation(self):
        dish = Dish.objects.create(name="Burger", price=9.99, dish_type=self.dish_type)
        self.assertEqual(str(dish), "Burger")

    def test_dish_ingredients_and_cooks(self):
        dish = Dish.objects.create(name="Burger", price=9.99, dish_type=self.dish_type)
        dish.ingredients.set([self.ingredient1, self.ingredient2])
        dish.cooks.add(self.cook)

        self.assertEqual(dish.ingredients.count(), 2)
        self.assertIn(self.ingredient1, dish.ingredients.all())
        self.assertIn(self.cook, dish.cooks.all())
