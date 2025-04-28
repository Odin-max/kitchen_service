from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

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
    DishForm
)

@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = Dish_type.objects.count()

    # num_visits = request.session.get("num_visits", 0)
    # request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        # "num_visits": num_visits + 1,
    }

    return render(request, "", context=context)


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
            if search_value:
                filter_kwargs = {f"{self.search_field}__icontains": search_value}
                queryset = queryset.filter(**filter_kwargs)
        return queryset


class IngredientListView(LoginRequiredMixin, GenericSearchListView):
    model = Ingredient
    context_object_name = "ingredients_list"
    template_name = ""
    paginate_by = 5
    search_form_class = IngredientSearchForm
    

class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
   model = Ingredient
   fields = "__all__"
   success_url = reverse_lazy("")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
   model = Ingredient
   fields = "__all__"
   success_url = reverse_lazy("")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
   model = Ingredient
   success_url = reverse_lazy("")

class DishTypeListView(LoginRequiredMixin, GenericSearchListView):
    model = Dish_type
    context_object_name = "dish_type_list"
    template_name = ""
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
    context_object_name = "cooks_list"
    template_name = ""
    paginate_by = 5
    queryset = Cook.objects.prefetch_related("dishes")
    search_form_class = CookSearchForm

    
class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")

class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = ["first_name", "last_name", "username", "years_of_experience"]
    form_class = CookCreationForm
    success_url = reverse_lazy("")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
   model = Cook
   fields = "__all__"
   form_class = CookUpdateForm
   success_url = reverse_lazy("")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
   model = Cook
   success_url = reverse_lazy("")


class DishListView(LoginRequiredMixin, GenericSearchListView):
    model = Dish
    context_object_name = "dishes_list"
    template_name = ""
    paginate_by = 5
    queryset = Dish.objects.select_related("dish_type").prefetch_related("ingredients", "cooks")
    search_form_class = DishSearchForm


class DishDetailView(LoginRequiredMixin, generic.DetailView):
   model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    dish = Dish.objects.get(id=pk)

    if dish in cook.dishes.all():
        cook.dishes.remove(dish)
    else:
        cook.dishes.add(dish)

    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail"), args=[pk])