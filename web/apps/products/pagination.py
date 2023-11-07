from rest_framework.pagination import PageNumberPagination

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 3

class ProductPagination(PageNumberPagination):
    # page = DEFAULT_PAGE
    page_size: int = DEFAULT_PAGE_SIZE
    page_size_query_param: str = 'page_size'