from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class PageNumberPaginatorModified(PageNumberPagination):
    page_size_query_param = 'limit'
