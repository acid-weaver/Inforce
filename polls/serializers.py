from rest_framework import serializers

from polls.models import Restaurant, Menu, Vote
from users.models import User


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'menus', 'created_by',
                  'created_at', 'updated_at')
        read_only_fields = ('created_by', 'menus', 'created_at', 'updated_at')

    def create(self, validated_data):
        name = validated_data.get('name', '')
        address = validated_data.get('address', '')

        # IsAuthenticated permission grants created_by not AnonimousUser
        created_by = self.context['request'].user
        created_by = User.objects.get(username=created_by)

        restaurant = Restaurant.objects.create(name=name, address=address,
                                               created_by=created_by)

        return restaurant


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'date', 'dishes', 'restaurant',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class MenuResultSerializer(serializers.ModelSerializer):
    result = serializers.IntegerField()

    class Meta:
        model = Menu
        fields = ('id', 'date', 'dishes', 'restaurant',
                  'result', 'created_at', 'updated_at')
        read_only_fields = fields


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'employee', 'menu', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
