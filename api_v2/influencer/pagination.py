from rest_framework import pagination

class InfluencerListPagination(pagination.PageNumberPagination):
       page_size = 12