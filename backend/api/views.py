from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.models import (Ingredient, IngredientInRecipe, Recipe,
                             ShoppingCart, Tag)
from users.models import Subscription, User

from .filters import RecipeFilter
from .mixins import ListCreateRetrieveUpdateDestroyViewSet, ListRetrieveViewSet
from .pagination import UserRecipePagination
from .permissions import IsAuthenticatedOwnerOrAdminOnly
from .serializers import (IngredientSerializer, RecipeMinifiedSerializer,
                          RecipeReadSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserDjoserCreateSerializer, UserDjoserSerializer)


class UserViewSet(UserViewSet):
    queryset = User.objects.all().order_by(F('username'))
    http_method_names = ['get', 'post', 'delete']
    pagination_class = UserRecipePagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserDjoserCreateSerializer
        return UserDjoserSerializer

    @action(
        detail=False,
        permission_classes=[IsAuthenticatedOwnerOrAdminOnly]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            subscribed_to__user=request.user).order_by('subscribed_to')
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOwnerOrAdminOnly]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        subscription = Subscription.objects.filter(
            user=user, author=author
        )
        if request.method == 'POST':
            if subscription:
                return Response(
                    {'errors': 'Вы уже подписаны на данного автора'},
                    status=status.HTTP_400_BAD_REQUEST)
            elif user == author:
                return Response(
                    {'errors': 'Вы пытаетесь подписаться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(
                user=user, author=author)
            serializer = UserDjoserSerializer(
                author, context={'request': request, })
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        if not subscription:
            return Response(
                {'errors': 'У Вас нет подписки на данного автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all().order_by(F('name'))
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    http_method_names = ['get', ]
    lookup_fields = ['id']
    search_fields = ('^name', )
    # permission_classes = [IsAdminUser]


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all().order_by(F('id'))
    serializer_class = TagSerializer
    http_method_names = ['get', ]
    lookup_fields = ['id']
    # permission_classes = [IsAdminUser]


class RecipeViewSet(ListCreateRetrieveUpdateDestroyViewSet):
    queryset = Recipe.objects.all().add_user_annotations(F('user_id'))
    serializer_class = RecipeSerializer(partial=True)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = UserRecipePagination
    permission_classes = [IsAuthenticatedOwnerOrAdminOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeSerializer

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        response = HttpResponse(content_type='text/plain')
        response[
            'Content-Disposition'
        ] = 'attachment; filename=shopping_list.txt'

        user = request.user
        ingredients = IngredientInRecipe.objects.filter(
            recipe__foodgram_shoppingcarts__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(
                total_amount=Sum('amount')
        )
        lines = []
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            amount = ingredient['total_amount']
            unit = ingredient['ingredient__measurement_unit']
            lines += f'{name}: {amount} {unit}\n'
        response.writelines(lines)
        return response

    @staticmethod
    def post_or_delete_object(obj, recipe, request):
        if request.method == 'POST':
            if obj.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Ошибка добавления. Уже есть в списке'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            obj.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        obj.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        permission_classes=[IsAuthenticatedOwnerOrAdminOnly],
        methods=['POST', 'DELETE']
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self.post_or_delete_object(
            obj=ShoppingCart, recipe=recipe, request=request)

    @action(
        detail=True,
        permission_classes=[IsAuthenticatedOwnerOrAdminOnly],
        methods=['POST', 'DELETE']
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self.post_or_delete_object(
            obj=ShoppingCart, recipe=recipe, request=request)
