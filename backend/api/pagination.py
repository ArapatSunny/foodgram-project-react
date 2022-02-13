from rest_framework.pagination import PageNumberPagination


class UserRecipePagination(PageNumberPagination):
    page_size = 6
