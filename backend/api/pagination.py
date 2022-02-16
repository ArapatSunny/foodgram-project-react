from rest_framework.pagination import PageNumberPagination


class UserRecipePagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'limit'
