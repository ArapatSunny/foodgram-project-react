from django_filters.rest_framework import FilterSet, filters

from foodgram.models import Recipe


class RecipeFilter(FilterSet):
    author = filters.AllValuesMultipleFilter(
        field_name='author__id'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorite = filters.BooleanFilter(
        method='get_is_favorite'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = [
            'author', 'tags',
            'is_favorite', 'is_in_shopping_cart'
        ]

    def get_is_favorite(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Recipe.objects.filter(
                recipe_foodgram_favorite_related__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Recipe.objects.filter(
                recipe_foodgram_shoppingcart_related__user=self.request.user)
        return queryset
