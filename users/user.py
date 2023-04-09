from django.db.models import Q, Count
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination

from ads.models import User
from users.serializers.user import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserPagination(PageNumberPagination):  # set page size for users listing
    page_size = 5


class UserListView(ListAPIView):
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')
    serializer_class = UserListSerializer
    pagination_class = UserPagination


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
