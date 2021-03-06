# Generated by Django 3.2 on 2022-02-05 17:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Укажите название игредиента. Например: Капуста', max_length=200, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Единицы измерения. Например: кг', max_length=200, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Минимальное количество 1', verbose_name='Количество в рецепте')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_in_recipe', to='foodgram.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Картинка, закодированная в Base64', upload_to='recipes/', verbose_name='Изображение рецепта')),
                ('name', models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название')),
                ('text', models.TextField(help_text='Описание Вашего рецепта здесь', verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Время приготовления (в минутах)', verbose_name='Время приготовления (в минутах)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='foodgram.IngredientInRecipe', to='foodgram.Ingredient', verbose_name='Список ингредиентов')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите навзание тега. Например, "Завтрак"', max_length=200, unique=True, verbose_name='Название')),
                ('color', models.CharField(help_text='Цвет в HEX', max_length=7, null=True, unique=True)),
                ('slug', models.SlugField(help_text='Укажите уникальный фрагмент URL-адреса для тега. Используйте только латиницу, цифры, дефисы и знаки подчёркивания.', max_length=200, null=True, unique=True, verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='foodgram.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='foodgram.tag')),
            ],
            options={
                'unique_together': {('recipe', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_foodgram_shoppingcart_related', related_query_name='foodgram_shoppingcarts', to='foodgram.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_foodgram_shoppingcart_related', related_query_name='foodgram_shoppingcarts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Добавьте теги к своему рецепту', related_name='recipes', through='foodgram.TagRecipe', to='foodgram.Tag', verbose_name='Список id тегов'),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_in_recipe', to='foodgram.recipe'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_foodgram_favorite_related', related_query_name='foodgram_favorites', to='foodgram.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_foodgram_favorite_related', related_query_name='foodgram_favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='shoppingcart_unique_favorite_user_recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientinrecipe',
            unique_together={('recipe', 'ingredient')},
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='favorite_unique_favorite_user_recipe'),
        ),
    ]
