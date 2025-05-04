from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from .models import (
    Cook,
    Dish_type,
    Ingredient,
    Dish
)

from .forms import (
    IngredientSearchForm,
    DishTypeSearchForm,
    CookSearchForm,
    DishSearchForm,
    CookCreationForm,
    CookUpdateForm,
    DishForm,
    LoginForm,
    SignUpForm,
)

@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = Dish_type.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


def login_view(request):
    form = LoginForm(request.POST or None)

    log_msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                log_msg = 'Invalid credentials'
        else:
            log_msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg":log_msg})

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully. Please log in.")
            return redirect("kitchen:login")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})


class GenericSearchListView(generic.ListView):
    search_form_class = None
    search_field = "name"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.search_form_class(self.request.GET)
        form.is_valid()
        context["search_form"] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            search_value = form.cleaned_data.get(self.search_field)
            if search_value in [None, "None", ""]:
                search_value = None
            if search_value:
                filter_kwargs = {f"{self.search_field}__icontains": search_value}
                queryset = queryset.filter(**filter_kwargs)
        return queryset


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IngredientListView(LoginRequiredMixin, GenericSearchListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5
    search_form_class = IngredientSearchForm
    

class IngredientCreateView(SuperuserRequiredMixin,LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = ["name"]
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(SuperuserRequiredMixin, LoginRequiredMixin, generic.UpdateView):
   model = Ingredient
   fields = "__all__"
   success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(SuperuserRequiredMixin, LoginRequiredMixin, generic.DeleteView):
   model = Ingredient
   success_url = reverse_lazy("kitchen:ingredient-list")

class DishTypeListView(LoginRequiredMixin, GenericSearchListView):
    model = Dish_type
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5
    search_form_class = DishTypeSearchForm


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
   model = Dish_type
   fields = "__all__"
   success_url = reverse_lazy("")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
   model = Dish_type
   fields = "__all__"
   success_url = reverse_lazy("")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
   model = Dish_type
   success_url = reverse_lazy("")


class CookListView(LoginRequiredMixin, GenericSearchListView):
    model = Cook
    search_field = "username"
    context_object_name = "cooks_list"
    template_name = "cook_list"
    paginate_by = 5
    queryset = Cook.objects.prefetch_related("dishes")
    search_form_class = CookSearchForm

    
class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")

    def test_func(self):
        return self.request.user.is_superuser


class CookUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin,SuperuserRequiredMixin, generic.DeleteView):
   model = Cook
   template_name = "kitchen/cook_confirm_delete.html"
   success_url = reverse_lazy("kitchen:cook-list")

   def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_superuser:
            return HttpResponseForbidden("Cannot delete superuser.")
        return super().dispatch(request, *args, **kwargs)


class DishListView(LoginRequiredMixin, GenericSearchListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5
    queryset = Dish.objects.select_related("dish_type").prefetch_related("ingredients", "cooks")
    search_form_class = DishSearchForm


class DishDetailView(LoginRequiredMixin, generic.DetailView):
   model = Dish


class DishCreateView(LoginRequiredMixin,SuperuserRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin,SuperuserRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin,SuperuserRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = get_object_or_404(Cook, id=request.user.id)
    dish = get_object_or_404(Dish, id=pk)

    if dish in cook.dishes.all():
        cook.dishes.remove(dish)
    else:
        cook.dishes.add(dish)

    next_url = request.POST.get("next") or reverse("kitchen:dish-list")
    return redirect(next_url)
