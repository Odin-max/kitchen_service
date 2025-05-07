from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen.models import Ingredient, Dish_type, Dish

User = get_user_model()


class PublicViewsTests(TestCase):
    def test_login_view_renders_correct_template(self):
        response = self.client.get(reverse("kitchen:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_register_view_renders_correct_template(self):
        response = self.client.get(reverse("kitchen:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")


class PrivateViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.superuser = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_index_view_authenticated(self):
        response = self.client.get(reverse("kitchen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/index.html")

    def test_ingredient_list_view(self):
        Ingredient.objects.create(name="Salt")
        response = self.client.get(reverse("kitchen:ingredient-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salt")

    def test_dish_type_list_view(self):
        Dish_type.objects.create(name="Dessert")
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dessert")

    def test_dish_list_view(self):
        dish_type = Dish_type.objects.create(name="Main")
        dish = Dish.objects.create(name="Pizza", price=10.0, dish_type=dish_type)
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")

    def test_toggle_assign_to_dish_adds_and_removes(self):
        dish_type = Dish_type.objects.create(name="Appetizer")
        dish = Dish.objects.create(name="Soup", price=5.5, dish_type=dish_type)
        response = self.client.post(
            reverse("kitchen:dish-assign-toggle", args=[dish.id]),
            follow=True
        )
        self.assertRedirects(response, reverse("kitchen:dish-list"))
        self.assertIn(dish, self.user.dishes.all())

        self.client.post(reverse("kitchen:dish-assign-toggle", args=[dish.id]))
        self.assertNotIn(dish, self.user.dishes.all())
