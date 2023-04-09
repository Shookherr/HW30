from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import IntegerField

from users.models import User, Location
from users.serializers.location import LocationSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']


class UserDetailSerializer(ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = User
        exclude = ['password']


class UserListSerializer(ModelSerializer):
    total_ads = IntegerField()

    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False, many=True, slug_field='name', queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)

        for loc_name in self._locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            new_user.location.add(loc)
        return new_user

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False, many=True, slug_field='name', queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.location.clear()
        for loc_name in self._locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.location.add(loc)
        return user

    class Meta:
        model = User
        fields = '__all__'
