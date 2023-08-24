from rest_framework.pagination import PageNumberPagination

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 3

class ProductPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        }

