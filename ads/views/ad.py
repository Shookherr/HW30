from django.http import JsonResponse

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad
from ads.permissions import IsStaff, IsOwner
from ads.serializers.ad import AdSerializer, AdListSerializer, AdDetailSerializer


def main_view(request):
    return JsonResponse({'status': 'OK'})


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')

    default_serializer_class = AdSerializer
    default_permission = [AllowAny]

    serializers = {
        'list': AdListSerializer,
        'create':  AdListSerializer,
        'retrieve': AdDetailSerializer,
    }
    permissions = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsStaff | IsOwner],
        'partial_update': [IsAuthenticated, IsStaff | IsOwner],
        'destroy': [IsAuthenticated, IsStaff | IsOwner],
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def list(self, request, *args, **kwargs):

        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)
