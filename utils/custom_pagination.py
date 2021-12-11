from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):

    page_size_query_param = 'size'
    max_page_size = 20

    def get_paginated_response(self, data):
        code = 0
        msg = 'success'

        return Response(OrderedDict([
            ('code', code),
            ('message', msg),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))
