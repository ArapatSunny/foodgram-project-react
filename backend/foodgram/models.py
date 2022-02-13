from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef
from users.models import User


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Укажите навзание тега. Например, "Завтрак"',
    )
    color = models.CharField(
        max_length=7,
        help_text='Цвет в HEX',
        unique=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        verbose_name="Уникальный слаг",
        help_text=(
            "Укажите уникальный фрагмент URL-адреса "
            "для тега. Используйте только латиницу, "
            "цифры, дефисы и знаки подчёркивания."
        ),
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиента."""
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента',
        help_text='Укажите название игредиента. Например: Капуста',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        help_text='Единицы измерения. Например: кг',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    """
    Получение дополнительных полей
    is_favorite и is_in_shopping_cart
    в queryset Recipe.
    """
    def add_user_annotations(self, user_id):
        return self.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=OuterRef('pk')
                )
            ),
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    user_id=user_id, recipe__pk=OuterRef('pk')
                )
            ),
        )


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Список ингредиентов',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Список id тегов',
        help_text='Добавьте теги к своему рецепту',
    )
    image = models.ImageField(
        upload_to='recipes/media/image/',
        verbose_name='Изображение рецепта',
        help_text='Картинка, закодированная в Base64',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название рецепта',
    )
    text = models.TextField(
        help_text='Описание Вашего рецепта здесь',
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Время приготовления (в минутах)',
        verbose_name='Время приготовления (в минутах)',
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tag'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tag'
    )

    class Meta:
        unique_together = [['recipe', 'tag']]

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class IngredientInRecipe(models.Model):
    """В этой модели будут связаны id ингредиента и id рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Минимальное количество 1',
        verbose_name='Количество в рецепте',
    )

    class Meta:
        unique_together = [['recipe', 'ingredient']]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class UserRecipe(models.Model):
    """
    Промежуточная модель,
    которая свяжет юзера и рецепт.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name='Рецепт'
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created']

        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(class)s_unique_favorite_user_recipe'
            )
        ]

    def __str__(self):
        return f'Пользователь: {self.user}, рецепт {self.recipe}'


class Favorite(UserRecipe):
    """
    Промежуточная модель,
    которая свяжет юзера и его избранное.
    """
    pass


class ShoppingCart(UserRecipe):
    """
    Промежуточная модель,
    которая свяжет юзера и его список покупок.
    """
    pass
