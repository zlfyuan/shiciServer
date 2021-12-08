from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):

    page_size_query_param = 'size'
    max_page_size = 20

    def get_paginated_response(self, data):
        code = 200
        msg = 'success'
        if not data:
            code = 404
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('code', code),
            ('message', msg),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))

    def get_none_page_response(self):
        return Response(OrderedDict([
            ('code', 200),
            ('message', "success"),
            ('count', None),
            ('next', None),
            ('previous', None),
            ('data', None),
        ]))