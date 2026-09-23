from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsSuperAdmin, IsAdminUserOrReadOnly

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    permission_classes = [IsAdminUserOrReadOnly]
