from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import pagination


from collections import OrderedDict


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('profile', data.get('profile')),
            ('results', data.get('data'))
        ]))

