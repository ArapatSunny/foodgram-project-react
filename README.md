# praktikum_new_diplom

### Сайт Foodgram, «Продуктовый помощник».
## Описание:
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта
В папке infra выполните команду docker-compose up.
При выполнении этой команды сервис frontend, описанный в docker-compose.yml подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/
Как будет выглядеть ваше приложение, можно посмотреть на Figma.com

# Сервисы и страницы проекта:
Главная страница, Страница рецепта, Страница пользователя, Подписка на авторов, Список избранного, Список покупок, Фильтрация по тегам, Регистрация и авторизация

### Технологии:
django==3.2
djangorestframework==3.13.1
django-filter==21.1
djoser==2.1.0
drf-extra-fields==3.2.1
drf-writable-nested==0.6.3
drf-yasg==1.20.0
gunicorn==20.0.4
psycopg2-binary==2.9.3
PostgreSQL
nginx

Модели: Ingredient, Tag, Recipe, Favorite, ShoppingCart, IngredientInRecipe

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ArapatSunny/foodgram-project-react.git
```

```
cd infra
```

Запуск контейнеров:

```
docker-compose up -d --build
```

```
docker-compose exec backend python manage.py migrate
```

```
docker-compose exec backend python manage.py collectstatic --no-input
```

Наполнение базы данными для рецептов

```
docker-compose exec backend python manage.py import --path '/app/data/ingredients.csv' --model_name 'foodgram.Igredient'
```

```
docker-compose exec backend python manage.py import --path '/app/data/tags.csv' --model_name 'foodgram.Tag'
```


### Примеры. Некоторые примеры запросов к API.

Запрос на получение списка рецептов:

```
http://api/recipes/
```

Запрос на получение списка подписок
```
http://api/users/subscription
```
IP-адрес сервера: 62.84.124.46

Доступ для администратора:
login: admin
password: foodgram

Тестовые пользователи:
  "email": "cate@yandex.ru"
  "password": "Cateeee123"

  "email": "nikita@ya.ru"
  "password": "vital555" 

Автор проекта:
Ансарова Арапат
Студент курса ЯндексПрактикум Python-разработчик
Факультет Бэкенд.